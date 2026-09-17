#!/usr/bin/env python3
"""Optimize local image assets for web publishing.

The script accepts one or more files/directories, recursively finds common raster
and SVG image formats, and writes optimized copies to an output directory. If
Pillow is installed, raster images can be resized, stripped of metadata, and
converted to WebP. SVG files are whitespace-minified without extra dependencies.
Without Pillow, the script still provides a safe dry-run/copy workflow so teams
can inventory image assets in minimal environments.
"""

from __future__ import annotations

import argparse
import importlib.util
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff", ".svg"}

if importlib.util.find_spec("PIL") is None:
    Image = None
else:
    Image = importlib.import_module("PIL.Image")


@dataclass(frozen=True)
class OptimizationResult:
    source: Path
    destination: Path
    original_bytes: int
    optimized_bytes: int
    action: str

    @property
    def saved_bytes(self) -> int:
        return max(self.original_bytes - self.optimized_bytes, 0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Optimize images for a website or social media asset folder."
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        type=Path,
        help="Image files or directories to process recursively.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("optimized-images"),
        help="Directory where optimized images will be written.",
    )
    parser.add_argument(
        "--max-width",
        type=int,
        default=1280,
        help="Resize images wider than this value while preserving aspect ratio.",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=82,
        help="Compression quality from 1 to 100 for JPEG/WebP outputs.",
    )
    parser.add_argument(
        "--format",
        choices=("original", "webp"),
        default="webp",
        help="Keep original formats or convert supported images to WebP.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned work without writing files.",
    )
    return parser.parse_args()


def iter_images(paths: Iterable[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_dir():
            for candidate in path.rglob("*"):
                if candidate.is_file() and candidate.suffix.lower() in SUPPORTED_EXTENSIONS:
                    yield candidate
        elif path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield path
        else:
            print(f"Skipping unsupported path: {path}", file=sys.stderr)


def destination_for(source: Path, output_dir: Path, output_format: str) -> Path:
    if source.suffix.lower() == ".svg":
        suffix = ".svg"
    else:
        suffix = ".webp" if output_format == "webp" else source.suffix.lower()
    return output_dir / f"{source.stem}{suffix}"


def optimize_with_pillow(
    source: Path,
    destination: Path,
    *,
    max_width: int,
    quality: int,
    output_format: str,
) -> OptimizationResult:
    original_bytes = source.stat().st_size
    destination.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(source) as image:  # type: ignore[union-attr]
        image_format = "WEBP" if output_format == "webp" else (image.format or "JPEG")
        working = image.copy()

        if working.mode in {"RGBA", "P"} and image_format in {"JPEG", "JPG"}:
            working = working.convert("RGB")

        if working.width > max_width:
            ratio = max_width / working.width
            next_height = max(1, round(working.height * ratio))
            working = working.resize((max_width, next_height))

        save_kwargs: dict[str, object] = {"optimize": True}
        if image_format in {"JPEG", "JPG", "WEBP"}:
            save_kwargs["quality"] = quality
        if image_format == "WEBP":
            save_kwargs["method"] = 6

        working.save(destination, format=image_format, **save_kwargs)

    optimized_bytes = destination.stat().st_size
    return OptimizationResult(source, destination, original_bytes, optimized_bytes, "optimized")



def optimize_svg(source: Path, destination: Path) -> OptimizationResult:
    original_bytes = source.stat().st_size
    destination.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        line.strip()
        for line in source.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
    optimized_bytes = destination.stat().st_size
    return OptimizationResult(source, destination, original_bytes, optimized_bytes, "optimized")

def copy_without_pillow(source: Path, destination: Path, dry_run: bool) -> OptimizationResult:
    original_bytes = source.stat().st_size
    if not dry_run:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        optimized_bytes = destination.stat().st_size
    else:
        optimized_bytes = original_bytes
    return OptimizationResult(source, destination, original_bytes, optimized_bytes, "copied")


def print_result(result: OptimizationResult) -> None:
    saved_kb = result.saved_bytes / 1024
    original_kb = result.original_bytes / 1024
    optimized_kb = result.optimized_bytes / 1024
    print(
        f"{result.action}: {result.source} -> {result.destination} "
        f"({original_kb:.1f} KB to {optimized_kb:.1f} KB, saved {saved_kb:.1f} KB)"
    )


def main() -> int:
    args = parse_args()
    images = sorted(set(iter_images(args.inputs)))

    if not images:
        print("No supported image files found.", file=sys.stderr)
        return 1

    if args.quality < 1 or args.quality > 100:
        print("--quality must be between 1 and 100.", file=sys.stderr)
        return 2

    if args.max_width < 1:
        print("--max-width must be greater than 0.", file=sys.stderr)
        return 2

    raster_images = [image for image in images if image.suffix.lower() != ".svg"]
    if Image is None and args.format == "webp" and raster_images:
        print(
            "Pillow is not installed; raster files will be copied with original formats. "
            "Install Pillow to resize or convert rasters to WebP.",
            file=sys.stderr,
        )

    total_original = 0
    total_optimized = 0

    for source in images:
        output_format = args.format if Image is not None else "original"
        destination = destination_for(source, args.output_dir, output_format)

        if args.dry_run:
            result = OptimizationResult(
                source, destination, source.stat().st_size, source.stat().st_size, "planned"
            )
        elif source.suffix.lower() == ".svg":
            result = optimize_svg(source, destination)
        elif Image is None:
            result = copy_without_pillow(source, destination, args.dry_run)
        else:
            result = optimize_with_pillow(
                source,
                destination,
                max_width=args.max_width,
                quality=args.quality,
                output_format=args.format,
            )

        total_original += result.original_bytes
        total_optimized += result.optimized_bytes
        print_result(result)

    if not args.dry_run:
        total_saved = max(total_original - total_optimized, 0)
        print(f"Total saved: {total_saved / 1024:.1f} KB")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
