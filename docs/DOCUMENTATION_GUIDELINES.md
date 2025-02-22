# Documentation Guidelines / 文档规范指南

## Overview / 概述

This document outlines the documentation standards for the Gomoku World project, with a focus on maintaining bilingual (English and Chinese) documentation.

本文档概述了五子棋世界项目的文档标准，重点关注双语（英文和中文）文档的维护。

## General Principles / 一般原则

1. All documentation must be bilingual (English and Chinese) / 所有文档必须双语（英文和中文）
2. English text comes first, followed by Chinese / 英文在前，中文在后
3. Use clear and concise language in both languages / 两种语言都要使用清晰简洁的表达

## Code Documentation / 代码文档

### Docstrings / 文档字符串
```python
"""
English description here.

中文描述在这里。
"""
```

### Comments / 注释
```python
# English comment here / 中文注释在这里

# For longer comments / 对于较长的注释：
# English:
#   Detailed explanation here
# 中文：
#   详细解释在这里
```

## File Headers / 文件头部

Every source file should include a bilingual header:

```python
"""
Gomoku World - [Module Name]
[Brief description in English]

五子棋世界 - [模块名称]
[中文简要描述]
"""
```

## Documentation Files / 文档文件

### Markdown Files / Markdown 文件

Use headers in both languages:
```markdown
# Title / 标题

## Subtitle / 副标题

Content in English.

中文内容。
```

### Release Notes / 版本说明

Maintain separate files for different audiences:
- `v1.x.x.user.md` and `v1.x.x.user.zh-CN.md`
- `v1.x.x.dev.beginner.md` and `v1.x.x.dev.beginner.zh-CN.md`
- `v1.x.x.dev.professional.md` and `v1.x.x.dev.professional.zh-CN.md`

## Translation Management / 翻译管理

### Key Naming / 键名命名
- Use descriptive English keys
- Follow the format: `category.subcategory.name`
- Example: `game.menu.start`

### Translation Files / 翻译文件
- Organize by language and category
- Use JSON format
- Include comments for context

## Review Process / 审查流程

1. Documentation changes must be reviewed for both languages / 文档更改必须对两种语言都进行审查
2. Ensure consistency across all related files / 确保所有相关文件的一致性
3. Verify technical accuracy in both languages / 验证两种语言的技术准确性

## Tools and Resources / 工具和资源

### Recommended Tools / 推荐工具
- Translation memory tools / 翻译记忆工具
- Markdown editors / Markdown 编辑器
- Spell checkers / 拼写检查器

### Style Guides / 风格指南
- Follow PEP 257 for docstrings / 遵循 PEP 257 的文档字符串规范
- Follow Chinese documentation standards / 遵循中文文档标准

## Maintenance / 维护

### Regular Reviews / 定期审查
- Review documentation quarterly / 每季度审查文档
- Update translations as needed / 根据需要更新翻译
- Remove obsolete content / 删除过时内容

### Version Control / 版本控制
- Document all changes in commit messages / 在提交信息中记录所有更改
- Use appropriate tags for documentation updates / 使用适当的标签进行文档更新
- Maintain change history / 维护更改历史

## Questions and Support / 问题和支持

For questions or support regarding documentation:
- Create an issue with the "documentation" label
- Contact the documentation team

关于文档的问题或支持：
- 创建带有"documentation"标签的问题
- 联系文档团队 