"""Remove the background from an image, producing a transparent PNG.

Usage:
    python remove_bg.py <input> [output] [--matting] [--chroma-key R,G,B]

Defaults:
    output      -> "<input-stem>_nobg.png" next to the input file
    method      -> rembg (AI model) if installed, otherwise chroma-key fallback
                   (chroma-key requires --chroma-key to be specified)
"""

import argparse
import sys
from pathlib import Path


def remove_with_rembg(input_path: Path, output_path: Path, alpha_matting: bool) -> None:
    from rembg import remove
    from PIL import Image

    with Image.open(input_path) as img:
        result = remove(img, alpha_matting=alpha_matting)
        result.save(output_path)


def remove_with_chroma_key(input_path: Path, output_path: Path, key_rgb: tuple[int, int, int], tolerance: int = 40) -> None:
    from PIL import Image

    img = Image.open(input_path).convert("RGBA")
    pixels = img.getdata()
    kr, kg, kb = key_rgb

    new_pixels = [
        (r, g, b, 0) if abs(r - kr) <= tolerance and abs(g - kg) <= tolerance and abs(b - kb) <= tolerance else (r, g, b, a)
        for (r, g, b, a) in pixels
    ]
    img.putdata(new_pixels)
    img.save(output_path)


def parse_rgb(value: str) -> tuple[int, int, int]:
    parts = [int(p.strip()) for p in value.split(",")]
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("Expected R,G,B e.g. 255,255,255")
    return (parts[0], parts[1], parts[2])


def main() -> int:
    parser = argparse.ArgumentParser(description="Remove image background -> transparent PNG")
    parser.add_argument("input", type=Path, help="Path to the source image")
    parser.add_argument("output", type=Path, nargs="?", default=None, help="Path for the output PNG")
    parser.add_argument("--matting", action="store_true", help="Use alpha matting for cleaner edges (rembg only, slower)")
    parser.add_argument("--chroma-key", type=parse_rgb, default=None, help="Force chroma-key removal for this R,G,B color")
    args = parser.parse_args()

    input_path: Path = args.input
    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 1

    output_path = args.output or input_path.with_name(f"{input_path.stem}_nobg.png")

    if args.chroma_key is not None:
        remove_with_chroma_key(input_path, output_path, args.chroma_key)
        print(f"Chroma-key removed ({args.chroma_key}) -> {output_path}")
        return 0

    try:
        remove_with_rembg(input_path, output_path, args.matting)
        print(f"Background removed (rembg) -> {output_path}")
        return 0
    except ImportError:
        print(
            "rembg is not installed and no --chroma-key color was given.\n"
            "Install it with: pip install rembg[cpu] pillow\n"
            "Or specify a solid background color to strip: --chroma-key 255,255,255",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
