# Interactive Tutorial / 交互式教程

## Game Basics / 游戏基础

### Starting a Game / 开始游戏

<div class="tutorial-animation">
    <video width="600" height="400" controls>
        <source src="../images/tutorials/animations/start-game.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</div>

1. Click "New Game" button / 点击"新游戏"按钮
2. Select game mode / 选择游戏模式
3. Configure settings / 配置设置
4. Start playing / 开始游戏

### Making Moves / 落子操作

<div class="tutorial-animation">
    <video width="600" height="400" controls>
        <source src="../images/tutorials/animations/making-moves.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</div>

```mermaid
sequenceDiagram
    participant Player
    participant Board
    participant Game
    Player->>Board: Click Position
    Board->>Game: Check Valid Move
    Game->>Board: Update Board
    Board->>Player: Show New State
```

### Understanding Win Conditions / 理解胜利条件

<div class="tutorial-animation">
    <video width="600" height="400" controls>
        <source src="../images/tutorials/animations/win-conditions.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</div>

Win patterns:
```mermaid
graph TD
    A[Win Conditions] --> B[Horizontal]
    A --> C[Vertical]
    A --> D[Diagonal]
    A --> E[Anti-diagonal]
    B --> F[Five in a row]
    C --> F
    D --> F
    E --> F
```

## Playing Against AI / 对战AI

### AI Difficulty Selection / AI难度选择

<div class="tutorial-animation">
    <video width="600" height="400" controls>
        <source src="../images/tutorials/animations/ai-selection.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</div>

```mermaid
graph LR
    A[Select AI] --> B[Easy]
    A --> C[Medium]
    A --> D[Hard]
    B --> E[Random Moves]
    C --> F[Strategic Moves]
    D --> G[Advanced Strategy]
```

### Understanding AI Behavior / 理解AI行为

<div class="tutorial-animation">
    <video width="600" height="400" controls>
        <source src="../images/tutorials/animations/ai-behavior.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</div>

AI decision process:
```mermaid
flowchart TD
    A[AI Turn] --> B[Analyze Board]
    B --> C[Evaluate Positions]
    C --> D[Choose Best Move]
    D --> E[Make Move]
    E --> F[Update Board]
```

## Online Multiplayer / 在线多人游戏

### Joining a Game / 加入游戏

<div class="tutorial-animation">
    <video width="600" height="400" controls>
        <source src="../images/tutorials/animations/join-game.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</div>

```mermaid
sequenceDiagram
    participant Player
    participant Server
    participant Opponent
    Player->>Server: Request Game
    Server->>Opponent: Match Request
    Opponent->>Server: Accept
    Server->>Player: Game Start
    Server->>Opponent: Game Start
```

### Playing Online / 在线对战

<div class="tutorial-animation">
    <video width="600" height="400" controls>
        <source src="../images/tutorials/animations/online-play.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</div>

Network game flow:
```mermaid
graph TD
    A[Make Move] --> B[Send to Server]
    B --> C[Validate Move]
    C --> D[Broadcast Move]
    D --> E[Update All Clients]
    E --> F[Next Turn]
```

## Customization / 自定义设置

### Theme Customization / 主题自定义

<div class="tutorial-animation">
    <video width="600" height="400" controls>
        <source src="../images/tutorials/animations/theme-customization.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</div>

Theme components:
```mermaid
mindmap
    root((Theme))
        Colors
            Board
            Pieces
            Background
            UI
        Fonts
            Main
            Menu
            Game
        Sounds
            Move
            Win
            Background
```

### Language Settings / 语言设置

<div class="tutorial-animation">
    <video width="600" height="400" controls>
        <source src="../images/tutorials/animations/language-settings.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</div>

Language selection flow:
```mermaid
flowchart LR
    A[Select Language] --> B[Load Resources]
    B --> C[Update UI]
    C --> D[Save Preference]
```

## Advanced Features / 高级功能

### Game Analysis / 游戏分析

<div class="tutorial-animation">
    <video width="600" height="400" controls>
        <source src="../images/tutorials/animations/game-analysis.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</div>

Analysis features:
```mermaid
mindmap
    root((Analysis))
        Move History
            Replay
            Statistics
            Evaluation
        Position Analysis
            Threats
            Opportunities
            Score
        AI Suggestions
            Best Moves
            Variations
            Win Rate
```

### Tournament Mode / 比赛模式

<div class="tutorial-animation">
    <video width="600" height="400" controls>
        <source src="../images/tutorials/animations/tournament-mode.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</div>

Tournament structure:
```mermaid
graph TD
    A[Tournament] --> B[Round 1]
    A --> C[Round 2]
    A --> D[Finals]
    B --> E[Matches]
    C --> E
    D --> E
    E --> F[Results]
    F --> G[Rankings]
```

## Style Guide / 样式指南

### CSS Styles / CSS样式

```css
.tutorial-animation {
    margin: 20px 0;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    background: #f5f5f5;
}

.tutorial-animation video {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 0 auto;
}
```

### Animation Guidelines / 动画指南

- Frame rate: 30fps
- Resolution: 1280x720
- Format: MP4 (H.264)
- Duration: 15-30 seconds
- File size: < 5MB 