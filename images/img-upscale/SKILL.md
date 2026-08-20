---
name: img-upscale
description: >-
  Upscales images with Real-ESRGAN 4× (realesrgan-x4plus) and applies a soft,
  gentle finish — not crunchy/oversharp. Use when the user asks to upscale,
  Real-ESRGAN, 4x, zvětšit obrázek, doostřit wallpaper bez přestřelené ostrosti,
  or invokes /img-upscale.
---

# Image Upscale (Real-ESRGAN 4×, soft finish)

## Goal

Take a source image (often AI-generated ~1536px) → **Real-ESRGAN 4×** → optional
target crop/resize → **soft** final look. Prefer gentle clarity over harsh
sharpening.

## Tooling

| Item | Path / value |
|------|----------------|
| Binary | `~/.local/share/realesrgan/realesrgan-ncnn-vulkan` |
| Models dir | `~/.local/share/realesrgan/models` |
| Default model | `realesrgan-x4plus` |
| Default scale | `4` |
| Helper | `scripts/upscale.sh` in this skill |

If the binary is missing, install once (needs user approval for download):

```bash
DIR="$HOME/.local/share/realesrgan"
mkdir -p "$DIR" && cd "$DIR"
curl -L --fail -o realesrgan.zip \
  "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-ubuntu.zip"
unzip -o realesrgan.zip
chmod +x realesrgan-ncnn-vulkan
```

Prefer GPU (Vulkan). AMD/NVIDIA both work with the ncnn-vulkan build.

## Workflow

1. Confirm input path and desired output path/size.
2. Run Real-ESRGAN 4× with `realesrgan-x4plus` (photoreal default).
3. If a specific canvas is needed (e.g. wallpaper `6400×1440`):
   - Crop from the **native x4 pixels** first (preserve detail).
   - Only then Lanczos-resize to the exact target (small scale only).
4. Apply the **soft finish** (below). Do **not** pile on UnsharpMask + high Sharpness.
5. Verify with `identify` and a quick visual check of a detail crop.

### Upscale command

```bash
ESR="$HOME/.local/share/realesrgan/realesrgan-ncnn-vulkan"
MODELDIR="$HOME/.local/share/realesrgan/models"

"$ESR" -i "$IN" -o "$OUT_X4" \
  -n realesrgan-x4plus -s 4 -f png -v \
  -m "$MODELDIR"
```

Or:

```bash
~/.cursor/skills/images/img-upscale/scripts/upscale.sh "$IN" "$OUT_X4"
```

### Soft finish (default — “jemné, ne moc ostré”)

After x4 (and any crop/resize to target):

```bash
magick "$SRC" \
  -gaussian-blur 0x0.85 \
  -sigmoidal-contrast 1.2x50% \
  -modulate 100,104,100 \
  -strip PNG24:"$OUT"
```

Defaults that worked well:

- light gaussian blur `0x0.85`
- mild contrast via sigmoidal `1.2x50%`
- slight saturation bump `modulate 100,104,100`
- **no** aggressive `-unsharp`, **no** `ImageEnhance.Sharpness` > ~1.1

### When the user wants more / less soft

| Request | Adjust |
|---------|--------|
| Soft / jemné (default) | blur `0x0.85`, no unsharp |
| A bit clearer | blur `0x0.5`, optional UnsharpMask `radius=0.9 percent=50 threshold=3` |
| Too soft / rozmazané | drop blur; keep mild contrast only |
| Too sharp / moc ostré | restore blur `0x0.85`; remove unsharp |

## Wallpaper / multi-monitor notes

- Prefer **one continuous** upscaled image over stitched side panels (seams show).
- For ultrawide targets: crop a native band with the right aspect from the x4 file, then small Lanczos to exact size.
- Keep important subjects (moon, path, focal object) inside the crop — detect/bias vertically before finishing.
- GNOME multi-monitor: `picture-options` = `spanned`, exact virtual size (e.g. `6400×1440`).

## Anti-patterns

- Do not “fix” softness with heavy UnsharpMask + Sharpness stacking — that looks crunchy and worse.
- Do not upscale a full desktop by stretching a small image with `!` geometry.
- Do not blend separate left/center/right generations unless the user accepts visible seams.
- Anime content: may use `realesrgan-x4plus-anime`; default stays `realesrgan-x4plus`.

## Checklist

```
- [ ] Real-ESRGAN binary available
- [ ] x4 output written and identified
- [ ] Target crop/resize done from native x4 when needed
- [ ] Soft finish applied (unless user asked for sharper)
- [ ] Final path + dimensions verified
```
