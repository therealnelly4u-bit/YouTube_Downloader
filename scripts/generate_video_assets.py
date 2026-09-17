#!/usr/bin/env python3
"""Generate short-form video planning assets and thumbnails.

This script uses only the Python standard library so it works in constrained
CI/dev environments. It creates a polished SVG thumbnail, an animated vertical
SVG video mock, captions, metadata, and an optional FFmpeg helper script that can
be used when FFmpeg is available locally.
"""

from __future__ import annotations

import argparse
import html
import json
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from textwrap import dedent

PLATFORM_NAMES = [
    "TypeSprint Studio",
    "KeyFlow Academy",
    "SwiftKeys Lab",
    "Accuracy Arcade",
]

HASHTAGS = [
    "#shorts",
    "#funny",
    "#cat",
    "#cute",
    "#viral",
    "#moments",
    "#catbehavior",
    "#orangecat",
    "#pets",
]

TAGS = [
    "cat shorts",
    "funny cat",
    "orange tabby",
    "cute cat video",
    "cat interrupts work",
    "pet comedy",
    "viral cat moments",
    "cat behavior",
]


@dataclass(frozen=True)
class Scene:
    start: float
    end: float
    visual: str
    caption: str


SCENES = [
    Scene(0, 3, "Glowing-eye orange tabby locks onto the workspace.", "My cat has one job…"),
    Scene(3, 8, "Cat leaps toward a chair beside the desk.", "Reach for attention before I can work."),
    Scene(8, 14, "Keyboard and laptop are blocked by paws.", "Every time I open my laptop, Mac clocks in."),
    Scene(14, 22, "Confident cat close-up with boss-energy pose.", "No meetings. No deadlines. Just full-time chaos."),
    Scene(22, 31, "Cat sits proudly like an employee of the month.", "Somehow, he still gets employee of the month."),
    Scene(31, 40, "Freeze frame with bold thumbnail text.", "Would your pet get hired for this job?"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate video and thumbnail assets.")
    parser.add_argument("--output-dir", type=Path, default=Path("assets/generated"))
    parser.add_argument("--slug", default="cat-short", help="Filename prefix for generated assets.")
    parser.add_argument("--platform-name", default=PLATFORM_NAMES[0], help="Typing platform name to include in metadata.")
    parser.add_argument("--tagline", default="Master Speed. Improve Accuracy.")
    parser.add_argument("--thumbnail-title", default="MY CAT HAS ONE JOB…")
    return parser.parse_args()


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def generate_thumbnail(title: str) -> str:
    words = title.replace("…", "...").split()
    line_one = " ".join(words[:2]) if len(words) > 2 else title
    line_two = " ".join(words[2:]) if len(words) > 2 else ""
    return dedent(
        f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" role="img" aria-labelledby="title desc">
          <title id="title">{esc(title)} YouTube thumbnail</title>
          <desc id="desc">Orange tabby cat jumping toward a chair with bold text reading {esc(title)}.</desc>
          <defs>
            <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0" stop-color="#fff7d6"/>
              <stop offset="0.55" stop-color="#ffcf4a"/>
              <stop offset="1" stop-color="#24140a"/>
            </linearGradient>
            <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
              <feDropShadow dx="0" dy="10" stdDeviation="8" flood-color="#000" flood-opacity="0.55"/>
            </filter>
            <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
              <feGaussianBlur stdDeviation="10" result="blur"/>
              <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
          </defs>
          <rect width="1280" height="720" fill="url(#bg)"/>
          <path d="M0 560 C230 480 340 640 520 540 C760 410 920 520 1280 390 L1280 720 L0 720 Z" fill="#fff" opacity="0.35"/>
          <g filter="url(#shadow)">
            <rect x="72" y="62" width="515" height="138" rx="24" fill="#111"/>
            <rect x="72" y="207" width="570" height="152" rx="24" fill="#111"/>
            <text x="104" y="168" font-family="Impact, Arial Black, sans-serif" font-size="92" fill="#fff" stroke="#000" stroke-width="8" paint-order="stroke">{esc(line_one)}</text>
            <text x="104" y="318" font-family="Impact, Arial Black, sans-serif" font-size="96" fill="#ffe432" stroke="#000" stroke-width="8" paint-order="stroke">{esc(line_two)}</text>
            <path d="M95 603 L555 603" stroke="#df1414" stroke-width="104" stroke-linecap="round" opacity="0.95"/>
            <text x="92" y="590" font-family="Impact, Arial Black, sans-serif" font-size="70" fill="#fff" stroke="#000" stroke-width="7" paint-order="stroke">REACH FOR</text>
            <text x="92" y="678" font-family="Impact, Arial Black, sans-serif" font-size="82" fill="#ffe432" stroke="#000" stroke-width="8" paint-order="stroke">ATTENTION!</text>
          </g>
          <g transform="translate(720 110) rotate(8)" filter="url(#glow)">
            <ellipse cx="255" cy="250" rx="250" ry="145" fill="#d87922"/>
            <ellipse cx="80" cy="210" rx="118" ry="95" fill="#d87922"/>
            <path d="M30 112 L66 24 L104 124 Z" fill="#d87922"/>
            <path d="M106 118 L158 28 L168 143 Z" fill="#d87922"/>
            <path d="M-12 366 C58 312 130 306 190 356" stroke="#d87922" stroke-width="54" fill="none" stroke-linecap="round"/>
            <circle cx="42" cy="198" r="15" fill="#111"/>
            <circle cx="112" cy="198" r="15" fill="#111"/>
            <path d="M66 231 Q82 246 101 231" stroke="#421f0a" stroke-width="8" fill="none" stroke-linecap="round"/>
            <path d="M220 150 C275 190 325 190 410 160" stroke="#a64d16" stroke-width="15" fill="none" opacity="0.55"/>
            <path d="M228 230 C288 265 362 262 450 220" stroke="#a64d16" stroke-width="15" fill="none" opacity="0.5"/>
            <rect x="105" y="382" width="360" height="94" rx="30" fill="#151515"/>
          </g>
          <path d="M447 435 C520 452 585 432 626 382" stroke="#e41414" stroke-width="24" fill="none" stroke-linecap="round"/>
          <path d="M624 382 L596 445 L565 395 Z" fill="#e41414"/>
        </svg>
        """
    ).strip() + "\n"


def generate_animated_svg(title: str) -> str:
    caption_layers = []
    for index, scene in enumerate(SCENES):
        begin = scene.start
        duration = scene.end - scene.start
        caption_layers.append(
            f'''<text id="caption-{index}" class="caption" x="540" y="1540">{esc(scene.caption)}
                 <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.92;1" begin="{begin}s" dur="{duration}s" fill="remove"/>
               </text>'''
        )
    captions = "\n".join(caption_layers)
    return dedent(
        f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920" role="img" aria-labelledby="title desc">
          <title id="title">Animated short video mock: {esc(title)}</title>
          <desc id="desc">A 40-second vertical animated SVG storyboard for a funny orange cat short.</desc>
          <style>
            .caption {{ font: 800 58px Arial, sans-serif; fill: #fff; stroke: #000; stroke-width: 10px; paint-order: stroke; text-anchor: middle; opacity: 0; }}
            .headline {{ font: 900 90px Impact, Arial Black, sans-serif; fill: #ffe432; stroke: #000; stroke-width: 12px; paint-order: stroke; text-anchor: middle; }}
            .cat {{ animation: bounce 2s ease-in-out infinite alternate; transform-origin: 540px 780px; }}
            .glow {{ animation: pulse 1.25s ease-in-out infinite alternate; }}
            .bar {{ animation: progress 40s linear forwards; }}
            @keyframes bounce {{ from {{ transform: translateY(0); }} to {{ transform: translateY(-48px); }} }}
            @keyframes pulse {{ from {{ opacity: .35; }} to {{ opacity: 1; }} }}
            @keyframes progress {{ from {{ width: 0; }} to {{ width: 880px; }} }}
          </style>
          <rect width="1080" height="1920" fill="#11131d"/>
          <circle cx="920" cy="230" r="270" fill="#ffcf4a" opacity="0.25"/>
          <text class="headline" x="540" y="210">{esc(title)}</text>
          <g class="cat">
            <ellipse cx="560" cy="800" rx="290" ry="210" fill="#d87922"/>
            <circle cx="405" cy="670" r="145" fill="#d87922"/>
            <path d="M300 565 L352 420 L426 575 Z" fill="#d87922"/>
            <path d="M430 560 L510 420 L516 600 Z" fill="#d87922"/>
            <circle class="glow" cx="360" cy="660" r="32" fill="#ffe95e"/>
            <circle class="glow" cx="455" cy="660" r="32" fill="#ffe95e"/>
            <path d="M382 724 Q414 750 452 724" stroke="#371b0b" stroke-width="13" fill="none" stroke-linecap="round"/>
            <path d="M575 640 C675 710 770 705 895 635" stroke="#a64d16" stroke-width="26" fill="none" opacity="0.55"/>
            <path d="M575 790 C690 850 815 845 940 760" stroke="#a64d16" stroke-width="26" fill="none" opacity="0.5"/>
            <path d="M275 1000 C410 900 600 905 735 1015" stroke="#d87922" stroke-width="84" fill="none" stroke-linecap="round"/>
          </g>
          <rect x="170" y="1100" width="740" height="180" rx="48" fill="#050505" opacity="0.78"/>
          <text x="540" y="1215" font-family="Impact, Arial Black, sans-serif" font-size="86" fill="#fff" stroke="#000" stroke-width="10" paint-order="stroke" text-anchor="middle">FULL-TIME CHAOS</text>
          {captions}
          <rect x="90" y="1770" width="880" height="22" rx="11" fill="#313545"/>
          <rect class="bar" x="90" y="1770" height="22" rx="11" fill="#ff2f6d"/>
        </svg>
        """
    ).strip() + "\n"


def srt_time(seconds: float) -> str:
    milliseconds = round((seconds - int(seconds)) * 1000)
    total = int(seconds)
    hours = total // 3600
    minutes = (total % 3600) // 60
    secs = total % 60
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"


def generate_srt() -> str:
    blocks = []
    for index, scene in enumerate(SCENES, start=1):
        blocks.append(
            f"{index}\n{srt_time(scene.start)} --> {srt_time(scene.end)}\n{scene.caption}\n"
        )
    return "\n".join(blocks)


def generate_ffmpeg_script(slug: str) -> str:
    return dedent(
        f"""
        #!/usr/bin/env bash
        set -euo pipefail

        # Optional export helper. Requires ffmpeg and an SVG renderer supported by
        # your ffmpeg build. If unsupported, open {slug}-animated-video.svg in a
        # browser and record/export it from there.
        ffmpeg -y -loop 1 -t 40 -i {slug}-thumbnail.svg \\
          -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,subtitles={slug}-captions.srt" \\
          -c:v libx264 -pix_fmt yuv420p -movflags +faststart {slug}.mp4
        """
    ).strip() + "\n"


def generate_manifest(slug: str, platform_name: str, tagline: str, title: str) -> dict[str, object]:
    return {
        "platform_name_options": PLATFORM_NAMES,
        "selected_platform_name": platform_name,
        "tagline": tagline,
        "video": {
            "slug": slug,
            "duration_seconds": SCENES[-1].end,
            "title_options": [
                "My Cat Has ONE Job… 😂 #shorts #funny #cat",
                "Orange Cat Interrupts My Work Again #shorts #funny #cute",
                "This Cat Works Full Time for Attention #shorts #viral",
                "Cat Behavior: He Always Does This When I Work #shorts",
            ],
            "recommended_title": "My Cat Has ONE Job… 😂 #shorts #funny #cat",
            "description": (
                "Meet Mac, the orange tabby who treats attention like a full-time job. "
                "Every time work starts, he shows up with confidence, chaos, and perfect comedic timing."
            ),
            "hashtags": HASHTAGS,
            "tags": TAGS,
            "thumbnail_alt": f"Orange tabby cat jumping toward a chair with bold text reading {title}",
            "scenes": [asdict(scene) for scene in SCENES],
        },
    }


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    thumbnail = args.output_dir / f"{args.slug}-thumbnail.svg"
    animated_video = args.output_dir / f"{args.slug}-animated-video.svg"
    captions = args.output_dir / f"{args.slug}-captions.srt"
    manifest = args.output_dir / f"{args.slug}-manifest.json"
    ffmpeg_script = args.output_dir / f"{args.slug}-render-video.sh"

    write(thumbnail, generate_thumbnail(args.thumbnail_title))
    write(animated_video, generate_animated_svg(args.thumbnail_title))
    write(captions, generate_srt())
    write(ffmpeg_script, generate_ffmpeg_script(args.slug))
    ffmpeg_script.chmod(0o755)
    manifest.write_text(
        json.dumps(
            generate_manifest(args.slug, args.platform_name, args.tagline, args.thumbnail_title),
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"Generated thumbnail: {thumbnail}")
    print(f"Generated animated video mock: {animated_video}")
    print(f"Generated captions: {captions}")
    print(f"Generated metadata: {manifest}")
    print(f"Generated optional FFmpeg helper: {ffmpeg_script}")
    if shutil.which("ffmpeg") is None:
        print("FFmpeg is not installed; SVG/caption assets were generated without rendering an MP4.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
