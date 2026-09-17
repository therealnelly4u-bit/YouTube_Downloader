#!/usr/bin/env bash
set -euo pipefail

# Optional export helper. Requires ffmpeg and an SVG renderer supported by
# your ffmpeg build. If unsupported, open cat-short-animated-video.svg in a
# browser and record/export it from there.
ffmpeg -y -loop 1 -t 40 -i cat-short-thumbnail.svg \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,subtitles=cat-short-captions.srt" \
  -c:v libx264 -pix_fmt yuv420p -movflags +faststart cat-short.mp4
