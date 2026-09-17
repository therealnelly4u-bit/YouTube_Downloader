# Cat Shorts Script and Image Optimization Plan

This package turns the provided orange-tabby reference into a short-form video concept with a clear hook, search-friendly metadata, and thumbnail/image optimization guidance.

## Platform Name Ideas

1. **TypeSprint Studio** — fast, polished, and competitive.
2. **KeyFlow Academy** — calm, skill-building, and learner-friendly.
3. **SwiftKeys Lab** — modern, practice-focused, and memorable.
4. **Accuracy Arcade** — playful, game-like, and performance-driven.

Recommended tagline: **Master Speed. Improve Accuracy.**

## Short Video Script: “My Cat Has One Job”

**Length:** 35–45 seconds
**Tone:** funny, warm, fast-paced
**Visual theme:** orange tabby, glowing eyes, desk/chair interruption, bold captions

| Timestamp | Visual | Voiceover / Caption |
| --- | --- | --- |
| 0:00–0:03 | Cat staring with glowing eyes. | “My cat has one job…” |
| 0:04–0:08 | Cat jumps toward the chair or desk. | “Reach for attention before I can do any work.” |
| 0:09–0:14 | Owner tries to type; cat blocks the setup. | “Every time I open my laptop, Mac clocks in.” |
| 0:15–0:22 | Close-up of confident cat face. | “No meetings. No deadlines. Just full-time chaos.” |
| 0:23–0:31 | Cat sits proudly like a boss. | “And somehow, he still gets employee of the month.” |
| 0:32–0:40 | Freeze frame with thumbnail-style text. | “Would your pet get hired for this job?” |

## Optimized Title Options

- **My Cat Has ONE Job… 😂 #shorts #funny #cat**
- **Orange Cat Interrupts My Work Again #shorts #funny #cute**
- **This Cat Works Full Time for Attention #shorts #viral**
- **Cat Behavior: He Always Does This When I Work #shorts**

## Description

Meet Mac, the orange tabby who treats attention like a full-time job. Every time work starts, he shows up with confidence, chaos, and perfect comedic timing. Watch until the end and tell us what job your pet would have.

## Tags and Hashtags

**Hashtags:** `#shorts #funny #cat #cute #viral #moments #catbehavior #orangecat #pets`
**Tags:** `cat shorts`, `funny cat`, `orange tabby`, `cute cat video`, `cat interrupts work`, `pet comedy`, `viral cat moments`, `cat behavior`

## Thumbnail and Image Optimization Checklist

- Use a **16:9 thumbnail at 1280×720** for standard YouTube previews.
- Keep the cat or main subject on the right third and bold text on the left third.
- Use 3–5 words of high-contrast text, such as **“MY CAT HAS ONE JOB…”**.
- Add a soft outline/glow around the cat so it stays readable on mobile.
- Export thumbnails as WebP or optimized JPEG at 80–85 quality.
- Keep file size under 300 KB when possible for fast page loads.
- Add descriptive alt text: `Orange tabby cat jumping toward a chair with bold text reading My Cat Has One Job`.

## Running the Image Optimizer

Use the repository script after adding local screenshots, thumbnails, or website images:

```bash
python3 scripts/optimize_images.py path/to/images --output-dir optimized-images --max-width 1280 --quality 82 --format webp
```

Run a no-write preview first:

```bash
python3 scripts/optimize_images.py path/to/images --dry-run
```

## Generated Asset Outputs

Run the generator to recreate the committed sample assets:

```bash
python3 scripts/generate_video_assets.py --output-dir assets/generated
```

The generator writes:

- `cat-short-thumbnail.svg` — a 1280×720 YouTube thumbnail.
- `cat-short-animated-video.svg` — a 1080×1920 animated vertical short mock.
- `cat-short-captions.srt` — timed captions matching the script.
- `cat-short-manifest.json` — platform names, tagline, metadata, tags, and scene data.
- `cat-short-render-video.sh` — an optional FFmpeg helper for environments with FFmpeg installed.
