---
name: remove-image-background
description: 'Remove the background from an image and produce a transparent PNG cutout. Use when the user asks to "remove background", "cut out", "make transparent", "nobg", or mentions Photoroom/remove.bg-style image processing for PNG/JPG assets.'
argument-hint: '<input-image-path> [output-path]'
---

# Remove Image Background

Produces a transparent-background PNG cutout from a photo, using the local
`rembg` AI model (no paid API, no upload of images to a third-party service).

## When to Use

- User wants a subject (person, object, couple photo, etc.) cut out with a
  transparent background, similar to Photoroom/remove.bg exports already used in
  this project (`*-Photoroom.png`, `*_nobg.png`).
- User wants to prep a new photo for embedding into `wedding-card.html` as a
  cutout image.

## Prerequisites

Requires Python 3.9+ and the `rembg` package (bundles an ONNX background-removal
model, runs fully offline after first download).

```powershell
pip install rembg[cpu] pillow
```

First run downloads a small model file (~40–170MB depending on model) to
`~/.u2net/` — this needs internet access once, then works offline.

## Procedure

1. **Confirm input file exists** and note its path.
2. **Run the removal script**: [scripts/remove_bg.py](./scripts/remove_bg.py)
   ```powershell
   python ".claude/skills/remove-image-background/scripts/remove_bg.py" "<input.jpg>" "<output_nobg.png>"
   ```
   Or use the PowerShell wrapper: [scripts/remove_bg.ps1](./scripts/remove_bg.ps1)
   ```powershell
   ./.claude/skills/remove-image-background/scripts/remove_bg.ps1 -InputPath "<input.jpg>" -OutputPath "<output_nobg.png>"
   ```
3. **If no output path is given**, the script defaults to
   `<input-name>_nobg.png` next to the source file — matching this repo's existing
   naming convention.
4. **Verify** the result has a transparent background by opening the PNG (checkered
   preview in most editors/VS Code image viewer confirms alpha transparency).
5. **Optional cleanup**: for stray semi-transparent fringe pixels, rerun with the
   `alpha_matting` option enabled (see script `--matting` flag) for a cleaner edge —
   slower but higher quality, best for hair/fine edges.

## Embedding into the wedding card

Per [CLAUDE.md](../../../CLAUDE.md), don't hand-embed new images — base64-encode
and splice them into `wedding-card.html` with a small Python script following the
existing pattern in that file. That is a separate step from background removal;
ask the user if they also want the cutout embedded once it's produced.

## Notes

- Works best on photos with a reasonably distinct subject (portrait/product shots).
- For simple flat/solid-color backgrounds, chroma-key removal is faster — the
  script falls back to this if `rembg` isn't installed (see `--chroma-key`
  option, requires specifying the background color to strip).
- This is a local, offline tool — no images are uploaded anywhere.
