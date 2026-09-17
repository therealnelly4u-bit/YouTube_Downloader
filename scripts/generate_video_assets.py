#!/usr/bin/env python3
"""Build reusable thumbnail and edit-package assets from a supplied source image.

The script intentionally does not invent footage.  It packages a creator-owned
photo or video frame into a mobile-safe SVG thumbnail, an SRT caption track, a
JSON edit brief, and an optional FFmpeg command.  This keeps the generated
assets usable for the challenge and pet references without shipping unrelated
placeholder imagery.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from textwrap import dedent


@dataclass(frozen=True)
class Scene:
    start: float
    end: float
    visual: str
    caption: str


VIDEO_TYPES = {
    "challenge": {
        "default_title": "WHO MAKES THE SHOT?",
        "description": "Eight friends. One mini hoop. Who lands the next shot?",
        "scenes": [
            Scene(0, 2, "Show all numbered players and the hoop.", "Pick your winner!"),
            Scene(2, 5, "Punch in on the first throw.", "Player 1 starts us off."),
            Scene(5, 10, "Show the closest attempts and reactions.", "Who has the best shot?"),
            Scene(10, 14, "Replay the winning moment.", "Comment the number you picked!"),
        ],
    },
    "cat": {
        "default_title": "CAT HAS A NEW LOOK",
        "description": "A calm cat gets a tiny accessory and steals the whole video.",
        "scenes": [
            Scene(0, 2, "Reveal the cat looking directly at camera.", "Wait for the reveal…"),
            Scene(2, 5, "Show the tiny headband detail.", "New look unlocked."),
            Scene(5, 9, "Hold for the cat's reaction.", "Does he approve?"),
            Scene(9, 13, "End on the strongest close-up.", "Rate the look from 1–10."),
        ],
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a thumbnail and edit package from a creator-owned image."
    )
    parser.add_argument("source_image", type=Path, help="Local JPEG, PNG, or WebP image to feature.")
    parser.add_argument("--type", choices=tuple(VIDEO_TYPES), default="challenge")
    parser.add_argument("--output-dir", type=Path, default=Path("assets/generated"))
    parser.add_argument("--slug", default=None, help="Output filename prefix; defaults to the video type.")
    parser.add_argument("--title", default=None, help="Thumbnail headline and metadata title.")
    parser.add_argument("--cta", default=None, help="Bottom call-to-action text.")
    return parser.parse_args()


def escape(value: str) -> str:
    return html.escape(value, quote=True)


def image_data_uri(source: Path) -> str:
    mime_type, _ = mimetypes.guess_type(source.name)
    if mime_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise ValueError("source_image must be a JPEG, PNG, or WebP file")
    payload = base64.b64encode(source.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{payload}"


def thumbnail_svg(image_uri: str, title: str, cta: str) -> str:
    return dedent(
        f"""\
        <svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" role="img" aria-labelledby="title desc">
          <title id="title">{escape(title)} thumbnail</title>
          <desc id="desc">Creator-supplied image with a high-contrast video headline and call to action.</desc>
          <defs>
            <linearGradient id="shade" x1="0" x2="1" y1="0" y2="0">
              <stop offset="0" stop-color="#080b16" stop-opacity=".94"/>
              <stop offset=".56" stop-color="#080b16" stop-opacity=".44"/>
              <stop offset="1" stop-color="#080b16" stop-opacity=".05"/>
            </linearGradient>
            <filter id="shadow"><feDropShadow dx="0" dy="8" stdDeviation="7" flood-opacity=".65"/></filter>
          </defs>
          <image href="{image_uri}" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
          <rect width="1280" height="720" fill="url(#shade)"/>
          <rect x="55" y="52" width="150" height="44" rx="22" fill="#ff3d74"/>
          <text x="80" y="83" font-family="Arial, sans-serif" font-size="24" font-weight="800" fill="#fff">SHORTS</text>
          <text x="64" y="315" font-family="Impact, Arial Black, sans-serif" font-size="92" fill="#fff" stroke="#000" stroke-width="7" paint-order="stroke" filter="url(#shadow)">{escape(title)}</text>
          <rect x="64" y="560" width="530" height="88" rx="20" fill="#ffcc26"/>
          <text x="96" y="618" font-family="Arial, sans-serif" font-size="38" font-weight="800" fill="#10131f">{escape(cta)}</text>
        </svg>
        """
    )


def srt(scenes: list[Scene]) -> str:
    def stamp(seconds: float) -> str:
        return f"00:00:{int(seconds):02},000"

    return "\n".join(
        f"{index}\n{stamp(scene.start)} --> {stamp(scene.end)}\n{scene.caption}\n"
        for index, scene in enumerate(scenes, start=1)
    )


def main() -> int:
    args = parse_args()
    if not args.source_image.is_file():
        raise SystemExit(f"Source image not found: {args.source_image}")

    package = VIDEO_TYPES[args.type]
    slug = args.slug or args.type
    title = args.title or package["default_title"]
    cta = args.cta or "COMMENT YOUR PICK"
    scenes: list[Scene] = package["scenes"]
    image_uri = image_data_uri(args.source_image)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    thumbnail = args.output_dir / f"{slug}-thumbnail.svg"
    captions = args.output_dir / f"{slug}-captions.srt"
    manifest = args.output_dir / f"{slug}-edit-brief.json"
    render_helper = args.output_dir / f"{slug}-render-video.sh"
    thumbnail.write_text(thumbnail_svg(image_uri, title, cta), encoding="utf-8")
    captions.write_text(srt(scenes), encoding="utf-8")
    manifest.write_text(
        json.dumps(
            {
                "title": title,
                "description": package["description"],
                "source_image": str(args.source_image),
                "format": "vertical short",
                "duration_seconds": scenes[-1].end,
                "scenes": [asdict(scene) for scene in scenes],
            },
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    render_helper.write_text(
        dedent(
            f"""\
            #!/usr/bin/env bash
            set -euo pipefail
            # Requires FFmpeg. Uses the supplied image as a 9:16 video backdrop.
            ffmpeg -y -loop 1 -t {scenes[-1].end:g} -i {args.source_image} \\
              -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,subtitles={captions.name}" \\
              -c:v libx264 -pix_fmt yuv420p -movflags +faststart {slug}.mp4
            """
        ),
        encoding="utf-8",
    )
    render_helper.chmod(0o755)
    print(f"Generated thumbnail: {thumbnail}")
    print(f"Generated captions: {captions}")
    print(f"Generated edit brief: {manifest}")
    print(f"Generated FFmpeg helper: {render_helper}")
    if shutil.which("ffmpeg") is None:
        print("FFmpeg is not installed; use the generated helper where FFmpeg is available.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
