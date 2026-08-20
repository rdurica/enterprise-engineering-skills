#!/usr/bin/env bash
# Real-ESRGAN 4× upscale helper for img-upscale skill.
# Usage: upscale.sh <input> <output.png> [model]
# Default model: realesrgan-x4plus
set -euo pipefail

IN="${1:?usage: upscale.sh <input> <output.png> [model]}"
OUT="${2:?usage: upscale.sh <input> <output.png> [model]}"
MODEL="${3:-realesrgan-x4plus}"

ESR_DIR="${REALESRGAN_DIR:-$HOME/.local/share/realesrgan}"
ESR="$ESR_DIR/realesrgan-ncnn-vulkan"
MODELDIR="$ESR_DIR/models"

if [[ ! -x "$ESR" ]]; then
  echo "Real-ESRGAN not found at $ESR" >&2
  echo "Install per ~/.cursor/skills/images/img-upscale/SKILL.md" >&2
  exit 1
fi

mkdir -p "$(dirname "$OUT")"
cd "$ESR_DIR"
"$ESR" -i "$IN" -o "$OUT" -n "$MODEL" -s 4 -f png -v -m "$MODELDIR"
identify "$OUT" 2>/dev/null || true
