#!/usr/bin/env python3
"""Build the bilingual static marketing site and render its Markdown policies."""
from pathlib import Path
from urllib.parse import urljoin
import os
import re
import shutil

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'
BASE_PATH = os.environ.get('SITE_BASE_PATH', '').strip('/')
BASE_PREFIX = f'/{BASE_PATH}' if BASE_PATH else ''
SITE_URL = os.environ.get('SITE_URL', '').rstrip('/')


def with_base_path(value: str) -> str:
    """Prefix root-relative URLs for hosts such as GitHub project Pages."""
    if not BASE_PREFIX:
        return value
    return re.sub(r'(["\'(])/(?!/)', lambda match: match.group(1) + BASE_PREFIX + '/', value)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(with_base_path(content), encoding='utf-8')


def write_route(route: str, content: str) -> None:
    write_text(DIST / route / 'index.html', content)


if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir(parents=True)

for name in ('site.css', 'site.js', 'favicon.png'):
    source = ROOT / name
    target = DIST / name
    if source.suffix in ('.css', '.js', '.svg'):
        write_text(target, source.read_text(encoding='utf-8'))
    else:
        shutil.copy2(source, target)

shutil.copytree(ROOT / 'assets', DIST / 'assets')
if BASE_PREFIX:
    # Gallery manifests contain root-relative image paths.
    for manifest_name in ('templates.json', 'templates.en.json'):
        manifest = DIST / 'assets' / manifest_name
        manifest.write_text(with_base_path(manifest.read_text(encoding='utf-8')), encoding='utf-8')

zh_home = (ROOT / 'index.html').read_text(encoding='utf-8')
en_home = (ROOT / 'index.en.html').read_text(encoding='utf-8')
write_route('zh', zh_home)
write_route('en', en_home)


def root_language_page() -> str:
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#f8f7f3"><meta name="robots" content="index,follow">
<meta name="description" content="Choose Chinese or English to visit XianNow.">
<title>XianNow / 苋在</title>
<link rel="alternate" hreflang="zh-CN" href="/zh/"><link rel="alternate" hreflang="en" href="/en/"><link rel="alternate" hreflang="x-default" href="/">
<link rel="icon" type="image/png" href="/favicon.png"><link rel="stylesheet" href="/site.css">
<script>
(function () {{
  var saved = null;
  try {{ saved = window.localStorage.getItem('xiannow-language'); }} catch (_) {{}}
  var language = saved === 'zh' || saved === 'en' ? saved : (navigator.language || '').toLowerCase().startsWith('zh') ? 'zh' : 'en';
  var target = new URL(language.concat(String.fromCharCode(47)), window.location.href);
  target.search = window.location.search;
  target.hash = window.location.hash;
  window.location.replace(target.href);
}}());
</script></head><body class="language-page">
<main class="language-card"><img src="/assets/app-icon.png" alt="" width="76" height="76"><p class="legal-kicker">XIANNow / 苋在</p><h1>Choose your language<br><span>选择语言</span></h1><div class="language-actions"><a class="button button-dark" href="/en/" hreflang="en">English</a><a class="button button-pink" href="/zh/" hreflang="zh-CN">中文</a></div></main>
</body></html>'''


write_text(DIST / 'index.html', root_language_page())

renderer = MarkdownIt('default', {'html': False, 'linkify': False}).enable('table')

LEGAL_LOCALES = {
    'zh': {
        'lang': 'zh-CN',
        'brand': '苋在',
        'home_label': '苋在首页',
        'back': '← 返回苋在',
        'nav_label': '法律页面',
        'terms': '用户协议',
        'privacy': '隐私政策',
        'description': lambda title: f'苋在{title}全文。',
        'tagline': '把日常拍成自己的故事。',
        'support': '客服与反馈',
        'back_home': '返回首页',
        'version': '当前版本',
        'switch_label': 'Switch to English',
        'switch_text': 'EN',
        'other_locale': 'en',
        'source_terms': '用户协议.md',
        'source_privacy': '隐私政策.md',
    },
    'en': {
        'lang': 'en',
        'brand': 'XianNow',
        'home_label': 'XianNow home',
        'back': '← Back to XianNow',
        'nav_label': 'Legal pages',
        'terms': 'Terms of Use',
        'privacy': 'Privacy Policy',
        'description': lambda title: f'Read the XianNow {title}.',
        'tagline': 'Turn everyday moments into stories of your own.',
        'support': 'Support & feedback',
        'back_home': 'Back to home',
        'version': 'Current page',
        'switch_label': '切换到中文',
        'switch_text': '中文',
        'other_locale': 'zh',
        'source_terms': 'terms.en.md',
        'source_privacy': 'privacy.en.md',
    },
}


def legal_page(locale: str, slug: str, markdown: str) -> str:
    copy = LEGAL_LOCALES[locale]
    other_locale = copy['other_locale']
    title = copy[slug]
    article = renderer.render(markdown)
    return f'''<!doctype html>
<html lang="{copy['lang']}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#f4f5f8"><meta name="robots" content="index,follow">
<meta name="description" content="{copy['description'](title)}">
<title>{title} | {copy['brand']}</title>
<link rel="canonical" href="/{locale}/{slug}/"><link rel="alternate" hreflang="zh-CN" href="/zh/{slug}/"><link rel="alternate" hreflang="en" href="/en/{slug}/"><link rel="alternate" hreflang="x-default" href="/zh/{slug}/">
<link rel="icon" type="image/png" href="/favicon.png"><link rel="stylesheet" href="/site.css">
</head><body class="legal-page">
<header class="legal-top"><a class="legal-back" href="/{locale}/">{copy['back']}</a><a class="brand" href="/{locale}/" aria-label="{copy['home_label']}"><img src="/assets/app-icon.png" alt="" width="40" height="40"><span>{copy['brand']}</span></a><nav class="legal-top-links" aria-label="{copy['nav_label']}"><a href="/{locale}/terms/">{copy['terms']}</a><a href="/{locale}/privacy/">{copy['privacy']}</a><a class="language-link" href="/{other_locale}/{slug}/" hreflang="{LEGAL_LOCALES[other_locale]['lang']}" aria-label="{copy['switch_label']}">{copy['switch_text']}</a></nav></header>
<main class="legal-main"><p class="legal-kicker">XIÁNZÀI / LEGAL</p><h1>{title}</h1><article class="legal-content">{article}</article></main>
<footer class="site-footer legal-footer"><div class="footer-brand"><a class="brand" href="/{locale}/"><img src="/assets/app-icon.png" alt="" width="38" height="38"><span>{copy['brand']}</span></a><p>{copy['tagline']}</p></div><nav class="footer-links" aria-label="{copy['nav_label']}"><a href="/{locale}/terms/">{copy['terms']}</a><a href="/{locale}/privacy/">{copy['privacy']}</a><a href="/{locale}/#faq">{copy['support']}</a><a href="/{locale}/">{copy['back_home']}</a></nav><div class="footer-bottom"><span>© 2026 {copy['brand']}</span><span>{copy['version']} · {title}</span></div></footer>
<script>document.querySelectorAll('.language-link').forEach(function (link) {{ link.addEventListener('click', function () {{ try {{ window.localStorage.setItem('xiannow-language', '{other_locale}'); }} catch (_) {{}} }}); }});</script>
</body></html>'''


rendered_legal = {}
for locale, copy in LEGAL_LOCALES.items():
    for slug in ('terms', 'privacy'):
        source_name = copy[f'source_{slug}']
        markdown = (ROOT / 'content' / source_name).read_text(encoding='utf-8')
        page = legal_page(locale, slug, markdown)
        rendered_legal[(locale, slug)] = page
        write_route(f'{locale}/{slug}', page)
        write_text(DIST / locale / f'{slug}.html', page)

# Keep the original Chinese legal URLs stable for existing in-App and external links.
for slug in ('terms', 'privacy'):
    page = rendered_legal[('zh', slug)]
    write_route(slug, page)
    write_text(DIST / f'{slug}.html', page)

write_text(DIST / 'robots.txt', 'User-agent: *\nAllow: /\n' + (f'Sitemap: {SITE_URL}/sitemap.xml\n' if SITE_URL else ''))

if SITE_URL:
    urls = ('/zh/', '/en/', '/zh/terms/', '/en/terms/', '/zh/privacy/', '/en/privacy/')
    entries = ''.join(f'<url><loc>{urljoin(SITE_URL + "/", path.lstrip("/"))}</loc></url>' for path in urls)
    sitemap = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{entries}</urlset>'
    write_text(DIST / 'sitemap.xml', sitemap)

print(f'Built bilingual static site: {DIST}')
