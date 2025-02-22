import sys
import json
from pathlib import Path
from gomoku_world.utils.logger import get_logger

logger = get_logger(__name__)

def verify_integration():
    issues = []
    
    # 1. 检查必要的文件
    required_files = [
        "src/gomoku_world/i18n/manager.py",
        "src/gomoku_world/utils/network.py",
        "resources/i18n/en/common.json",
        "resources/i18n/zh/common.json"
    ]
    
    for file in required_files:
        if not Path(file).exists():
            issues.append(f"Missing file: {file}")
    
    # 2. 检查版本号一致性
    version_files = [
        "setup.cfg",
        "pyproject.toml",
        "src/gomoku_world/__init__.py"
    ]
    
    versions = {}
    for file in version_files:
        # 读取版本号
        try:
            with open(file, encoding='utf-8') as f:
                content = f.read()
                if "version = " in content:
                    version = content.split("version = ")[1].split("\n")[0].strip('"\'')
                    versions[file] = version
        except Exception as e:
            issues.append(f"Failed to read version from {file}: {e}")
    
    if len(set(versions.values())) > 1:
        issues.append(f"Inconsistent versions: {versions}")
    
    # 3. 检查国际化键的一致性
    en_keys = set()
    zh_keys = set()
    
    for lang in ["en", "zh"]:
        for category in ["common", "game"]:
            file = f"resources/i18n/{lang}/{category}.json"
            if Path(file).exists():
                try:
                    with open(file, encoding='utf-8') as f:
                        data = json.load(f)
                        keys = set(data.keys())
                        if lang == "en":
                            en_keys.update(keys)
                        else:
                            zh_keys.update(keys)
                except Exception as e:
                    issues.append(f"Failed to read translations from {file}: {e}")
    
    missing_zh = en_keys - zh_keys
    if missing_zh:
        issues.append(f"Missing Chinese translations for: {missing_zh}")
    
    # 4. 检查GUI组件的国际化支持
    gui_files = [
        "src/gomoku_world/gui/main_window.py",
        "src/gomoku_world/gui/menu_bar.py"
    ]
    
    for file in gui_files:
        if Path(file).exists():
            try:
                with open(file, encoding='utf-8') as f:
                    content = f.read()
                    if "i18n_manager.get_text" not in content:
                        issues.append(f"Missing i18n support in: {file}")
            except Exception as e:
                issues.append(f"Failed to read {file}: {e}")
    
    # 输出结果
    if issues:
        logger.error("Found integration issues:")
        for issue in issues:
            logger.error(f"- {issue}")
        return False
    
    logger.info("All integration checks passed!")
    return True

if __name__ == "__main__":
    sys.exit(0 if verify_integration() else 1) 