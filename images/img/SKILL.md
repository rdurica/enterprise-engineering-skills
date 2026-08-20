---
name: img
description: Generate or regenerate image assets using the built-in image API. Use when the user invokes /img, asks to create images, generate pictures, regenerate graphics, make visuals, posters, thumbnails, social media images, promo assets, or says to call/provolat the image API.
---

# Image Generation

## Core Rule

Use the `GenerateImage` tool for image assets. Do not hand-build production images with SVG, HTML, canvas, screenshots, ImageMagick composition, or template scripts unless the user explicitly asks for editable deterministic source files.

## Workflow

1. Read the target brief or surrounding content first: post text, campaign plan, existing images, brand assets, desired filenames, dimensions, and destination folder.
2. Use existing good outputs as `reference_image_paths` when visual consistency matters.
3. Prefer image prompts with no embedded text by default. If the user explicitly asks for text in the image, include it.
4. State constraints directly in the prompt:
   - `no words`
   - `no letters`
   - `no numbers`
   - `no readable UI text`
   - `no watermark`
   - `no captions`
5. Generate the image with `GenerateImage`.
6. Copy or move the generated file into the user-requested destination and filename.
7. Verify the final file exists and inspect dimensions with an image tool when available.
8. Visually inspect at least representative outputs before saying the work is done.

## Prompt Pattern

Use concrete, art-directed prompts:

```text
Premium [target channel] image for [product/context], theme: [specific message].
Composition: [main subject], [supporting visual elements], [mood].
Style: [brand palette], [lighting], [medium], [quality bar].
IMPORTANT: no words, no letters, no numbers, no readable UI text, no watermark, no captions.
```

## Text In Images

When the user asks for text in the image:

1. For exact wording, Czech diacritics, brand names, prices, dates, URLs, or short slogans, prefer generating a clean background with `GenerateImage` and then adding the exact text locally as an overlay.
2. Use the image API for text only when the user accepts approximate typography or when the text is decorative and not mission-critical.
3. Keep text short and readable. Social media images work best with one headline and optionally one short subline.
4. Verify the final rendered text visually before saying the work is done.

## Replacement Work

When regenerating existing assets:

1. Keep the original filenames unless the user asks otherwise.
2. Preserve existing good images and overwrite only the requested bad ones.
3. If a prior generated image failed because of text, remove text from the next prompt instead of trying to fix typography manually.
4. If a prior generated image failed because of a bad object, describe the object more specifically in the next prompt and use good references.

## Notes

- For social media campaigns, text belongs in the post body unless the user requests poster text or cover text.
- Use brand/logo references when available, but avoid relying on generated images to reproduce exact logos unless the user accepts approximate branding.
- If exact dimensions are required and the image API returns a different size, crop/resize only after generation.
