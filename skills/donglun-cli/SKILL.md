---
name: donglun-cli
description: 在东方热线论坛（东论）发帖、回帖、浏览热帖、查看帖子和回复。支持 Markdown 格式，token 通过环境变量或配置文件读取。
allowed-tools: Read, Bash(cd *), Bash(python:scripts/post_donglun.py *)
---

# 东论发帖/回帖/浏览 Skill

Token 通过环境变量 `CNOOL_API_TOKEN` 或 `config.json` 配置。

## 使用方式

### 浏览热帖

```bash
# 获取最近7天热帖（默认）
python scripts/post_donglun.py --hot

# 获取最近3天热帖
python scripts/post_donglun.py --hot -d 3

# 分页浏览
python scripts/post_donglun.py --hot -p 2 -s 50
```

### 查看帖子详情

```bash
python scripts/post_donglun.py -v 10939082
```

### 查看回复列表

```bash
# 查看帖子的所有回复
python scripts/post_donglun.py --replies 10939082

# 分页查看
python scripts/post_donglun.py --replies 10939082 -p 2 -s 50
```

### 发帖

```bash
# 发帖（需要提供标题）
python scripts/post_donglun.py -t "帖子标题" -c "帖子内容"

# 从文件读取内容
python scripts/post_donglun.py -t "长文分享" -c @article.txt

# Markdown 格式发帖（自动转换为 HTML）
python scripts/post_donglun.py -t "Markdown 测试" -c "**粗体** 和 *斜体*" -m

# 从 Markdown 文件读取并转换
python scripts/post_donglun.py -t "技术分享" -c @article.md -m
```

### 回帖

```bash
# 回复指定帖子
python scripts/post_donglun.py -r "10939082" -c "回复内容"

# 从文件读取内容
python scripts/post_donglun.py -r "10939082" -c @reply.txt

# Markdown 格式回复
python scripts/post_donglun.py -r "10939082" -c "**粗体回复**" -m
```

## Markdown 支持

使用 `-m` 或 `--markdown` 参数启用 Markdown 格式转换：

- 转换后的 HTML 会自动添加内联样式
- 表格带黑色实线边框
- 支持标题、粗体、斜体、链接、图片、列表、引用、代码块等常见语法

支持的 Markdown 语法：
- `# 标题` - 标题
- `**粗体**` / `*斜体*` - 文字格式
- `` `代码` `` - 行内代码
- ` ```代码块``` ` - 代码块
- `- 列表项` / `1. 列表项` - 列表
- `> 引用` - 引用
- `| 表格 |` - 表格
- `[链接](url)` / `![图片](url)` - 链接和图片
