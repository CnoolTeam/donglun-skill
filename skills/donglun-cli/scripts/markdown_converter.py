#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 到 HTML 转换器
支持标准 Markdown 语法，自动添加内联样式
"""

import re
from typing import Dict

# 尝试导入 markdown 库，如果没有则使用简单的正则转换
try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False


def markdown_to_html(content: str) -> str:
    """
    将 Markdown 格式转换为 HTML，并添加内联样式
    优先使用 markdown 库，如果没有安装则使用简单的正则转换
    """
    if MARKDOWN_AVAILABLE:
        # 预处理：在文本和列表之间插入空行，让 markdown 库能正确识别列表
        content = _preprocess_lists(content)

        # 使用 markdown 库进行转换
        html = markdown.markdown(content, extensions=['tables', 'fenced_code'])
        html = add_inline_styles(html)
        return html
    else:
        # 简单的正则转换（基础 Markdown 语法），直接生成带样式的 HTML
        return convert_markdown_with_styles(content)


def _preprocess_lists(content: str) -> str:
    """
    预处理：在文本和列表之间插入空行
    让 markdown 库能正确识别列表
    """
    lines = content.split('\n')
    new_lines = []
    for i, line in enumerate(lines):
        new_lines.append(line)
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            current_line = line.strip()
            # 如果当前行不是列表，下一行是列表，且它们之间没有空行
            if (current_line and
                not current_line.startswith('- ') and
                not current_line.startswith('* ') and
                not re.match(r'^\d+\.\s', current_line) and
                not current_line.startswith('#') and
                not current_line.startswith('>') and
                not current_line.startswith('```') and
                not current_line.startswith('|') and
                (next_line.startswith('- ') or
                 next_line.startswith('* ') or
                 re.match(r'^\d+\.\s', next_line))):
                # 插入空行
                new_lines.append('')
    return '\n'.join(new_lines)


def add_inline_styles(html: str) -> str:
    """
    为已转换的 HTML 添加内联样式
    处理 markdown 库生成的 HTML
    """
    # 表格样式 - 边框实线黑色1像素
    html = re.sub(r'<table>', r'<table style="border-collapse:collapse;border:1px solid black;width:100%;">', html)
    html = re.sub(r'<th>', r'<th style="border:1px solid black;padding:8px;background-color:#f2f2f2;font-weight:bold;">', html)
    # 处理 <td> - 避免重复添加 style
    html = re.sub(r'<td(?![^>]*style=)[^>]*>', r'<td style="border:1px solid black;padding:8px;">', html)

    # 代码块样式
    html = re.sub(r'<pre>', r'<pre style="background-color:#f5f5f5;border:1px solid #ddd;border-radius:3px;padding:10px;overflow-x:auto;">', html)
    html = re.sub(r'<code>', r'<code style="font-family:Consolas,Monaco,monospace;font-size:14px;">', html)

    # 行内代码样式
    html = re.sub(r'`([^`]+)`', r'<code style="background-color:#f5f5f5;padding:2px 4px;border-radius:3px;font-family:Consolas,Monaco,monospace;font-size:14px;">\1</code>', html)

    # 标题样式
    html = re.sub(r'<h1>', r'<h1 style="font-size:28px;font-weight:bold;color:#333;margin:20px 0 10px 0;">', html)
    html = re.sub(r'<h2>', r'<h2 style="font-size:24px;font-weight:bold;color:#444;margin:18px 0 9px 0;">', html)
    html = re.sub(r'<h3>', r'<h3 style="font-size:20px;font-weight:bold;color:#555;margin:16px 0 8px 0;">', html)
    html = re.sub(r'<h4>', r'<h4 style="font-size:18px;font-weight:bold;color:#666;margin:14px 0 7px 0;">', html)
    html = re.sub(r'<h5>', r'<h5 style="font-size:16px;font-weight:bold;color:#777;margin:12px 0 6px 0;">', html)
    html = re.sub(r'<h6>', r'<h6 style="font-size:14px;font-weight:bold;color:#888;margin:10px 0 5px 0;">', html)

    # 引用块样式
    html = re.sub(r'<blockquote>', r'<blockquote style="border-left:4px solid #ddd;padding-left:16px;margin:10px 0;color:#666;font-style:italic;">', html)

    # 链接样式
    html = re.sub(r'<a ', r'<a style="color:#0066cc;text-decoration:none;" ', html)
    html = re.sub(r'<a>', r'<a style="color:#0066cc;text-decoration:none;">', html)

    # 水平线样式
    html = re.sub(r'<hr>', r'<hr style="border:none;border-top:1px solid #ddd;margin:20px 0;">', html)

    # 列表样式 - 添加 list-style-type
    # 分别处理 ul 和 ol 块中的 li
    def style_ul_list(match):
        content = match.group(1)
        # 给 ul 中的 li 添加 disc 样式
        content = re.sub(r'<li>', r'<li style="margin:5px 0;list-style-type:disc;">', content)
        return f'<ul style="margin:10px 0;padding-left:20px;list-style-type:disc;">{content}</ul>'

    def style_ol_list(match):
        content = match.group(1)
        # 给 ol 中的 li 添加 decimal 样式
        content = re.sub(r'<li>', r'<li style="margin:5px 0;list-style-type:decimal;">', content)
        return f'<ol style="margin:10px 0;padding-left:20px;list-style-type:decimal;">{content}</ol>'

    # 先处理 ul
    html = re.sub(r'<ul[^>]*>(.*?)</ul>', style_ul_list, html, flags=re.DOTALL)
    # 再处理 ol
    html = re.sub(r'<ol[^>]*>(.*?)</ol>', style_ol_list, html, flags=re.DOTALL)

    # 段落样式
    html = re.sub(r'<p>', r'<p style="margin:10px 0;line-height:1.6;">', html)

    # 图片样式
    html = re.sub(r'<img ', r'<img style="max-width:100%;height:auto;display:block;margin:10px 0;" ', html)

    return html


def convert_markdown_with_styles(content: str) -> str:
    """
    使用正则转换 Markdown 到 HTML，并直接添加内联样式
    关键：按顺序处理，先处理多行块级元素，再处理段落
    """
    # 按行分割，方便处理
    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 空行跳过
        if not stripped:
            i += 1
            continue

        # 代码块 (```)
        if stripped.startswith('```'):
            i = _process_code_block(lines, i, result)
            continue

        # 标题 (# ## ### #### ##### ######)
        if stripped.startswith('#'):
            i = _process_heading(lines, i, result)
            continue

        # 无序列表 (- item 或 * item)
        if stripped.startswith('- ') or stripped.startswith('* '):
            i = _process_unordered_list(lines, i, result)
            continue

        # 有序列表 (1. item)
        if re.match(r'^\d+\.\s', stripped):
            i = _process_ordered_list(lines, i, result)
            continue

        # 引用 (> text)
        if stripped.startswith('> '):
            i = _process_blockquote(lines, i, result)
            continue

        # 水平分隔线 (--- 或 *** 或 ___)
        if re.match(r'^(---+|\*\*\*|___)\s*$', stripped):
            result.append('<hr style="border:none;border-top:1px solid #ddd;margin:20px 0;">')
            i += 1
            continue

        # 表格
        if '|' in stripped and i + 1 < len(lines) and '|' in lines[i + 1]:
            i = _process_table(lines, i, result)
            continue

        # 普通段落
        i = _process_paragraph(lines, i, result)

    return '\n\n'.join(result)


def _process_code_block(lines, i, result):
    """处理代码块"""
    code_lines = []
    i += 1
    while i < len(lines) and not lines[i].strip().startswith('```'):
        code_lines.append(lines[i])
        i += 1
    code_content = '\n'.join(code_lines)
    result.append(f'<pre style="background-color:#f5f5f5;border:1px solid #ddd;border-radius:3px;padding:10px;overflow-x:auto;"><code style="font-family:Consolas,Monaco,monospace;font-size:14px;">{code_content}</code></pre>')
    return i + 1


def _process_heading(lines, i, result):
    """处理标题"""
    stripped = lines[i].strip()
    level = len(stripped) - len(stripped.lstrip('#'))
    if 1 <= level <= 6 and stripped[level:level+1] == ' ':
        text = stripped[level+1:].strip()
        sizes = {1: '28px', 2: '24px', 3: '20px', 4: '18px', 5: '16px', 6: '14px'}
        colors = {1: '#333', 2: '#444', 3: '#555', 4: '#666', 5: '#777', 6: '#888'}
        margins = {1: '20px 0 10px 0', 2: '18px 0 9px 0', 3: '16px 0 8px 0', 4: '14px 0 7px 0', 5: '12px 0 6px 0', 6: '10px 0 5px 0'}
        result.append(f'<h{level} style="font-size:{sizes[level]};font-weight:bold;color:{colors[level]};margin:{margins[level]};">{text}</h{level}>')
    return i + 1


def _process_unordered_list(lines, i, result):
    """处理无序列表"""
    list_items = []
    while i < len(lines):
        list_line = lines[i].strip()
        if list_line.startswith('- ') or list_line.startswith('* '):
            item_text = list_line[2:].strip()
            item_text = process_inline(item_text)
            list_items.append(f'<li style="margin:5px 0;list-style-type:disc;">{item_text}</li>')
            i += 1
        elif list_line == '':
            i += 1
            continue
        else:
            break
    result.append(f'<ul style="margin:10px 0;padding-left:20px;list-style-type:disc;">{"".join(list_items)}</ul>')
    return i


def _process_ordered_list(lines, i, result):
    """处理有序列表"""
    list_items = []
    while i < len(lines):
        list_line = lines[i].strip()
        match = re.match(r'^(\d+)\.\s+(.+)$', list_line)
        if match:
            item_text = match.group(2).strip()
            item_text = process_inline(item_text)
            list_items.append(f'<li style="margin:5px 0;list-style-type:decimal;">{item_text}</li>')
            i += 1
        elif list_line == '':
            i += 1
            continue
        else:
            break
    result.append(f'<ol style="margin:10px 0;padding-left:20px;list-style-type:decimal;">{"".join(list_items)}</ol>')
    return i


def _process_blockquote(lines, i, result):
    """处理引用块"""
    quote_lines = []
    while i < len(lines) and lines[i].strip().startswith('> '):
        quote_lines.append(lines[i].strip()[2:])
        i += 1
    quote_text = ' '.join(quote_lines)
    quote_text = process_inline(quote_text)
    result.append(f'<blockquote style="border-left:4px solid #ddd;padding-left:16px;margin:10px 0;color:#666;font-style:italic;">{quote_text}</blockquote>')
    return i


def _process_table(lines, i, result):
    """处理表格"""
    stripped = lines[i].strip()
    next_line = lines[i + 1].strip() if i + 1 < len(lines) else ''

    # 检查是否是表格分隔行 (|------|------|)
    if re.match(r'^\|[-:\s|]+\|$', next_line) or re.match(r'^\|[-:\s|]+$', next_line):
        # 构建表头
        header_cells = [c.strip() for c in stripped.split('|') if c.strip()]
        header_html = ''.join([f'<th style="border:1px solid black;padding:8px;background-color:#f2f2f2;font-weight:bold;">{c}</th>' for c in header_cells])
        header_row = f'<tr>{header_html}</tr>'

        # 跳过分隔行
        i += 2

        # 读取数据行
        body_rows = []
        while i < len(lines) and '|' in lines[i]:
            row_line = lines[i].strip()
            cells = [c.strip() for c in row_line.split('|') if c.strip()]
            if cells:
                row_html = ''.join([f'<td style="border:1px solid black;padding:8px;">{c}</td>' for c in cells])
                body_rows.append(f'<tr>{row_html}</tr>')
            i += 1

        table_html = f'<table style="border-collapse:collapse;border:1px solid black;width:100%;"><thead>{header_row}</thead><tbody>{"".join(body_rows)}</tbody></table>'
        result.append(table_html)
        return i

    # 不是表格，作为普通行返回
    return i


def _process_paragraph(lines, i, result):
    """处理普通段落"""
    para_lines = []
    while i < len(lines):
        stripped_line = lines[i].strip()

        # 空行停止
        if stripped_line == '':
            i += 1
            break

        # 如果遇到其他块级元素，停止
        if (stripped_line.startswith('#') or
            stripped_line.startswith('- ') or
            stripped_line.startswith('* ') or
            stripped_line.startswith('> ') or
            stripped_line.startswith('```') or
            stripped_line.startswith('|') or
            re.match(r'^\d+\.\s', stripped_line) or
            re.match(r'^(---+|\*\*\*|___)\s*$', stripped_line)):
            break

        para_lines.append(lines[i])
        i += 1

        # 检查下一行是否是列表项，如果是则停止段落
        if i < len(lines):
            next_line = lines[i].strip()
            if (next_line.startswith('- ') or
                next_line.startswith('* ') or
                re.match(r'^\d+\.\s', next_line)):
                break

    if para_lines:
        para_text = ' '.join(para_lines)
        para_text = process_inline(para_text)
        result.append(f'<p style="margin:10px 0;line-height:1.6;">{para_text}</p>')

    if not para_lines:
        i += 1

    return i


def process_inline(text: str) -> str:
    """处理行内元素"""
    # 粗体 (**text**)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)

    # 斜体 (*text*)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)

    # 删除线 (~~text~~)
    text = re.sub(r'~~(.+?)~~', r'<del>\1</del>', text)

    # 行内代码 (`code`)
    text = re.sub(r'`([^`]+)`', r'<code style="background-color:#f5f5f5;padding:2px 4px;border-radius:3px;font-family:Consolas,Monaco,monospace;font-size:14px;">\1</code>', text)

    # 链接 [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color:#0066cc;text-decoration:none;">\1</a>', text)

    # 图片 ![alt](url)
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" style="max-width:100%;height:auto;display:block;margin:10px 0;">', text)

    return text
