#!/usr/bin/env python
"""
Translation validation script
翻译验证脚本
"""

import sys
import json
from pathlib import Path
from gomoku_world.i18n import i18n_manager
from gomoku_world.utils.logger import get_logger

logger = get_logger(__name__)

def validate_translations():
    """Validate all translations"""
    try:
        # Run validation
        results = i18n_manager.validate_translations()
        
        # Process results
        issues = []
        
        # Check individual language validation results
        for lang, lang_results in results.items():
            if lang == "format_consistency":
                continue
                
            if lang.startswith("compare_"):
                # Process comparison results
                target_lang = lang.split("_")[1]
                for file_name, compare_result in lang_results.items():
                    if not compare_result.get("valid", False):
                        missing = compare_result.get("missing_keys", [])
                        extra = compare_result.get("extra_keys", [])
                        if missing:
                            issues.append(f"Missing keys in {target_lang}/{file_name}: {missing}")
                        if extra:
                            issues.append(f"Extra keys in {target_lang}/{file_name}: {extra}")
            else:
                # Process language directory validation results
                for file_name, file_result in lang_results.items():
                    if not file_result.get("valid", False):
                        error = file_result.get("error", "Unknown error")
                        issues.append(f"Validation failed for {lang}/{file_name}: {error}")
                        
        # Check format consistency
        format_check = results.get("format_consistency", {})
        if not format_check.get("valid", False):
            inconsistencies = format_check.get("inconsistencies", [])
            for issue in inconsistencies:
                issues.append(
                    f"Format inconsistency in {issue['file']} for key '{issue['key']}': "
                    f"expected {issue['expected']}, found {issue['found']}"
                )
                
        # Output results
        if issues:
            logger.error("Translation validation failed:")
            for issue in issues:
                logger.error(f"- {issue}")
            return False
            
        logger.info("All translations validated successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return False

def main():
    """Main entry point"""
    try:
        success = validate_translations()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Script error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 