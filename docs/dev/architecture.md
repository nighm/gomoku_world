# Gomoku Architecture

## Overview

The Gomoku game is built with a modular architecture that separates core game logic from platform-specific implementations.

```
src/gomoku/
├── core/           # Core game logic
├── gui/            # GUI implementation
├── network/        # Network play support
├── utils/          # Utility functions
├── platforms/      # Platform-specific code
└── resources/      # Game resources
```

## Core Components

### Game Logic

The core game logic is implemented in the `core` module:
- `Board`: Manages game state
- `Rules`: Implements game rules
- `AI`: Provides computer player implementation

Key features:
- Pure Python implementation
- Platform-independent
- Testable in isolation
- No GUI dependencies

### GUI System

The GUI system is built with Pygame:
- Modular design
- Theme support
- Resolution independence
- Platform-specific optimizations

### Platform Support

Platform-specific code is isolated in the `platforms` module:
- Windows implementation
- Linux implementation
- Android implementation
- Common base classes

## Data Flow

1. User Input
   ```
   GUI Event -> Event Handler -> Game State Update -> Display Update
   ```

2. AI Move
   ```
   Game State -> AI Evaluation -> Move Selection -> Game State Update -> Display Update
   ```

3. Network Play
   ```
   Local Move -> Network Protocol -> Remote Player -> Network Protocol -> Local Update
   ```

## Key Design Patterns

1. Model-View-Controller (MVC)
   - Model: Board and game state
   - View: GUI components
   - Controller: Event handlers

2. Factory Pattern
   - Theme creation
   - Platform-specific implementations

3. Strategy Pattern
   - AI algorithms
   - Network protocols

4. Observer Pattern
   - Game state updates
   - Network synchronization

## Resource Management

Resources are managed through the `resources` module:
- Fonts
- Images
- Sound effects
- Configuration files

Features:
- Lazy loading
- Platform-specific paths
- PyInstaller support

## Configuration System

Configuration is managed through JSON files:
- Theme definitions
- Game settings
- AI parameters

## Internationalization

Text handling:
- Unicode support
- Multiple language files
- Dynamic language switching

## Testing Strategy

1. Unit Tests
   - Core game logic
   - AI algorithms
   - Utility functions

2. Integration Tests
   - Game flow
   - GUI interaction
   - Network play

3. Performance Tests
   - AI speed
   - GUI responsiveness
   - Network latency

## Build System

The build system supports:
- Windows executable
- Linux binary
- Android APK
- Development builds

## Future Considerations

1. Planned Improvements
   - WebAssembly support
   - Cloud save support
   - Tournament mode

2. Scalability
   - Microservices for online play
   - Database integration
   - Analytics support 