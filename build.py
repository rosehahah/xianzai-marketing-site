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

for name in ('site.css', 'site.js', 'event-photo.css', 'favicon.png'):
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


def event_photo_page(kind: str, markdown: str, locale: str = 'zh') -> str:
    """Independent product pages: no homepage scripts, cookies, or external assets."""
    is_privacy = kind == 'privacy'
    english = locale == 'en'
    product_home = '/event-photo/en/' if english else '/event-photo/'
    privacy_route = product_home + 'privacy/'
    title = ('Privacy Policy' if is_privacy else 'Support & Help') if english else ('隐私政策' if is_privacy else '支持与帮助')
    route = privacy_route if is_privacy else product_home
    other_home = '/event-photo/' if english else '/event-photo/en/'
    other_route = other_home + ('privacy/' if is_privacy else '')
    canonical = SITE_URL + route if SITE_URL else route
    description = ('现场活动拍摄如何处理本地照片、系统权限、模板素材、免费首场资格和 Apple 购买。'
                   if is_privacy else '现场活动拍摄的拍摄保存、免费首场、Pro 购买与恢复帮助，以及官方联系渠道。')
    if english:
        description = ('How 现场活动拍摄 handles local photos, permissions, template downloads, free-event allowance and Apple purchases.'
                       if is_privacy else 'Camera, saving, free-event allowance, Pro purchase and restore help for 现场活动拍摄.')
    article = renderer.render(markdown)
    section_number = 0
    headings = []

    def anchor_heading(match):
        nonlocal section_number
        section_number += 1
        anchor = f'section-{section_number}'
        headings.append((anchor, match.group(1)))
        return f'<h2 id="{anchor}">{match.group(1)}</h2>'

    article = re.sub(r'<h2>(.*?)</h2>', anchor_heading, article)
    contents = ''.join(f'<li><a href="#{anchor}">{heading}</a></li>' for anchor, heading in headings)
    lede = ('普通拍摄在设备上处理；联网素材、Apple 购买和管理员模板发布分别说明。'
            if is_privacy else '活动前设好文字、Logo 和色调，现场直接拍出统一成片。拍摄、保存和购买的问题，从这里开始。')
    if english:
        lede = ('Ordinary captures are processed on your device. Downloads, Apple purchases and authorized template publishing are explained separately.'
                if is_privacy else 'Set your event text, logo and color style before shooting. Find help with capturing, saving and Pro here. The app interface is currently in Simplified Chinese.')
    quick_start = '' if is_privacy else '''<section class="event-start" aria-labelledby="start-title">
<div><span class="event-number">01—03</span><h2 id="start-title">从一场活动开始</h2></div>
<ol><li><strong>创建活动</strong><span>选择活动场景，挑好模板。</span></li><li><strong>设好风格</strong><span>改文字、Logo 和滤镜强度。</span></li><li><strong>现场拍摄</strong><span>先拍出第一张，再继续记录。</span></li></ol>
<p class="event-scenes">茶咖相聚 <span>·</span> 灵感工坊 <span>·</span> 生活市集 <span>·</span> 分享沙龙 <span>·</span> 户外同行</p>
</section>'''
    if english and not is_privacy:
        quick_start = '''<section class="event-start" aria-labelledby="start-title">
<div><span class="event-number">01—03</span><h2 id="start-title">Start with one event</h2></div>
<ol><li><strong>Create an event</strong><span>Choose a scene and a template.</span></li><li><strong>Set your style</strong><span>Edit text, logo and filter intensity.</span></li><li><strong>Capture the event</strong><span>Save your first photo, then keep shooting.</span></li></ol>
<p class="event-scenes">Tea &amp; coffee <span>·</span> Creative workshops <span>·</span> Lifestyle markets <span>·</span> Sharing salons <span>·</span> Outdoor gatherings</p>
</section>'''
    support_label = 'Support' if english else '支持帮助'
    privacy_label = 'Privacy' if english else '隐私政策'
    lang = 'en' if english else 'zh-CN'
    other_lang = 'zh-CN' if english else 'en'
    contact_text = 'Need more help?' if english else '需要进一步帮助？'
    contact_copy = 'Developer / operator: 韩月 (Han Yue)<br>Email us for product support or privacy requests.' if english else '开发者 / 运营者：韩月<br>产品支持与隐私请求均可通过邮件联系。'
    return f'''<!doctype html>
<html lang="{lang}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#f8f7f3"><meta name="robots" content="index,follow">
<meta name="description" content="{description}"><meta name="referrer" content="strict-origin-when-cross-origin">
<title>{title} | 现场活动拍摄</title><link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="{lang}" href="{route}"><link rel="alternate" hreflang="{other_lang}" href="{other_route}">
<link rel="stylesheet" href="/event-photo.css">
</head><body class="event-page">
<a class="event-skip" href="#main">{'Skip to content' if english else '跳到正文'}</a>
<header class="event-header"><a class="event-brand" href="{product_home}"><span class="event-mark" aria-hidden="true"></span><span>现场活动拍摄</span></a><nav aria-label="{'Product information' if english else '产品信息'}"><a href="{product_home}"{' aria-current="page"' if not is_privacy else ''}>{support_label}</a><a href="{privacy_route}"{' aria-current="page"' if is_privacy else ''}>{privacy_label}</a><a href="{other_route}" lang="{other_lang}" hreflang="{other_lang}">{'中文' if english else 'English'}</a></nav></header>
<main id="main" class="event-main"><section class="event-intro"><p class="event-kicker">{'PRIVACY' if is_privacy else 'SUPPORT'} / 现场活动拍摄</p><h1>{title}<span class="event-title-square" aria-hidden="true"></span></h1><p class="event-lede">{lede}</p><p class="event-updated">{'Updated: October 16, 2026' if english else '更新日期：2026 年 10 月 16 日'}</p></section>
{quick_start}
<div class="event-reading"><aside class="event-toc"><h2>{'On this page' if english else '本页内容'}</h2><ol>{contents}</ol></aside><article class="event-content" aria-label="{title}">{article}</article></div>
<section class="event-contact" aria-labelledby="contact-title"><div><p class="event-kicker">CONTACT</p><h2 id="contact-title">{contact_text}</h2><p>{contact_copy}</p></div><a href="mailto:hanr6969@gmail.com">hanr6969@gmail.com <span aria-hidden="true">↗</span></a></section>
</main>
<footer class="event-footer"><span>© 2026 韩月 · 现场活动拍摄</span><nav aria-label="{'Footer' if english else '页脚'}"><a href="{product_home}">{support_label}</a><a href="{privacy_route}">{privacy_label}</a><a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">{'Apple Standard EULA' if english else 'Apple 标准使用条款'}</a></nav></footer>
</body></html>'''


for locale, product_route in (('zh', 'event-photo'), ('en', 'event-photo/en')):
    for kind in ('support', 'privacy'):
        suffix = '.en' if locale == 'en' else ''
        markdown = (ROOT / 'content' / f'event-photo-{kind}{suffix}.md').read_text(encoding='utf-8')
        route = product_route + ('/privacy' if kind == 'privacy' else '')
        write_route(route, event_photo_page(kind, markdown, locale))

write_text(DIST / 'robots.txt', 'User-agent: *\nAllow: /\n' + (f'Sitemap: {SITE_URL}/sitemap.xml\n' if SITE_URL else ''))

if SITE_URL:
    urls = ('/zh/', '/en/', '/zh/terms/', '/en/terms/', '/zh/privacy/', '/en/privacy/', '/event-photo/', '/event-photo/privacy/', '/event-photo/en/', '/event-photo/en/privacy/')
    entries = ''.join(f'<url><loc>{urljoin(SITE_URL + "/", path.lstrip("/"))}</loc></url>' for path in urls)
    sitemap = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{entries}</urlset>'
    write_text(DIST / 'sitemap.xml', sitemap)

print(f'Built bilingual static site: {DIST}')
