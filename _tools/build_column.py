# -*- coding: utf-8 -*-
"""発達コラムを _columns/*.md から生成する（標準実装ルール準拠）。

使い方（リポジトリ直下で）: python3 _tools/build_column.py
- column/<slug>.html を全記事ぶん再生成（前後リンクもここで更新される）
- column/index.html を再生成（公開日の新しい順）
- sitemap.xml の column エントリを追加・更新
ヘッダー・フッターは guide-nagoya.html から取り出し、リンクを絶対パスに直して使う。
アンダースコアで始まるフォルダは GitHub Pages（Jekyll）で公開されない。
"""
import glob
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://junochild.com'
os.chdir(ROOT)


# ---------------------------------------------------------------- 原稿の読み込み
def parse(path):
    text = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', text, re.S)
    assert m, f'front matter がありません: {path}'
    meta, refs, key = {}, [], None
    for line in m.group(1).splitlines():
        if re.match(r'^\s+-\s', line) and key == 'refs':
            refs.append(re.sub(r'^\s+-\s', '', line).strip())
        elif ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            meta[key] = val.strip()
    meta['refs'] = refs
    for k in ['slug', 'title', 'description', 'lead', 'published', 'updated']:
        assert meta.get(k), f'{k} が未記入です: {path}'
    meta['body'] = m.group(2)
    return meta


def esc(s):
    return html.escape(s, quote=False)


def inline(s):
    s = esc(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    return s


def link_urls(s):
    s = esc(s)
    return re.sub(r'(https?://[^\s<]+)', r'<a href="\1" target="_blank" rel="noopener">\1</a>', s)


# ---------------------------------------------------------------- Markdown → HTML
def md_to_html(md):
    lines = md.strip('\n').split('\n')
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith('### '):
            out.append(f'<h3 class="col-h3">{inline(line[4:].strip())}</h3>')
            i += 1
        elif line.startswith('## '):
            out.append(f'<h2 class="col-h2">{inline(line[3:].strip())}</h2>')
            i += 1
        elif line.startswith('>'):
            block = []
            while i < len(lines) and lines[i].startswith('>'):
                block.append(re.sub(r'^>\s?', '', lines[i]).strip())
                i += 1
            block = [b for b in block if b]
            kind, label = 'note', ''
            if block and block[0] in ('【研究】', '【注記】'):
                label = block.pop(0).strip('【】')
                kind = 'research' if label == '研究' else 'note'
            ps = ''.join(f'<p>{inline(b)}</p>' for b in block)
            lab = f'<span class="col-{kind}__label">{label}</span>' if label else ''
            out.append(f'<div class="col-{kind}">{lab}{ps}</div>')
        elif re.match(r'^- \[ \] ', line):
            items = []
            while i < len(lines) and re.match(r'^- \[ \] ', lines[i]):
                items.append(f'<li>{inline(lines[i][6:].strip())}</li>')
                i += 1
            out.append('<ul class="col-check">' + ''.join(items) + '</ul>')
        elif line.startswith('- '):
            items = []
            while i < len(lines) and lines[i].startswith('- ') and not re.match(r'^- \[ \] ', lines[i]):
                items.append(f'<li>{inline(lines[i][2:].strip())}</li>')
                i += 1
            out.append('<ul class="col-list">' + ''.join(items) + '</ul>')
        elif re.match(r'^\*\*.+\*\*$', line.strip()):
            out.append(f'<p class="col-sub">{inline(line.strip())}</p>')
            i += 1
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(r'^(#{2,3} |>|- )', lines[i]):
                para.append(lines[i].strip())
                i += 1
            out.append(f'<p class="col-p">{inline("".join(para))}</p>')
    return '\n'.join('      ' + o for o in out)


# ---------------------------------------------------------------- 共通パーツ
def absolutize(chunk):
    chunk = re.sub(r'href="index\.html"', 'href="/"', chunk)
    return re.sub(r'href="(?!https?:|mailto:|tel:|/|#)([^"]+)"', r'href="/\1"', chunk)


guide = open('guide-nagoya.html', encoding='utf-8').read()
NAV = absolutize(guide[guide.index('<nav class="nav"'):guide.index('</nav>') + len('</nav>')])
NAV = NAV.replace('<a href="/column/" class="nav__link">', '<a href="/column/" class="nav__link" aria-current="page">', 1)
FOOTER = absolutize(guide[guide.index('<footer'):guide.index('</footer>') + len('</footer>')])
fs = guide.index('<div class="floating-cta">')
FLOAT = guide[fs:guide.index('</div>', guide.index('</a>', fs)) + len('</div>')]

HEAD_TOP = '''<!DOCTYPE html>
<html lang="ja">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-YLCQ40CH33"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-YLCQ40CH33');
  </script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
'''
HEAD_LINKS = '''  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
  <link rel="icon" type="image/png" href="/webサイト用画像/ファビコン.png">
  <link rel="stylesheet" href="/css/style.css">
'''
TAIL = f'''
{FOOTER}

<!-- フローティングCTA -->
{FLOAT}

<script src="/js/main.js"></script>
<script src="/js/tracking.js"></script>
</body>
</html>
'''

STYLE = '''  <style>
    /* 発達コラム：読み物として行間・本文幅を優先 */
    .col-wrap { max-width: 760px; margin-inline: auto; }
    .col-back { display: inline-flex; align-items: center; gap: 6px; color: var(--juno-primary-dark); font-size: 0.875rem; font-weight: 600; margin-bottom: 32px; }
    .col-back:hover { text-decoration: underline; }
    .col-meta { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 14px; }
    .col-tag { display: inline-block; font-size: 0.75rem; font-weight: 700; color: var(--juno-primary-dark); background: var(--juno-primary-light); border-radius: 100px; padding: 3px 12px; }
    .col-date { font-family: 'Nunito', sans-serif; font-size: 0.85rem; color: var(--juno-text-sub); font-variant-numeric: tabular-nums; }
    .col-title { font-size: 1.7rem; font-weight: 700; line-height: 1.5; color: var(--juno-text); margin-bottom: 36px; text-wrap: balance; }
    .col-h2 { font-size: 1.3rem; font-weight: 700; line-height: 1.6; color: var(--juno-text); margin: 56px 0 18px; padding-bottom: 10px; border-bottom: 2px solid var(--juno-primary-light); }
    .col-h3 { font-size: 1.05rem; font-weight: 700; line-height: 1.7; color: var(--juno-text); margin: 36px 0 12px; padding-left: 12px; border-left: 3px solid var(--juno-primary); }
    .col-p { font-size: 1rem; line-height: 2.05; color: var(--juno-text); margin-bottom: 1.1em; }
    .col-sub { font-size: 1rem; line-height: 1.9; color: var(--juno-text); margin: 24px 0 6px; }
    .col-list, .col-check { margin: 8px 0 22px; display: flex; flex-direction: column; gap: 8px; }
    .col-list li, .col-check li { position: relative; padding-left: 26px; font-size: 0.98rem; line-height: 1.85; color: var(--juno-text); }
    .col-list li::before { content: ""; position: absolute; left: 8px; top: 0.78em; width: 6px; height: 6px; border-radius: 50%; background: var(--juno-primary); }
    .col-check li::before { content: ""; position: absolute; left: 2px; top: 0.42em; width: 15px; height: 15px; border: 1.5px solid var(--juno-primary); border-radius: 3px; background: var(--juno-white); }
    .col-research { background: var(--juno-bg-sub); border-left: 3px solid var(--juno-border); border-radius: 0 10px 10px 0; padding: 16px 20px; margin: 18px 0 22px; }
    .col-research p { font-size: 0.93rem; line-height: 1.95; color: var(--juno-text); }
    .col-research p + p { margin-top: 0.6em; }
    .col-research__label, .col-note__label { display: block; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; color: var(--juno-primary-dark); margin-bottom: 6px; }
    .col-note { border-left: 2px solid var(--juno-border); padding: 4px 0 4px 16px; margin: 18px 0 24px; }
    .col-note p { font-size: 0.86rem; line-height: 1.9; color: var(--juno-text-sub); }
    .col-note p + p { margin-top: 0.6em; }
    .col-note__label { color: var(--juno-text-sub); }
    .col-refs { margin-top: 64px; padding-top: 20px; border-top: 1px solid var(--juno-border); }
    .col-refs__title { font-size: 0.9rem; font-weight: 700; color: var(--juno-text); margin-bottom: 10px; }
    .col-refs li { font-size: 0.8rem; line-height: 1.8; color: var(--juno-text-sub); padding-left: 1.2em; text-indent: -1.2em; margin-bottom: 6px; word-break: break-all; }
    .col-refs a { color: var(--juno-primary-dark); }
    .col-pager { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 40px; }
    .col-pager a { display: block; border: 1px solid var(--juno-border); border-radius: 12px; padding: 14px 16px; font-size: 0.88rem; line-height: 1.7; color: var(--juno-text); background: var(--juno-white); }
    .col-pager a:hover { border-color: var(--juno-primary); }
    .col-pager__dir { display: block; font-size: 0.75rem; color: var(--juno-primary-dark); font-weight: 700; margin-bottom: 2px; }
    .col-pager__next { grid-column: 2; text-align: right; }
    .col-links { margin-top: 32px; display: flex; flex-direction: column; gap: 14px; font-size: 0.9rem; line-height: 1.9; color: var(--juno-text-sub); }
    .col-links a { color: var(--juno-primary-dark); font-weight: 600; border-bottom: 1px solid var(--juno-primary); }
    .col-sign { margin-top: 40px; padding: 18px 20px; background: var(--juno-bg); border-radius: 10px; font-size: 0.8rem; line-height: 1.9; color: var(--juno-text-sub); }
    .col-sign strong { color: var(--juno-text); }
    /* 一覧 */
    .col-lead { max-width: 760px; margin: 0 auto 36px; font-size: 0.98rem; line-height: 2; color: var(--juno-text-sub); }
    .col-lead p + p { margin-top: 0.8em; }
    .col-cards { max-width: 760px; margin-inline: auto; display: flex; flex-direction: column; gap: 16px; }
    .col-card { display: block; background: var(--juno-white); border: 1px solid var(--juno-border); border-radius: 14px; padding: 22px 26px; transition: border-color 0.2s, box-shadow 0.2s; }
    .col-card:hover { border-color: var(--juno-primary); box-shadow: var(--juno-shadow); }
    .col-card__title { font-size: 1.1rem; font-weight: 700; line-height: 1.6; color: var(--juno-text); margin: 4px 0 8px; }
    .col-card__lead { font-size: 0.9rem; line-height: 1.85; color: var(--juno-text-sub); }
    .col-card__more { display: inline-block; margin-top: 10px; font-size: 0.85rem; font-weight: 600; color: var(--juno-primary-dark); }
    @media (max-width: 768px) {
      .col-title { font-size: 1.4rem; }
      .col-h2 { font-size: 1.15rem; margin-top: 44px; }
      .col-pager { grid-template-columns: 1fr; }
      .col-pager__next { grid-column: 1; }
      .col-card { padding: 18px 18px; }
    }
  </style>
'''


def fmt_date(d):
    return d.replace('-', '.')


# ---------------------------------------------------------------- 生成
arts = sorted((parse(p) for p in glob.glob('_columns/*.md')), key=lambda a: (a['published'], a['slug']))
slugs = [a['slug'] for a in arts]
assert len(slugs) == len(set(slugs)), 'slug が重複しています'

for idx, a in enumerate(arts):
    prev_a = arts[idx - 1] if idx > 0 else None
    next_a = arts[idx + 1] if idx + 1 < len(arts) else None
    url = f"{SITE}/column/{a['slug']}.html"
    ld = {
        '@context': 'https://schema.org', '@type': 'Article',
        'headline': a['title'], 'description': a['description'],
        'datePublished': a['published'], 'dateModified': a['updated'],
        'author': {'@type': 'Organization', 'name': 'こども訪問看護ステーションJuno'},
        'publisher': {'@type': 'Organization', 'name': 'こども訪問看護ステーションJuno', 'url': SITE + '/'},
        'articleSection': '発達コラム', 'inLanguage': 'ja', 'mainEntityOfPage': url,
    }
    pager = ''
    if prev_a or next_a:
        pager = '      <nav class="col-pager" aria-label="前後の記事">\n'
        if prev_a:
            pager += f'        <a href="/column/{prev_a["slug"]}.html"><span class="col-pager__dir">← 前の記事</span>{esc(prev_a["title"])}</a>\n'
        if next_a:
            pager += f'        <a class="col-pager__next" href="/column/{next_a["slug"]}.html"><span class="col-pager__dir">次の記事 →</span>{esc(next_a["title"])}</a>\n'
        pager += '      </nav>\n'
    updated = ''
    if a['updated'] != a['published']:
        updated = f'<span class="col-date">更新 <time datetime="{a["updated"]}">{fmt_date(a["updated"])}</time></span>'
    refs = ''.join(f'<li>{link_urls(r)}</li>' for r in a['refs'])
    page = (HEAD_TOP
            + f'  <title>{esc(a["title"])} | 発達コラム | こども訪問看護ステーションJuno</title>\n'
            + f'  <meta name="description" content="{html.escape(a["description"])}">\n'
            + f'  <link rel="canonical" href="{url}">\n'
            + HEAD_LINKS
            + '  <script type="application/ld+json">\n  ' + json.dumps(ld, ensure_ascii=False, indent=2).replace('\n', '\n  ') + '\n  </script>\n'
            + STYLE + '</head>\n<body>\n\n' + NAV + '\n\n'
            + '<section class="section" style="padding-top:48px;">\n  <div class="container">\n    <div class="col-wrap">\n'
            + '      <a href="/column/" class="col-back">← 発達コラム 一覧へ</a>\n'
            + '      <article>\n'
            + f'      <div class="col-meta"><span class="col-tag">発達コラム</span><span class="col-date"><time datetime="{a["published"]}">{fmt_date(a["published"])}</time></span>{updated}</div>\n'
            + f'      <h1 class="col-title">{esc(a["title"])}</h1>\n'
            + md_to_html(a['body']) + '\n'
            + ('      <section class="col-refs" aria-label="参考文献">\n        <h2 class="col-refs__title">参考文献</h2>\n'
               f'        <ul>{refs}</ul>\n      </section>\n' if refs else '')
            + '      </article>\n'
            + pager
            + '      <div class="col-links">\n'
            + '        <p><a href="/column/">発達コラム 一覧へ ＞</a></p>\n'
            + '      </div>\n'
            + '      <div class="col-sign"><strong>こども訪問看護ステーションJuno</strong><br>'
              'このコラムは、訪問看護の現場での経験・臨床データ蓄積と、学術文献をもとに作成しています。<br>'
              '記載内容は一般的な情報であり、個々のお子さまへの対応を示すものではありません。</div>\n'
            + '    </div>\n  </div>\n</section>\n'
            + TAIL)
    open(f'column/{a["slug"]}.html', 'w', encoding='utf-8').write(page)

# 一覧
cards = ''.join(
    f'''      <a class="col-card" href="/column/{a["slug"]}.html">
        <span class="col-date"><time datetime="{a["published"]}">{fmt_date(a["published"])}</time></span>
        <h2 class="col-card__title">{esc(a["title"])}</h2>
        <p class="col-card__lead">{esc(a["lead"])}</p>
        <span class="col-card__more">読む ＞</span>
      </a>
''' for a in reversed(arts))
index = (HEAD_TOP
         + '  <title>発達コラム | こども訪問看護ステーションJuno</title>\n'
         + '  <meta name="description" content="お子さまの発達に関する困りごとについて、研究知見をもとに整理したコラムです。こども訪問看護ステーションJunoが作成しています。">\n'
         + f'  <link rel="canonical" href="{SITE}/column/">\n'
         + HEAD_LINKS + STYLE + '</head>\n<body>\n\n' + NAV + '\n\n'
         + '<div class="page-header">\n  <div class="container">\n    <div class="section__label">Column</div>\n'
         + '    <h1 class="page-header__title">発達コラム</h1>\n  </div>\n</div>\n\n'
         + '<section class="section">\n  <div class="container">\n'
         + '    <div class="col-lead">\n'
         + '      <p>お子さまの発達に関する困りごとについて、研究で明らかになっていることをもとに整理しています。</p>\n'
         + '      <p>一般的な情報であり、個々のお子さまへの対応を示すものではありませんが、ご家庭での見かたを考える材料になればと思います。</p>\n'
         + '    </div>\n'
         + '    <div class="col-cards">\n' + cards + '    </div>\n'
         + '  </div>\n</section>\n'
         + TAIL)
open('column/index.html', 'w', encoding='utf-8').write(index)

# サイトマップ
sm = open('sitemap.xml', encoding='utf-8').read()


def upsert(sm, loc, lastmod, priority):
    pat = re.compile(r'  <url>\s*<loc>' + re.escape(loc) + r'</loc>.*?</url>\n', re.S)
    entry = f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <priority>{priority}</priority>\n  </url>\n'
    if pat.search(sm):
        return pat.sub(entry, sm)
    return sm.replace('</urlset>', entry + '</urlset>')


latest = max(a['updated'] for a in arts)
sm = upsert(sm, f'{SITE}/column/', latest, '0.7')
for a in reversed(arts):
    sm = upsert(sm, f'{SITE}/column/{a["slug"]}.html', a['updated'], '0.6')
open('sitemap.xml', 'w', encoding='utf-8').write(sm)

print(f'生成: column/index.html ＋ {len(arts)}記事', [a['slug'] for a in arts])
