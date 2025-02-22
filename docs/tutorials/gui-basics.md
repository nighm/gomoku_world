# GUI 基础教程 / GUI Basics Tutorial

## 概述 / Overview

本教程将介绍如何使用 PyQt6 构建五子棋游戏的图形用户界面。我们将学习如何创建游戏窗口、绘制棋盘、处理用户输入等内容。

## GUI 框架选择 / GUI Framework Selection

我们选择 PyQt6 作为 GUI 框架的原因：
- 跨平台支持
- 丰富的组件库
- 优秀的性能
- 完善的文档
- 活跃的社区

## 基础窗口创建 / Basic Window Creation

### 1. 主窗口类 / Main Window Class

```python
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import Qt

class GomokuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gomoku World")
        self.setMinimumSize(800, 600)
        self.init_ui()
```

### 2. 界面初始化 / UI Initialization

```python
def init_ui(self):
    # 创建中心部件
    self.central_widget = QWidget()
    self.setCentralWidget(self.central_widget)
    
    # 创建布局
    self.layout = QVBoxLayout()
    self.central_widget.setLayout(self.layout)
    
    # 添加菜单栏
    self.create_menu_bar()
    
    # 添加工具栏
    self.create_tool_bar()
    
    # 创建状态栏
    self.statusBar().showMessage("Ready")
```

## 棋盘绘制 / Board Drawing

### 1. 棋盘部件 / Board Widget

```python
from PyQt6.QtGui import QPainter, QPen, QBrush
from PyQt6.QtCore import QRect

class BoardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.board_size = 15
        self.cell_size = 40
        self.padding = 20
        
    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_grid(painter)
        self.draw_pieces(painter)
```

### 2. 网格绘制 / Grid Drawing

```python
def draw_grid(self, painter: QPainter):
    """绘制棋盘网格"""
    # 设置画笔
    pen = QPen(Qt.black, 1, Qt.SolidLine)
    painter.setPen(pen)
    
    # 绘制横线
    for i in range(self.board_size):
        y = self.padding + i * self.cell_size
        painter.drawLine(
            self.padding, y,
            self.padding + (self.board_size - 1) * self.cell_size, y
        )
    
    # 绘制竖线
    for i in range(self.board_size):
        x = self.padding + i * self.cell_size
        painter.drawLine(
            x, self.padding,
            x, self.padding + (self.board_size - 1) * self.cell_size
        )
```

### 3. 棋子绘制 / Piece Drawing

```python
def draw_pieces(self, painter: QPainter):
    """绘制棋子"""
    for y in range(self.board_size):
        for x in range(self.board_size):
            piece = self.board.get_piece(x, y)
            if piece:
                self.draw_piece(painter, x, y, piece)

def draw_piece(self, painter: QPainter, x: int, y: int, piece: Player):
    """绘制单个棋子"""
    center_x = self.padding + x * self.cell_size
    center_y = self.padding + y * self.cell_size
    radius = self.cell_size // 2 - 2
    
    color = Qt.black if piece == Player.BLACK else Qt.white
    painter.setBrush(QBrush(color))
    painter.drawEllipse(
        center_x - radius,
        center_y - radius,
        radius * 2,
        radius * 2
    )
```

## 事件处理 / Event Handling

### 1. 鼠标事件 / Mouse Events

```python
def mousePressEvent(self, event):
    """处理鼠标点击事件"""
    if event.button() == Qt.LeftButton:
        # 获取点击位置对应的棋盘坐标
        x = round((event.x() - self.padding) / self.cell_size)
        y = round((event.y() - self.padding) / self.cell_size)
        
        # 检查坐标是否有效
        if 0 <= x < self.board_size and 0 <= y < self.board_size:
            # 尝试落子
            if self.game.make_move(Position(x, y)):
                self.update()  # 重绘棋盘
```

### 2. 键盘事件 / Keyboard Events

```python
def keyPressEvent(self, event):
    """处理键盘事件"""
    if event.key() == Qt.Key_Escape:
        self.close()  # 退出游戏
    elif event.key() == Qt.Key_U:
        self.game.undo()  # 悔棋
        self.update()
```

## 菜单和工具栏 / Menus and Toolbars

### 1. 菜单创建 / Menu Creation

```python
def create_menu_bar(self):
    """创建菜单栏"""
    menubar = self.menuBar()
    
    # 文件菜单
    file_menu = menubar.addMenu("File")
    file_menu.addAction("New Game", self.new_game)
    file_menu.addAction("Save Game", self.save_game)
    file_menu.addAction("Load Game", self.load_game)
    file_menu.addSeparator()
    file_menu.addAction("Exit", self.close)
    
    # 设置菜单
    settings_menu = menubar.addMenu("Settings")
    settings_menu.addAction("Game Rules", self.show_rules)
    settings_menu.addAction("AI Level", self.set_ai_level)
```

### 2. 工具栏创建 / Toolbar Creation

```python
def create_tool_bar(self):
    """创建工具栏"""
    toolbar = self.addToolBar("Game Tools")
    toolbar.addAction("Undo", self.game.undo)
    toolbar.addAction("Hint", self.show_hint)
    toolbar.addAction("Restart", self.new_game)
```

## 对话框和消息 / Dialogs and Messages

### 1. 游戏结束对话框 / Game Over Dialog

```python
def show_game_over_dialog(self, winner: Player):
    """显示游戏结束对话框"""
    msg = QMessageBox()
    msg.setWindowTitle("Game Over")
    msg.setText(f"Player {winner.name} wins!")
    msg.setStandardButtons(
        QMessageBox.Ok | QMessageBox.Retry
    )
    
    if msg.exec() == QMessageBox.Retry:
        self.new_game()
```

### 2. 状态栏更新 / Status Bar Update

```python
def update_status(self):
    """更新状态栏信息"""
    player = "Black" if self.game.current_player == Player.BLACK else "White"
    self.statusBar().showMessage(f"Current Player: {player}")
```

## 样式和主题 / Styles and Themes

### 1. 应用样式表 / Apply Stylesheet

```python
def apply_style(self):
    """应用自定义样式"""
    self.setStyleSheet("""
        QMainWindow {
            background-color: #f0f0f0;
        }
        
        QMenuBar {
            background-color: #e0e0e0;
        }
        
        QStatusBar {
            background-color: #e0e0e0;
        }
    """)
```

### 2. 主题切换 / Theme Switching

```python
def switch_theme(self, theme: str):
    """切换主题"""
    if theme == "dark":
        self.apply_dark_theme()
    else:
        self.apply_light_theme()
```

## 练习项目 / Practice Projects

1. 实现基本的棋盘绘制
2. 添加鼠标落子功能
3. 创建游戏菜单
4. 实现悔棋功能
5. 添加主题切换

## 进阶主题 / Advanced Topics

1. 动画效果
2. 自定义控件
3. 响应式布局
4. 多语言支持
5. 性能优化

## 调试技巧 / Debugging Tips

1. 使用 Qt Designer
2. 打印调试信息
3. 使用 Qt Debug Bridge
4. 性能分析工具

## 参考资料 / References

1. [PyQt6 官方文档](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
2. [Qt 设计指南](https://doc.qt.io/qt-6/design.html)
3. [GUI 编程最佳实践](../best-practices/gui.md)
4. [示例代码库](../examples/gui/) 