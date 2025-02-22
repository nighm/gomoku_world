# Core API Reference / 核心API参考

## Architecture Overview / 架构概述

```mermaid
classDiagram
    class Game {
        +Board board
        +int current_player
        +List~Position~ move_history
        +make_move(row, col)
        +check_winner(row, col)
        +reset()
    }
    
    class Board {
        +np.ndarray board
        +int size
        +place_piece(row, col, player)
        +clear_cell(row, col)
        +is_valid_move(row, col)
    }
    
    class Position {
        +int row
        +int col
    }
    
    class AI {
        +Strategy strategy
        +get_move(board, player)
        +evaluate_position(board)
    }
    
    Game --> Board
    Game --> Position
    AI --> Board
```

## Game Module / 游戏模块

### Board Class / 棋盘类

```mermaid
classDiagram
    class Board {
        +np.ndarray board
        +int size
        +place_piece(row, col, player)
        +clear_cell(row, col)
        +is_valid_move(row, col)
        +get_piece(row, col)
        +is_full()
        +get_empty_cells()
        +__str__()
    }
```

### Game Class / 游戏类

```mermaid
classDiagram
    class Game {
        +Board board
        +int current_player
        +List~Position~ move_history
        +Optional~int~ winner
        +bool _game_over
        +make_move(row, col)
        +check_winner(row, col)
        +reset()
        +get_valid_moves()
        +is_board_full()
        +is_game_over()
        +get_winner()
    }
```

### Position Class / 位置类

```mermaid
classDiagram
    class Position {
        +int row
        +int col
    }
```

## AI Module / AI模块

### AI Engine / AI引擎

```mermaid
classDiagram
    class AI {
        +Strategy strategy
        +get_move(board, player)
        +evaluate_position(board)
    }
    
    class Strategy {
        <<interface>>
        +get_move(board, player)*
    }
    
    class MinMaxStrategy {
        +evaluator: PositionEvaluator
        +get_move(board, player)
        -_min_value(board, depth, alpha, beta)
        -_max_value(board, depth, alpha, beta)
    }
    
    class MCTSStrategy {
        +simulation_limit: int
        +get_move(board, player)
        -_select(node)
        -_expand(node)
        -_simulate(node)
        -_backpropagate(node, result)
    }
    
    AI --> Strategy
    Strategy <|.. MinMaxStrategy
    Strategy <|.. MCTSStrategy
```

### Strategies / 策略

```mermaid
classDiagram
    class Strategy {
        <<interface>>
        +get_move(board, player)*
    }
    
    class MinMaxStrategy {
        +evaluator: PositionEvaluator
        +get_move(board, player)
        -_min_value(board, depth, alpha, beta)
        -_max_value(board, depth, alpha, beta)
    }
    
    class MCTSStrategy {
        +simulation_limit: int
        +get_move(board, player)
        -_select(node)
        -_expand(node)
        -_simulate(node)
        -_backpropagate(node, result)
    }
    
    Strategy <|.. MinMaxStrategy
    Strategy <|.. MCTSStrategy
```

### Evaluation / 评估

```mermaid
classDiagram
    class PositionEvaluator {
        +Dict pattern_scores
        +evaluate(board, player)
        -_evaluate_line(line, player)
        -_get_pattern_score(count)
    }
```

## Platform Module / 平台模块

### Platform Base / 平台基类

```mermaid
classDiagram
    class PlatformBase {
        +str name
        +Path config_dir
        +get_font_path(font_name)
        +get_resource_path(resource_name)
        +get_config_path()
        +get_log_path()
        +setup()
        +cleanup()
    }
    
    class WindowsPlatform {
        +Path fonts_dir
    }
    
    class LinuxPlatform {
        +Path fonts_dir
    }
    
    class MacOSPlatform {
        +Path fonts_dir
    }
    
    class WebPlatform {
    }
    
    PlatformBase <|-- WindowsPlatform
    PlatformBase <|-- LinuxPlatform
    PlatformBase <|-- MacOSPlatform
    PlatformBase <|-- WebPlatform
```

## Resource Module / 资源模块

### Resource Manager / 资源管理器

```mermaid
classDiagram
    class ResourceManager {
        +Dict _resources
        +Dict _theme
        +Dict _texts
        +get_theme()
        +get_text(key)
        +load_resources(resource_dir)
    }
```

### Theme Manager / 主题管理器

```mermaid
classDiagram
    class Theme {
        +Dict _theme
        +get_color(key)
        +set_theme(theme_name)
    }
```

### I18n Manager / 国际化管理器

```mermaid
classDiagram
    class I18n {
        +str _language
        +Dict _texts
        +get_text(key)
        +get_bilingual(key)
        +set_language(language)
    }
``` 