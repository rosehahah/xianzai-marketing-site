#!/bin/sh
# Create web derivatives without changing the original MP4/JPEG assets.
# Usage: sh scripts/optimize-hero-media.sh [input-directory] [output-directory]
# Dependencies: ffmpeg with libx264, Python 3 with Pillow/WebP support.
# Optional overrides: HERO_PYTHON, HERO_THREADS, HERO_CRF, HERO_POSTER_QUALITY.
set -eu

site_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
input_dir=${1:-"$site_root/assets/video"}
output_dir=${2:-"$site_root/assets/video"}
hero_python=${HERO_PYTHON:-python3}
hero_threads=${HERO_THREADS:-4}
hero_crf=${HERO_CRF:-22}
hero_poster_quality=${HERO_POSTER_QUALITY:-85}

command -v ffmpeg >/dev/null 2>&1 || { echo 'ffmpeg is required.' >&2; exit 1; }
command -v "$hero_python" >/dev/null 2>&1 || { echo 'Python 3 is required; set HERO_PYTHON if needed.' >&2; exit 1; }
"$hero_python" - <<'PY'
from PIL import features
if not features.check('webp'):
    raise SystemExit('Pillow with WebP support is required.')
PY

for language in en zh; do
  for asset in "hero-$language.mp4" "hero-$language-portrait.mp4" "hero-$language-poster.jpg" "hero-$language-portrait-poster.jpg"; do
    test -f "$input_dir/$asset" || { echo "Missing source asset: $input_dir/$asset" >&2; exit 1; }
  done
done

mkdir -p "$output_dir"
work_dir=$(mktemp -d "$output_dir/.hero-web-XXXXXX")
trap 'rm -rf "$work_dir"' EXIT
trap 'exit 1' HUP INT TERM

encode_video() {
  ffmpeg -hide_banner -loglevel warning -nostdin -i "$1" \
    -map 0:v:0 -map '0:a:0?' -map_metadata -1 \
    -vf "scale=$2:$3:flags=lanczos:out_range=tv,setsar=1" \
    -c:v libx264 -preset slow -crf "$hero_crf" -threads "$hero_threads" \
    -r 30 -pix_fmt yuv420p -color_range tv \
    -c:a aac -b:a 128k -movflags +faststart -y "$4"
}

for language in en zh; do
  echo "Encoding $language landscape (2560 x 1098)."
  encode_video "$input_dir/hero-$language.mp4" 2560 1098 "$work_dir/hero-$language-web.mp4"
  echo "Encoding $language portrait (1080 x 1920)."
  encode_video "$input_dir/hero-$language-portrait.mp4" 1080 1920 "$work_dir/hero-$language-portrait-web.mp4"
done

"$hero_python" - "$input_dir" "$work_dir" "$hero_poster_quality" <<'PY'
from pathlib import Path
import sys
from PIL import Image, ImageOps

source, output = map(Path, sys.argv[1:3])
quality = int(sys.argv[3])
for language in ('en', 'zh'):
    for orientation, width in (('', 1920), ('-portrait', 1080)):
        stem = f'hero-{language}{orientation}-poster'
        with Image.open(source / f'{stem}.jpg') as image:
            image = ImageOps.exif_transpose(image).convert('RGB')
            height = round(image.height * width / image.width)
            image = image.resize((width, height), Image.Resampling.LANCZOS)
            image.save(output / f'{stem}.webp', 'WEBP', quality=quality, method=6)
PY

# Publish only the derivatives, after every encode has succeeded.
for language in en zh; do
  for asset in "hero-$language-web.mp4" "hero-$language-portrait-web.mp4" "hero-$language-poster.webp" "hero-$language-portrait-poster.webp"; do
    mv -f "$work_dir/$asset" "$output_dir/$asset"
  done
done
echo "Web derivatives written to $output_dir; original assets preserved."
