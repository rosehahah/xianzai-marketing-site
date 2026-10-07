#!/usr/bin/env python3
"""Re-layout the existing hero animation for portrait screens without changing its source."""
from pathlib import Path
import json, re, subprocess, tempfile

site = Path(__file__).resolve().parents[1]
project = site.parent / 'remotion-xiannow'
source_path = project / 'src/appstore-hero/AppStoreHero.tsx'
source = source_path.read_text()
source = source.replace("'../product-film/shared'", json.dumps(str(project / 'src/product-film/shared')))
source = source.replace('HERO_WIDTH = 3840', 'HERO_WIDTH = 1080').replace('HERO_HEIGHT = 1646', 'HERO_HEIGHT = 1920')
source = source.replace('size: 150', 'size: 82').replace('size: 138', 'size: 76')
source = source.replace('const PHONE = {x: 1920, y: 860, width: 470}', 'const PHONE = {x: 540, y: 835, width: 330}')
props = """const PROPS: Prop[] = [
  {src: 'obj-77.png', x: 170, y: 570, size: 280, rotate: -2},
  {src: 'obj-33.png', x: 910, y: 570, size: 280, rotate: 3},
  {src: 'obj-22.png', x: 155, y: 970, size: 310, rotate: 2},
  {src: 'obj-55.png', x: 915, y: 970, size: 300, rotate: -4},
  {src: 'obj-44.png', x: 260, y: 1400, size: 370, rotate: 6, floor: true},
  {src: 'obj-88.png', x: 820, y: 1400, size: 370, rotate: -2, floor: true},
  {src: 'obj-11.png', x: 175, y: 320, size: 190, rotate: -5},
  {src: 'obj-66.png', x: 905, y: 320, size: 190, rotate: 5},
];"""
characters = """const CHARACTERS: Character[] = [
  {src: 'ip-sprout-tea.png', size: 180, from: [120, 1040], to: [150, 790], at: 176, behind: 2},
  {src: 'ip-cactus.png', size: 150, from: [320, 1470], to: [350, 1160], at: 182, behind: 4},
  {src: 'ip-ghost.png', size: 145, from: [820, 1470], to: [720, 1150], at: 186, behind: 5},
  {src: 'ip-devil.png', size: 210, from: [920, 1470], to: [930, 1170], at: 179, behind: 5},
  {src: 'ip-bunny.png', size: 150, from: [900, 380], to: [850, 450], at: 189, behind: 7},
  {src: 'ip-sprout-wink.png', size: 145, from: [170, 380], to: [210, 460], at: 192, behind: 6},
  {src: 'ip-monster.png', size: 150, from: [720, -200], to: [720, 390], at: 184, behind: -1, spin: 220},
];"""
source, n = re.subn(r'const PROPS: Prop\[\] = \[.*?\n\];', props, source, count=1, flags=re.S)
assert n == 1
source, n = re.subn(r'const CHARACTERS: Character\[\] = \[.*?\n\];', characters, source, count=1, flags=re.S)
assert n == 1
source = source.replace('top: 64,', 'top: 145,').replace("gap: lang === 'en' ? '0.28em' : 0,", "gap: 0,\n        flexDirection: 'column',\n        alignItems: 'center',\n        lineHeight: 1.08,")
source += """
import {Composition, registerRoot} from 'remotion';
const PortraitRoot = () => <>
  <Composition id="WebHeroPortraitZH" component={AppStoreHero} width={1080} height={1920} fps={30} durationInFrames={240} />
  <Composition id="WebHeroPortraitEN" component={AppStoreHero} defaultProps={{lang: 'en' as const}} width={1080} height={1920} fps={30} durationInFrames={240} />
</>;
registerRoot(PortraitRoot);
"""
output = site / 'assets/video'
output.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='xiannow-portrait-') as directory:
    temp = Path(directory)
    (temp / 'node_modules').symlink_to(project / 'node_modules', target_is_directory=True)
    entry = temp / 'portrait.tsx'
    entry.write_text(source)
    cli = project / 'node_modules/.bin/remotion'
    for lang in ('zh', 'en'):
        composition = 'WebHeroPortrait' + lang.upper()
        common = [str(cli), str(entry), composition, '--public-dir=' + str(project / 'public'), '--browser-executable=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--log=error']
        subprocess.run([common[0], 'still', *common[1:], str(output / f'hero-{lang}-portrait-poster.jpg'), '--frame=189', '--image-format=jpeg', '--jpeg-quality=100', '--scale=1.5'], cwd=project, check=True)
        subprocess.run([common[0], 'render', *common[1:], str(output / f'hero-{lang}-portrait.mp4'), '--codec=h264', '--crf=16', '--image-format=png', '--scale=1.5', '--pixel-format=yuv420p', '--audio-codec=aac', '--audio-bitrate=256k', '--concurrency=3'], cwd=project, check=True)
