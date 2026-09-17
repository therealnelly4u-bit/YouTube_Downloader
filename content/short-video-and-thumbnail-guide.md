# Short Video and Thumbnail Guide

This guide supports the two creator-owned references: the numbered mini-hoop
challenge and the cat close-up. It does not assume that generated visuals are a
replacement for the supplied footage or photo.

## Challenge Short: “Who Makes the Shot?”

**Hook:** “Pick your winner before the ball drops.”

| Time | Footage | Caption |
| --- | --- | --- |
| 0:00–0:02 | Wide shot of all eight numbered players. | Pick your winner! |
| 0:02–0:05 | First attempt and the group reaction. | Player 1 starts us off. |
| 0:05–0:10 | Fast cuts of the closest attempts. | Who has the best shot? |
| 0:10–0:14 | Winning shot or best reaction replay. | Comment the number you picked! |

**Title:** `Who Makes the Shot? 🎯 Pick Your Winner #shorts`

**Thumbnail headline:** `WHO MAKES THE SHOT?`
**Thumbnail CTA:** `COMMENT YOUR PICK`

## Cat Short: “Cat Has a New Look”

**Hook:** “Wait until you see his new look.”

| Time | Footage | Caption |
| --- | --- | --- |
| 0:00–0:02 | Cat looking into camera. | Wait for the reveal… |
| 0:02–0:05 | Show the small headband detail. | New look unlocked. |
| 0:05–0:09 | Hold on the cat’s expression. | Does he approve? |
| 0:09–0:13 | End on the strongest close-up. | Rate the look from 1–10. |

**Title:** `My Cat Has a New Look 😹 #shorts #cat`

**Thumbnail headline:** `CAT HAS A NEW LOOK`
**Thumbnail CTA:** `RATE IT 1–10`

## Generate a Package From a Real Reference

Pass a local JPEG, PNG, or WebP file to create a source-image-based thumbnail,
caption track, edit brief, and FFmpeg helper:

```bash
python3 scripts/generate_video_assets.py path/to/challenge.jpg \
  --type challenge --output-dir assets/generated

python3 scripts/generate_video_assets.py path/to/cat.jpg \
  --type cat --cta "RATE IT 1–10" --output-dir assets/generated
```

The generator embeds the supplied source image inside the SVG thumbnail, so the
thumbnail remains portable. The optional render script creates a 9:16 MP4 from
the reference image and captions when FFmpeg is available.

## Image Delivery Checklist

- Use a 1280×720 thumbnail with a concise, high-contrast headline.
- Keep critical text away from the image edges for mobile crops.
- Use the original creator-owned image; obtain permission before publishing
  images containing recognizable people.
- Run the image optimizer before upload when publishing raster thumbnails.

```bash
python3 scripts/optimize_images.py path/to/images --output-dir optimized-images \
  --max-width 1280 --quality 82 --format webp
```
