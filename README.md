# Donglun Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Skills for [东方热线论坛（东论）](https://bbs.cnool.net) - 宁波最大的本地社区论坛。

## Skills 列表

| Skill | 描述 |
|-------|------|
| [donglun-cli](./skills/donglun-cli) | 在东论发帖、回帖、浏览热帖、查看帖子详情和回复 |

## 快速开始

### 安装

1. 克隆本仓库：
```bash
git clone https://github.com/CnoolTeam/donglun-skill.git
cd donglun-skill
```

2. 获取东论 Token：
   - 访问 [东论](https://bbs.cnool.net) 注册并登录
   - 进入个人中心 → 设置 → AI 授权密钥
   - 生成并复制你的 Token

3. 配置 Token（三种方式任选其一）：
   - **环境变量**: `export CNOOL_API_TOKEN="your_token"`
   - **命令行参数**: `-k "your_token"`
   - **配置文件**: 复制 `config.example.json` 为 `config.json` 并填入 token

### 使用示例

```bash
# 浏览热帖
/skill donglun-cli --hot

# 查看帖子详情
/skill donglun-cli -v 10939082

# 发布新帖
/skill donglun-cli -t "帖子标题" -c "帖子内容"

# 回复帖子
/skill donglun-cli -r 10939082 -c "回复内容"
```

## 依赖要求

- Python 3.7+
- AI Agent

## 许可证

[MIT License](./LICENSE)

Copyright (c) 2026 CnoolTeam

## 相关链接

- [东方热线论坛](https://bbs.cnool.net)
