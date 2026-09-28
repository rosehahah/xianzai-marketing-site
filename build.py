#!/usr/bin/env python3
"""Assemble a dependency-light static site and render the supplied Markdown policies."""
from pathlib import Path
import shutil
import os
import re
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'
BASE_PATH = os.environ.get('SITE_BASE_PATH', '').strip('/')
BASE_PREFIX = f'/{BASE_PATH}' if BASE_PATH else ''

def with_base_path(value: str) -> str:
    if not BASE_PREFIX:
        return value
    return re.sub(r'(["\'(])/(?!/)', lambda match: match.group(1) + BASE_PREFIX + '/', value)

if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir(parents=True)
for name in ('index.html', 'site.css', 'site.js', 'favicon.png'):
    source = ROOT / name
    target = DIST / name
    if source.suffix in ('.html', '.css', '.js', '.svg'):
        target.write_text(with_base_path(source.read_text(encoding='utf-8')), encoding='utf-8')
    else:
        shutil.copy2(source, target)
shutil.copytree(ROOT / 'assets', DIST / 'assets')

if BASE_PREFIX:
    # The template manifest contains root-relative image paths used by the gallery.
    manifest = DIST / 'assets' / 'templates.json'
    manifest.write_text(with_base_path(manifest.read_text(encoding='utf-8')), encoding='utf-8')

terms = (ROOT / 'content' / '用户协议.md').read_text(encoding='utf-8')
privacy = (ROOT / 'content' / '隐私政策.md').read_text(encoding='utf-8')
renderer = MarkdownIt('default', {'html': False, 'linkify': False}).enable('table')

def legal_page(title: str, slug: str, content: str) -> str:
    article = renderer.render(content)
    other_slug = 'privacy' if slug == 'terms' else 'terms'
    other_title = '隐私政策' if slug == 'terms' else '用户协议'
    return f'''<!doctype html>
<html lang="zh-CN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#f4f5f8"><meta name="robots" content="index,follow">
<meta name="description" content="苋在{title}全文。">
<title>{title}｜苋在</title><link rel="icon" type="image/png" href="/favicon.png"><link rel="stylesheet" href="/site.css">
</head><body class="legal-page">
<header class="legal-top"><a class="legal-back" href="/">← 返回苋在</a><a class="brand" href="/" aria-label="苋在首页"><img src="/assets/app-icon.png" alt="" width="40" height="40"><span>苋在</span></a><nav class="legal-top-links" aria-label="法律页面"><a href="/terms/">用户协议</a><a href="/privacy/">隐私政策</a></nav></header>
<main class="legal-main"><p class="legal-kicker">XIÁNZÀI / LEGAL</p><h1>{title}</h1><article class="legal-content">{article}</article></main>
<footer class="site-footer legal-footer"><div class="footer-brand"><a class="brand" href="/"><img src="/assets/app-icon.png" alt="" width="38" height="38"><span>苋在</span></a><p>把日常拍成自己的故事。</p></div><nav class="footer-links" aria-label="法律与支持"><a href="/terms/">用户协议</a><a href="/privacy/">隐私政策</a><a href="/#faq">客服与反馈</a><a href="/">返回首页</a></nav><div class="footer-bottom"><span>© 2026 苋在</span><span>当前版本 · {title}</span></div></footer>
</body></html>'''

for slug, title, content in (('terms', '用户协议', terms), ('privacy', '隐私政策', privacy)):
    route = DIST / slug
    route.mkdir()
    (route / 'index.html').write_text(with_base_path(legal_page(title, slug, content)), encoding='utf-8')
    # Also expose stable .html URLs for static hosts without clean URL support.
    (DIST / f'{slug}.html').write_text(with_base_path(legal_page(title, slug, content)), encoding='utf-8')

print(f'Built static site: {DIST}')
