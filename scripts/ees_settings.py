"""Shared catalog and user-settings logic for build-agents, opencode-config and the setup server.

Settings live in ${XDG_CONFIG_HOME:-~/.config}/enterprise-engineering-skills/settings.json and hold only
deviations from the pack defaults (agents.toml, config/opencode.json): an absent key means the current
default. Merging is per key, so a `codex.model` deviation leaves the default `codex.effort` alone.

    {"providers": ["claude", "codex"],
     "agents": {"<agent>": {"<provider>": {"model": ..., "effort"|"variant": ...}}},
     "opencode": {"model": ..., "small_model": ..., "agent": {"<id>": {"model": ..., "variant": ...}}}}

Unknown agents, providers, keys and values of the wrong type warn and are ignored; a value outside the
catalog warns and is still used. Warnings are plain strings, printed by callers as `warn    <text>`.

API: settings_path, load_catalog, load_defaults, load_settings, merge_agents, merge_opencode,
check_defaults, check_opencode_defaults, check_top_level, prune, write_settings, atomic_write, warn.

CLI (used by install.sh, which must only write JSON through Python):
    python3 scripts/ees_settings.py path                    print the settings.json path
    python3 scripts/ees_settings.py set-providers [<id>...] rewrite only `providers`, keep every other key
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
providers = ("claude", "codex", "cursor", "opencode", "pi")
# Editable keys per provider (others, such as tools or color, stay in agents.toml) and their catalog list.
editable = {
    "claude": ("model", "effort"),
    "codex": ("model", "effort"),
    "cursor": ("model",),
    "opencode": ("model", "variant"),
    "pi": ("model", "variant"),
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
    """Return (config/opencode.json copy with the `opencode` deviations applied, warnings)."""
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
        elif key == "agent" and isinstance(value, dict):
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
    return merged, out


def prune(settings, agents_toml, fragment):
    """Copy of settings without values equal to the defaults and without emptied objects."""
    out = {}
    if isinstance(settings.get("providers"), list):
        out["providers"] = settings["providers"]
    agents = {}
    for agent, tables in (settings.get("agents") or {}).items():
        for provider, cfg in (tables or {}).items():
            default = agents_toml.get(agent, {}).get(provider, {})
            kept = {k: v for k, v in cfg.items() if default.get(k) != v}
            if kept:
                agents.setdefault(agent, {})[provider] = kept
    if agents:
        out["agents"] = agents
    section = settings.get("opencode") or {}
    oc = {k: v for k, v in section.items() if k in ("model", "small_model") and fragment.get(k) != v}
    oc_agents = {}
    for agent_id, cfg in (section.get("agent") or {}).items():
        kept = {k: v for k, v in cfg.items() if fragment.get("agent", {}).get(agent_id, {}).get(k) != v}
        if kept:
            oc_agents[agent_id] = kept
    if oc_agents:
        oc["agent"] = oc_agents
    if oc:
        out["opencode"] = oc
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
    print("usage: ees_settings.py path | set-providers [<id>...]", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
