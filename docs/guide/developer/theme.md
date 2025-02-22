# Theme Development Guide / 主题开发指南

## Overview / 概述
This guide explains how to create and customize themes for GomokuWorld.
本指南说明如何为GomokuWorld创建和自定义主题。

## Theme Structure / 主题结构

### Configuration Format / 配置格式
```json
{
  "name": "string",           // Theme name / 主题名称
  "version": "string",        // Theme version / 主题版本
  "author": "string",         // Theme author / 主题作者
  "description": "string",    // Theme description / 主题描述
  "colors": {},              // Color definitions / 颜色定义
  "fonts": {},              // Font definitions / 字体定义
  "assets": {},             // Asset paths / 资源路径
  "styles": {}              // Style definitions / 样式定义
}
```

### Color Schemes / 配色方案
- Primary colors / 主要颜色
  - Background / 背景色
  - Foreground / 前景色
  - Accent / 强调色

- Game colors / 游戏颜色
  - Board / 棋盘
  - Grid lines / 网格线
  - Black pieces / 黑子
  - White pieces / 白子
  - Last move marker / 最后落子标记
  - Win line / 胜利线

- UI colors / 界面颜色
  - Button colors / 按钮颜色
  - Text colors / 文本颜色
  - Border colors / 边框颜色
  - Menu colors / 菜单颜色

### Asset Organization / 资源组织
- Directory structure / 目录结构
```
themes/
  ├── default/              # Default theme / 默认主题
  │   ├── config.json      # Theme configuration / 主题配置
  │   ├── assets/          # Theme assets / 主题资源
  │   │   ├── images/      # Image assets / 图片资源
  │   │   ├── sounds/      # Sound assets / 音效资源
  │   │   └── fonts/       # Font assets / 字体资源
  │   └── styles/          # Style definitions / 样式定义
  └── custom/              # Custom themes / 自定义主题
      └── ...
```

### Font Management / 字体管理
- Font loading / 字体加载
- Font fallbacks / 字体回退
- Font scaling / 字体缩放
- Multi-language support / 多语言支持

## Creating Themes / 创建主题

### Basic Theme / 基础主题
1. Create theme directory / 创建主题目录
2. Create configuration file / 创建配置文件
3. Add required assets / 添加必需资源
4. Test theme / 测试主题

### Custom Colors / 自定义颜色
- Color definition / 颜色定义
```json
{
  "colors": {
    "primary": "#4A90E2",
    "secondary": "#50E3C2",
    "background": "#FFFFFF",
    "text": "#333333",
    "board": {
      "background": "#F5DEB3",
      "grid": "#000000",
      "black": "#000000",
      "white": "#FFFFFF"
    }
  }
}
```

### Custom Assets / 自定义资源
- Image assets / 图片资源
  - Board textures / 棋盘纹理
  - Piece designs / 棋子设计
  - UI elements / 界面元素

- Sound assets / 音效资源
  - Move sounds / 落子音效
  - Win sounds / 胜利音效
  - Background music / 背景音乐

### Testing Themes / 测试主题
- Visual testing / 视觉测试
- Performance testing / 性能测试
- Cross-platform testing / 跨平台测试
- Accessibility testing / 可访问性测试

## Theme API / 主题API

### Color Management / 颜色管理
```python
class ThemeManager:
    def get_color(name: str) -> Color
    def set_color(name: str, color: Color)
    def reset_colors()
```

### Asset Loading / 资源加载
```python
class AssetManager:
    def load_image(path: str) -> Image
    def load_sound(path: str) -> Sound
    def load_font(path: str, size: int) -> Font
```

### Dynamic Updates / 动态更新
- Hot reload support / 热重载支持
- Theme switching / 主题切换
- State persistence / 状态持久化

### Fallback Handling / 回退处理
- Missing assets / 缺失资源
- Invalid colors / 无效颜色
- Font substitution / 字体替换

## Best Practices / 最佳实践

### Design Guidelines / 设计指南
- Color contrast / 颜色对比
- Visual hierarchy / 视觉层次
- Consistency / 一致性
- Accessibility / 可访问性

### Performance Tips / 性能提示
- Asset optimization / 资源优化
- Caching strategy / 缓存策略
- Memory management / 内存管理
- Loading time / 加载时间

### Compatibility / 兼容性
- Platform support / 平台支持
- Resolution handling / 分辨率处理
- DPI scaling / DPI缩放
- Color spaces / 色彩空间 