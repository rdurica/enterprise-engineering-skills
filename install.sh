#!/usr/bin/env bash
# Link this pack into Claude Code: ~/.claude/skills/<skill> and ~/.claude/agents/<agent>.md.
# Re-run after adding or renaming a skill or agent; `git pull` alone updates existing links.
set -euo pipefail

pack="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
claude_dir="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
dry_run=0
[[ "${1:-}" == "--dry-run" ]] && dry_run=1

link() {
  local src="$1" dest="$2"
  if [[ -L "$dest" ]]; then
    local current
    current="$(readlink -f "$dest" || true)"
    if [[ "$current" == "$src" ]]; then
      echo "ok      $dest"
      return
    fi
    # Replace only links into this pack or dangling links, never someone else's skill.
    if [[ "$current" == "$pack"/* || ! -e "$dest" ]]; then
      echo "relink  $dest -> $src"
    else
      echo "skip    $dest (links to $current; remove it manually to use this pack)" >&2
      return
    fi
  elif [[ -e "$dest" ]]; then
    echo "skip    $dest (real file or directory; remove it manually to use this pack)" >&2
    return
  else
    echo "link    $dest -> $src"
  fi
  (( dry_run )) || ln -sfn "$src" "$dest"
}

(( dry_run )) || mkdir -p "$claude_dir/skills" "$claude_dir/agents"

for skill in "$pack"/skills/*/; do
  skill="${skill%/}"
  [[ -f "$skill/SKILL.md" ]] || continue
  link "$skill" "$claude_dir/skills/$(basename "$skill")"
done

for agent in "$pack"/agents/*.md; do
  link "$agent" "$claude_dir/agents/$(basename "$agent")"
done

# Personal, gitignored skills live in skills/personal/<name>/.
if [[ -d "$pack/skills/personal" ]]; then
  for skill in "$pack"/skills/personal/*/; do
    skill="${skill%/}"
    [[ -f "$skill/SKILL.md" ]] || continue
    link "$skill" "$claude_dir/skills/$(basename "$skill")"
  done
fi

echo "Done. Start a new Claude Code session and check /skills and /agents."
