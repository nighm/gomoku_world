"""
Basic configuration usage example.
基本配置使用示例。
"""

from gomoku_world.config import game_config, i18n_config
from gomoku_world.config.validator import ConfigValidator
from gomoku_world.config.exceptions import ConfigError, ConfigValidationError

def main():
    """
    Main function.
    主函数。
    """
    try:
        # Basic operations / 基本操作
        print("Current game configuration:")
        print(game_config.to_dict())
        
        print("\nGetting specific values:")
        board_size = game_config.get("game.board_size")
        print(f"Board size: {board_size}")
        
        theme = game_config.get("display.theme")
        print(f"Theme: {theme}")
        
        # Setting values / 设置值
        print("\nSetting new values:")
        game_config.set("game.board_size", 13)
        game_config.set("display.theme", "dark")
        
        print("Updated configuration:")
        print(game_config.to_dict())
        
        # Validation example / 验证示例
        print("\nValidation example:")
        validator = ConfigValidator()
        
        # Add validation rules / 添加验证规则
        validator.add_type_rule("game.board_size", int)
        validator.add_range_rule("game.board_size", 9, 19)
        validator.add_enum_rule("display.theme", ["light", "dark"])
        
        # Try invalid values / 尝试无效值
        try:
            game_config.set("game.board_size", 21)  # Too large
            validator.validate(game_config.to_dict())
        except ConfigValidationError as e:
            print("Validation failed as expected:")
            print(e)
        
        # Reset configuration / 重置配置
        print("\nResetting configuration:")
        game_config.reset()
        print(game_config.to_dict())
        
    except ConfigError as e:
        print(f"Configuration error: {e}")

if __name__ == "__main__":
    main()

 