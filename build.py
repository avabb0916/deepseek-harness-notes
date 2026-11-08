#!/usr/bin/env python3
"""把 dsh-series/03-文章 的 24 篇笔记，构建成可直接放 GitHub Pages 的静态电子书。
用法：python3 dsh-book/build.py
产物：dsh-book/docs/{index.html,ch01..24.html,images/*}
"""
import re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERIES = ROOT / 'dsh-series'
ART = SERIES / '03-文章'
DOCS = Path(__file__).resolve().parent / 'docs'
CONV = ROOT / 'tools' / 'dsh_series_html.py'

def fm_of(text):
    fm = {}
    if text.startswith('---'):
        end = text.find('\n---', 3)
        for line in text[3:end].splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                fm[k.strip()] = v.strip()
    return fm

def main():
    shutil.rmtree(DOCS, ignore_errors=True)
    (DOCS / 'images').mkdir(parents=True)
    files = sorted([p for p in ART.glob('[0-9][0-9]-*.md')
                    if not p.name.startswith(('00-', '99-'))])
    if not files:
        sys.exit('no articles')
    chapters = []
    for p in files:
        text = p.read_text(encoding='utf-8')
        fm = fm_of(text)
        num = p.name[:2]
        title = fm.get('title') or p.stem
        out = DOCS / f'ch{num}.html'
        subprocess.run([sys.executable, str(CONV), str(p), str(out)], check=True,
                       stdout=subprocess.DEVNULL)
        chapters.append({'num': num, 'title': title, 'file': out.name})
    # 注入导航
    for i, c in enumerate(chapters):
        prev = chapters[i-1] if i > 0 else None
        nxt = chapters[i+1] if i < len(chapters)-1 else None
        left = f'<a href="{prev["file"]}">← {prev["num"]} {prev["title"]}</a>' if prev else '<span></span>'
        right = f'<a href="{nxt["file"]}">{nxt["num"]} {nxt["title"]} →</a>' if nxt else '<span></span>'
        nav = (f'<div class="booknav">{left}<a href="index.html">目录</a>{right}</div>')
        css = ('<style>.booknav{max-width:1080px;margin:0 auto;padding:14px 40px;'
               'display:flex;justify-content:space-between;gap:16px;'
               'font-family:ui-sans-serif,-apple-system,"PingFang SC",sans-serif;font-size:13px;'
               'border-bottom:1px solid #ddd7c9;color:#6d685f}'
               '.booknav a{color:#1f4e5f;text-decoration:none}.booknav a:hover{text-decoration:underline}'
               '@media print{.booknav{display:none}}</style>')
        html = (DOCS / c['file']).read_text(encoding='utf-8')
        html = html.replace('</head>', css + '</head>', 1)
        html = html.replace('<body>', '<body>' + nav, 1)
        (DOCS / c['file']).write_text(html, encoding='utf-8')
    # 学习计划页
    plan_md = SERIES / '07-排期' / '一周学习+两周发布-v1.0.md'
    if plan_md.exists():
        subprocess.run([sys.executable, str(CONV), str(plan_md), str(DOCS / 'plan.html')],
                       check=True, stdout=subprocess.DEVNULL)
        html = (DOCS / 'plan.html').read_text(encoding='utf-8')
        html = html.replace('<body>', '<body><div class="booknav" style="max-width:1080px;margin:0 auto;padding:14px 40px;font-size:13px;border-bottom:1px solid #ddd7c9"><a href="index.html" style="color:#1f4e5f">← 回目录</a></div>', 1)
        (DOCS / 'plan.html').write_text(html, encoding='utf-8')
    # 案例路线图
    cases_md = SERIES / '09-案例' / '00-案例路线图.md'
    if cases_md.exists():
        subprocess.run([sys.executable, str(CONV), str(cases_md), str(DOCS / 'cases.html')],
                       check=True, stdout=subprocess.DEVNULL)
        html = (DOCS / 'cases.html').read_text(encoding='utf-8')
        html = html.replace('<body>', '<body><div class="booknav" style="max-width:1080px;margin:0 auto;padding:14px 40px;font-size:13px;border-bottom:1px solid #ddd7c9"><a href="index.html" style="color:#1f4e5f">← 回目录</a></div>', 1)
        (DOCS / 'cases.html').write_text(html, encoding='utf-8')
    # 图片
    ov = Path(__file__).resolve().parent / 'assets' / 'overview.png'
    if ov.exists():
        shutil.copy2(ov, DOCS / 'images' / '00-全景图.png')
    for png in sorted((ART / '配图').glob('*.png')):
        shutil.copy2(png, DOCS / 'images' / png.name)
    # 首页
    toc = '\n'.join(
        f'<li><a href="{c["file"]}"><b>{c["num"]}</b> {c["title"]}</a></li>' for c in chapters)
    gallery = '\n'.join(
        f'<figure><img src="images/{png.name}" alt="{png.stem}"><figcaption>{png.stem}</figcaption></figure>'
        for png in sorted((DOCS / 'images').glob('*.png')))
    index = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>一切皆插件 · DeepSeek Harness 学习笔记</title>
<style>
:root{{--ink:#1b1a17;--muted:#6d685f;--line:#ddd7c9;--paper:#fbf9f3;--accent:#b23a2a;--accent2:#1f4e5f}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);
font-family:ui-serif,"Songti SC","Noto Serif CJK SC",Georgia,serif;line-height:1.8;font-size:17px}}
.page{{max-width:1080px;margin:0 auto;padding:56px 40px 80px}}
.kicker{{font-family:ui-sans-serif,-apple-system,"PingFang SC",sans-serif;font-size:12px;letter-spacing:.18em;color:var(--accent);font-weight:700}}
h1{{font-size:40px;line-height:1.25;margin:12px 0 14px}}h2{{font-size:24px;margin:44px 0 14px;padding-top:14px;border-top:1px solid var(--line)}}
.meta{{font-family:ui-sans-serif,-apple-system,"PingFang SC",sans-serif;font-size:13px;color:var(--muted)}}
blockquote{{margin:22px 0;padding:16px 20px;background:#f7efe2;border-left:4px solid var(--accent);color:#3f3a33}}
ul.toc{{padding-left:0;list-style:none;columns:2;column-gap:40px}}ul.toc li{{margin:8px 0;break-inside:avoid;font-size:15px}}
ul.toc a{{color:var(--accent2);text-decoration:none}}ol.toc a:hover{{text-decoration:underline}}
.gallery{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px}}
.gallery figure{{margin:0;background:#fff;border:1px solid var(--line);border-radius:8px;padding:10px}}
.gallery img{{width:100%;height:auto;display:block;border-radius:4px}}
.gallery figcaption{{font-family:ui-sans-serif,-apple-system,"PingFang SC",sans-serif;font-size:12px;color:var(--muted);margin-top:8px;text-align:center}}
footer{{margin-top:56px;padding-top:18px;border-top:3px solid var(--ink);font-family:ui-sans-serif,-apple-system,"PingFang SC",sans-serif;font-size:12.5px;color:var(--muted)}}
@media print{{.gallery{{grid-template-columns:repeat(2,1fr)}}}}
</style></head><body><div class="page">
<div class="kicker">DSH · 学习笔记</div>
<h1>一切皆插件<br>我的 DeepSeek Harness 学习笔记</h1>
<div class="meta">24 篇 ｜ 版本 v1.1 ｜ 2026-11-08 ｜ 依据：本机 dsh 0.2.2-rc.1 实测 + 官方文档 + X/社区资料</div>
<img src="images/00-全景图.png" alt="教程全景图" style="width:100%;height:auto;margin:26px 0 6px;border:1px solid var(--line);border-radius:10px">
<blockquote>这不是教程，是我从 0 到 1 学 DeepSeek Harness 的笔记。我先学会，才发出来；看不懂的地方，我写"我还没搞懂"。</blockquote>
<h2>怎么用这本笔记</h2>
<p>1. 从第 01 篇开始读，每篇顶部有「我带着的问题」和「读完能答的三个问题」；答不出，就回去重读那一节。<br>
2. 想动手的，按 <a href="plan.html">7 天学习 + 14 天发布计划</a> 每天读 2—4 篇 + 做 1 件小事。<br>
3. 每篇文末有「术语小抄」和「我还没搞懂」，看不懂术语先看小抄。</p>
<h2>目录（26 篇）</h2>
<ul class="toc">{toc}</ul>
<h2>第二批：案例（在写）</h2>
<p>24 篇讲机制，第二批讲"用它做成了什么"。六个案例的路线图：<a href="cases.html">案例篇路线图</a>。</p>
<h2>配图</h2>
<p>全部配图为手绘白底风格，可单独保存使用（19 张）。</p>
<div class="gallery">{gallery}</div>
<footer>版本 v1.0 ｜ 2026-11-08 ｜ 依据：dsh-series/03-文章 24 篇 ｜ 本机 dsh 0.2.2-rc.1</footer>
</div></body></html>'''
    (DOCS / 'index.html').write_text(index, encoding='utf-8')
    (DOCS / '.nojekyll').write_text('', encoding='utf-8')
    print(f'built {len(chapters)} chapters, {len(list((DOCS/"images").glob("*.png")))} images')

if __name__ == '__main__':
    main()
