#!/usr/bin/env python3.12
"""TUOJ HTML -> Markdown 转换脚本

把从 TUOJ (ai.tuoj.thusaac.com / oj.cs.tsinghua.edu.cn) 保存的
'作业 - 题目 - TUOJ.html' 转成干净的 Markdown 文件。

用法:
    python3.12 tuoj_html2md.py <html文件或目录> [输出目录]

    - 传文件: 转换单个 HTML，输出到同目录或指定目录
    - 传目录: 递归查找所有 *TUOJ.html，批量转换
"""

import sys
import os
import re
import html
import zipfile
import urllib.request
from bs4 import BeautifulSoup
from markdownify import markdownify as md


def convert_tuoj_html(html_path, output_dir=None):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取题目标题
    title_m = re.search(r'<div class="page-header"><h1>(.*?)</h1>', content)
    title = title_m.group(1) if title_m else 'Untitled'

    # 提取 <markdown> 标签内的内容
    m = re.search(r'<markdown[^>]*>(.*?)</markdown>', content, re.DOTALL)
    if not m:
        print(f"  跳过 (未找到 <markdown> 标签): {html_path}")
        return None

    inner = m.group(1)

    # 移除复制按钮 overlay
    inner = re.sub(
        r'<div style="position: absolute[^"]*"[^>]*>.*?</div></div>',
        '', inner, flags=re.DOTALL
    )
    # 移除 <copy-button> 标签
    inner = re.sub(r'<copy-button[^>]*>.*?</copy-button>', '', inner, flags=re.DOTALL)

    # 用 BeautifulSoup 精确替换 KaTeX span (嵌套结构复杂，正则无法可靠匹配)
    soup = BeautifulSoup(inner, 'html.parser')
    for katex_span in soup.find_all('span', class_='katex'):
        ann = katex_span.find('annotation', encoding='application/x-tex')
        latex = html.unescape(ann.string.strip()) if ann and ann.string else ''
        katex_span.replace_with(f'${latex}$')

    inner = str(soup)

    # KaTeX 块 -> $$ ... $$
    inner = re.sub(
        r'<katex-mathblock[^>]*>(.*?)</katex-mathblock>',
        lambda m: '\n$$\n' + m.group(1).strip() + '\n$$\n',
        inner, flags=re.DOTALL
    )
    # KaTeX 行内 -> $ ... $
    inner = re.sub(
        r'<katex-mathinline[^>]*>(.*?)</katex-mathinline>',
        lambda m: '$' + m.group(1).strip() + '$',
        inner, flags=re.DOTALL
    )

    # 转换
    result = md(inner, heading_style='ATX', code_language='')

    # 加标题
    result = f'# {title}\n\n{result}'

    # 清理多余空行 (最多保留两个连续空行)
    result = re.sub(r'\n{3,}', '\n\n', result)
    result = result.strip() + '\n'

    # 确定输出路径
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        out_path = os.path.join(output_dir, title + '.md')
    else:
        out_path = os.path.splitext(html_path)[0] + '.md'

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f'  -> {out_path}')

    # 下载附件
    attachment_dir = os.path.dirname(html_path)
    links = re.findall(
        r'href="(https?://[^"]*(?:download|std|\.zip)[^"]*)"', inner
    )
    # 也匹配 <markdown> 原始内容中的链接 (BeautifulSoup 替换后 inner 已改变，从 soup 重新提取)
    link_soup = BeautifulSoup(m.group(1), 'html.parser')
    for a_tag in link_soup.find_all('a', href=True):
        href = a_tag['href']
        if href not in links and ('download' in href.lower() or '.zip' in href.lower() or '/std' in href.lower()):
            links.append(href)

    for url in links:
        fname = url.split('/')[-1]
        if fname == 'downloads.zip':
            fname = url.split('/')[-2].replace('.downloads.zip', '') + '_downloads.zip'
        dest = os.path.join(attachment_dir, fname)
        if os.path.exists(dest):
            print(f'  附件已存在，跳过: {fname}')
            continue
        try:
            print(f'  下载: {fname} ...', end=' ', flush=True)
            urllib.request.urlretrieve(url, dest)
            size = os.path.getsize(dest)
            print(f'{size} bytes')
            # 如果是 zip 且目录里没有同名的解压文件，自动解压
            if zipfile.is_zipfile(dest):
                with zipfile.ZipFile(dest, 'r') as zf:
                    members = [n for n in zf.namelist() if not n.startswith('__MACOSX')]
                    # 检查是否已经有解压后的文件
                    need_extract = any(not os.path.exists(os.path.join(attachment_dir, n)) for n in members)
                    if need_extract:
                        for n in members:
                            zf.extract(n, attachment_dir)
                        print(f'    解压: {", ".join(members)}')
        except Exception as e:
            print(f'失败: {e}')

    return out_path


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    target = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    if os.path.isfile(target):
        print(f'转换: {target}')
        convert_tuoj_html(target, output_dir)
    elif os.path.isdir(target):
        count = 0
        for root, dirs, files in os.walk(target):
            for fname in files:
                if 'TUOJ' in fname and fname.endswith('.html'):
                    fpath = os.path.join(root, fname)
                    print(f'转换: {fpath}')
                    convert_tuoj_html(fpath, output_dir)
                    count += 1
        print(f'\n共转换 {count} 个文件')
    else:
        print(f'找不到: {target}')
        sys.exit(1)


if __name__ == '__main__':
    main()
