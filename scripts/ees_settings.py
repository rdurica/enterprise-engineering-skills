"""Shared catalog and user-settings logic for build-agents, opencode-config and the setup server.

Settings live in ${XDG_CONFIG_HOME:-~/.config}/enterprise-engineering-skills/settings.json and hold only
deviations from the pack defaults (agents.toml, config/opencode.json): an absent key means the current
default. Merging is per key, so a `codex.model` deviation leaves the default `codex.effort` alone.

    {"providers": ["claude", "codex"],
     "agents": {"<agent>": {"<provider>": {"model": ..., "effort"|"variant": ...}}},
     "opencode": {"model": ..., "small_model": ..., "agent": {"<id>": {"model": ..., "variant": ...}}}}

Unknown agents, providers, keys and values of the wrong type warn and are ignored; a value outside the
catalog warns and is still used. Warnings are plain strings, printed by callers as `warn    <text>`.

Models the user loads from their own tools on the setup page (Load models) live next to it in models.json,
{"<provider>": {"models": [...], "efforts"|"variants": [...], "source": ..., "loaded_at": ...}}. They extend
the pack catalog for the user's own values only; pack defaults must still be in config/models.toml.

API: settings_path, load_catalog, load_defaults, load_settings, merge_agents, merge_opencode,
local_models_path, load_local_models, with_local,
check_defaults, check_opencode_defaults, check_top_level, prune, write_settings, atomic_write, warn.

CLI (used by install.sh, which must only write JSON through Python):
    python3 scripts/ees_settings.py path                    print the settings.json path
    python3 scripts/ees_settings.py set-providers [<id>...] rewrite only `providers`, keep every other key
    python3 scripts/ees_settings.py get-providers           print the stored providers, one per line; exit 3
                                                            when settings.json has no valid `providers` list
Stdlib only, Python 3.11+.
"""
import copy
import json
import os
import sys
import tempfile
import tomllib
from pathlib import Path

pack = Path(__file__).resolve().parent.parent
providers = ("claude", "codex", "cursor", "opencode", "pi", "antigravity")
# Editable keys per provider (others, such as tools or color, stay in agents.toml) and their catalog list.
editable = {
    "claude": ("model", "effort"),
    "codex": ("model", "effort"),
    "cursor": ("model",),
    "opencode": ("model", "variant"),
    "pi": ("model", "variant"),
    "antigravity": ("model",),
}
catalog_list = {"model": "models", "effort": "efforts", "variant": "variants"}
top_level = ("providers", "agents", "opencode")
opencode_top = ("model", "small_model", "agent")
opencode_agent_keys = ("model", "variant")


def warn(text):
    print(f"warn    {text}", file=sys.stderr)


def settings_path():
    base = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return base / "enterprise-engineering-skills" / "settings.json"


def load_catalog(root=pack):
    return tomllib.loads((root / "config" / "models.toml").read_text(encoding="utf-8"))


def local_models_path():
    return settings_path().with_name("models.json")


def load_local_models(path=None):
    """Return (models.json as {provider: entry}, warnings). Missing is {}; unreadable or malformed parts warn."""
    path = path or local_models_path()
    if not path.is_file():
        return {}, []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return {}, [f"{path} cannot be read ({error}); ignored"]
    if not isinstance(data, dict):
        return {}, [f"{path} is not a JSON object; ignored"]
    out, warnings = {}, []
    for provider, entry in data.items():
        if provider not in providers or not isinstance(entry, dict):
            warnings.append(f"{path}: {provider!r} is not a known provider entry; ignored")
            continue
        lists = {k: v for k, v in entry.items() if k in catalog_list.values()}
        if not all(isinstance(v, list) and all(isinstance(x, str) for x in v) for v in lists.values()):
            warnings.append(f"{path}: {provider} lists must hold strings; ignored")
            continue
        out[provider] = entry
    return out, warnings


def with_local(catalog, local):
    """The pack catalog extended by the lists loaded from the user's tools; pack entries keep their order first."""
    merged = copy.deepcopy(catalog)
    for provider, entry in local.items():
        target = merged.setdefault(provider, {})
        for key in catalog_list.values():
            if isinstance(entry.get(key), list):
                target[key] = list(dict.fromkeys(target.get(key, []) + entry[key]))
    return merged


def load_defaults(root=pack):
    """Return (agents.toml as dict, config/opencode.json as dict)."""
    agents = tomllib.loads((root / "agents.toml").read_text(encoding="utf-8"))
    fragment = json.loads((root / "config" / "opencode.json").read_text(encoding="utf-8"))
    return agents, fragment


def load_settings(path=None):
    """Return (settings dict, warnings). A missing file is {}; an unreadable one warns and is {}."""
    path = path or settings_path()
    if not path.is_file():
        return {}, []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return {}, [f"{path} cannot be read ({error}); ignored"]
    if not isinstance(data, dict):
        return {}, [f"{path} is not a JSON object; ignored"]
    return data, []


def in_catalog(catalog, provider, key, value):
    allowed = catalog.get(provider, {}).get(catalog_list[key])
    return isinstance(allowed, list) and value in allowed


def check_top_level(settings, catalog):
    """Warnings for unknown top-level keys and unknown or malformed `providers`."""
    out = [f"settings key {key!r} is unknown; ignored" for key in settings if key not in top_level]
    selected = settings.get("providers")
    if selected is not None:
        if not isinstance(selected, list):
            out.append("settings providers must be a list; ignored")
        else:
            out += [f"settings providers: {p!r} is not a known provider; ignored" for p in selected if p not in providers]
    return out


def check_defaults(agents_toml, catalog):
    """Errors for pack defaults in agents.toml that the catalog lacks (an author mistake)."""
    errors = []
    for agent, tables in agents_toml.items():
        for provider, cfg in tables.items():
            if provider not in editable:
                continue
            for key in editable[provider]:
                if key in cfg and not in_catalog(catalog, provider, key, cfg[key]):
                    errors.append(f"agent {agent}: default {provider}.{key} = {cfg[key]!r} is not in config/models.toml")
    return errors


def check_opencode_defaults(fragment, catalog):
    """Warnings for defaults in config/opencode.json that the catalog lacks."""
    out = []
    for key in ("model", "small_model"):
        if key in fragment and not in_catalog(catalog, "opencode", "model", fragment[key]):
            out.append(f"opencode default {key} = {fragment[key]!r} is not in config/models.toml")
    for agent_id, cfg in fragment.get("agent", {}).items():
        for key in opencode_agent_keys:
            if key in cfg and not in_catalog(catalog, "opencode", key, cfg[key]):
                out.append(f"opencode default agent {agent_id} {key} = {cfg[key]!r} is not in config/models.toml")
    return out


def merge_agents(agents_toml, settings, catalog):
    """Return (agents.toml copy with the deviations applied, warnings)."""
    merged, out = copy.deepcopy(agents_toml), []
    section = settings.get("agents")
    if section is None:
        return merged, out
    if not isinstance(section, dict):
        return merged, ["settings agents must be an object; ignored"]
    for agent, tables in section.items():
        if agent not in merged:
            out.append(f"settings agent {agent!r} is unknown; ignored")
            continue
        if not isinstance(tables, dict):
            out.append(f"settings agent {agent}: expected an object; ignored")
            continue
        for provider, cfg in tables.items():
            if provider not in editable:
                out.append(f"settings agent {agent}: {provider!r} is not a known provider; ignored")
            elif provider not in merged[agent]:
                out.append(f"settings agent {agent}: has no {provider} in agents.toml; ignored")
            elif not isinstance(cfg, dict):
                out.append(f"settings agent {agent} {provider}: expected an object; ignored")
            else:
                for key, value in cfg.items():
                    label = f"{agent} {provider}.{key}"
                    if key not in editable[provider]:
                        out.append(f"settings agent {label} is not editable; ignored")
                    elif not isinstance(value, str):
                        out.append(f"settings agent {label}: {value!r} is not a string; ignored")
                    else:
                        if not in_catalog(catalog, provider, key, value):
                            out.append(f"agent {label} = {value!r} is not in the catalog; used anyway")
                        merged[agent][provider][key] = value
    return merged, out


def merge_opencode(fragment, settings, catalog):
    """Return (config/opencode.json copy with the `opencode` deviations applied, warnings).

    A built-in agent whose default model is the default `model` (build, plan) or `small_model` (general,
    explore, compaction, title, summary) follows the user's `model` or `small_model`, unless the user set that
    agent's model directly.
    """
    merged, out = copy.deepcopy(fragment), []
    section = settings.get("opencode")
    if section is None:
        return merged, out
    if not isinstance(section, dict):
        return merged, ["settings opencode must be an object; ignored"]

    def put(target, key, value, label, catalog_key):
        if not isinstance(value, str):
            out.append(f"settings opencode {label}: {value!r} is not a string; ignored")
            return
        if not in_catalog(catalog, "opencode", catalog_key, value):
            out.append(f"opencode {label} = {value!r} is not in the catalog; used anyway")
        target[key] = value

    for key, value in section.items():
        if key in ("model", "small_model"):
            put(merged, key, value, key, "model")
        elif key == "agent" and not isinstance(value, dict):
            out.append("settings opencode agent must be an object; ignored")
        elif key == "agent":
            for agent_id, cfg in value.items():
                if agent_id not in merged.get("agent", {}):
                    out.append(f"settings opencode agent {agent_id!r} is unknown; ignored")
                elif not isinstance(cfg, dict):
                    out.append(f"settings opencode agent {agent_id}: expected an object; ignored")
                else:
                    for k, v in cfg.items():
                        if k in opencode_agent_keys:
                            put(merged["agent"][agent_id], k, v, f"agent.{agent_id}.{k}", k)
                        else:
                            out.append(f"settings opencode agent {agent_id} key {k!r} is not editable; ignored")
        else:
            out.append(f"settings opencode key {key!r} is unknown; ignored")
    own_agents = section.get("agent") if isinstance(section.get("agent"), dict) else {}
    for session_key in ("model", "small_model"):
        if session_key not in section or merged.get(session_key) == fragment.get(session_key):
            continue
        for agent_id, cfg in merged.get("agent", {}).items():
            own = own_agents.get(agent_id)
            if isinstance(own, dict) and "model" in own:
                continue
            if fragment["agent"][agent_id].get("model") == fragment.get(session_key):
                cfg["model"] = merged[session_key]
    return merged, out


def prune_values(values, defaults):
    """Copy of values without entries equal to defaults (recursively) and without objects emptied by that."""
    if not isinstance(values, dict):
        return values
    out = {}
    for key, value in values.items():
        default = defaults.get(key) if isinstance(defaults, dict) else None
        if isinstance(value, dict) and value:
            value = prune_values(value, default)
            if not value:
                continue
        elif value == default:
            continue
        out[key] = value
    return out


def prune(settings, agents_toml, fragment):
    """Copy of settings without values equal to the defaults and without emptied objects.

    Stale entries the build only warns about (unknown agent, provider or key, wrong type) are kept as written.
    """
    out = {}
    if isinstance(settings.get("providers"), list):
        out["providers"] = settings["providers"]
    for key, defaults in (("agents", agents_toml), ("opencode", fragment)):
        kept = prune_values(settings.get(key), defaults)
        if kept and isinstance(kept, dict):
            out[key] = kept
    # Keys this module does not know are kept as the user wrote them.
    out.update({k: v for k, v in settings.items() if k not in top_level})
    return out


def mode_for(path):
    """Mode of the existing file (through symlinks), or the umask default for a new one."""
    try:
        return path.stat().st_mode & 0o7777
    except OSError:
        umask = os.umask(0)
        os.umask(umask)
        return 0o666 & ~umask


def atomic_write(path, data, mode):
    """Write data beside path and rename, so an interrupted run never leaves a truncated file."""
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    tmp = Path(name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
        tmp.chmod(mode)
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise


def write_settings(settings, path=None, root=pack):
    """Atomically write settings, dropping values equal to the pack defaults. Returns what was written."""
    path = path or settings_path()
    agents_toml, fragment = load_defaults(root)
    data = prune(settings, agents_toml, fragment)
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(path, (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode("utf-8"), mode_for(path))
    return data


def main(argv):
    if argv[:1] == ["path"] and len(argv) == 1:
        print(settings_path())
        return 0
    if argv[:1] == ["set-providers"]:
        unknown = [p for p in argv[1:] if p not in providers]
        if unknown:
            print(f"unknown provider: {', '.join(unknown)} (known: {', '.join(providers)})", file=sys.stderr)
            return 2
        path = settings_path()
        settings = {}
        if path.is_file():
            try:
                settings = json.loads(path.read_text(encoding="utf-8"))
                if not isinstance(settings, dict):
                    raise ValueError("not a JSON object")
            except (OSError, ValueError) as error:
                print(f"{path} cannot be updated ({error}); fix or remove it", file=sys.stderr)
                return 1
        settings["providers"] = list(dict.fromkeys(argv[1:]))
        path.parent.mkdir(parents=True, exist_ok=True)
        atomic_write(path, (json.dumps(settings, indent=2, ensure_ascii=False) + "\n").encode("utf-8"), mode_for(path))
        return 0
    if argv[:1] == ["get-providers"] and len(argv) == 1:
        stored = load_settings()[0].get("providers")
        if not isinstance(stored, list):
            return 3
        print("\n".join(p for p in dict.fromkeys(stored) if p in providers))
        return 0
    print("usage: ees_settings.py path | set-providers [<id>...] | get-providers", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
