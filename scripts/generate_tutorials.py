"""
Generate tutorial animations
生成教程动画
"""

import os
from pathlib import Path
from gomoku_world.utils.animation.generator import AnimationGenerator

def main():
    # Create animation generator
    generator = AnimationGenerator()
    
    # Get output directory
    output_dir = Path("docs/images/tutorials/animations")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate animations
    print("Generating AI game animation...")
    generator.generate_ai_game(str(output_dir / "ai-game.mp4"))
    
    print("Generating theme switch animation...")
    generator.generate_theme_switch(str(output_dir / "theme-switch.mp4"))
    
    print("Done!")

if __name__ == "__main__":
    main() 