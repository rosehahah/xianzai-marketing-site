#!/bin/sh
# Usage: sh scripts/prepare-hero-media.sh [directory-containing-the-two-original-mp4s]
set -eu
site_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
input_dir=${1:-"$site_root/../remotion-xiannow/out"}
output_dir="$site_root/assets/video"
command -v ffmpeg >/dev/null 2>&1 || { echo 'ffmpeg is required.' >&2; exit 1; }
for language in zh en; do
  test -f "$input_dir/xiannow-appstore-hero-8s-$language.mp4" || { echo "Missing $language source video in $input_dir" >&2; exit 1; }
done
mkdir -p "$output_dir"
for language in zh en; do
  input_file="$input_dir/xiannow-appstore-hero-8s-$language.mp4"
  ffmpeg -hide_banner -loglevel error -i "$input_file" -map 0:v:0 -map '0:a:0?' -c copy -movflags +faststart "$output_dir/hero-$language.mp4" -y
  ffmpeg -hide_banner -loglevel error -ss 6.3 -i "$input_file" -frames:v 1 -q:v 2 "$output_dir/hero-$language-poster.jpg" -y
done
