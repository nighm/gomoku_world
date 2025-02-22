"""
Translation validation module
翻译验证模块
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from ..utils.logger import get_logger

logger = get_logger(__name__)

class TranslationValidator:
    """
    Translation file validator
    翻译文件验证器
    """
    
    @staticmethod
    def validate_file(file_path: Path) -> Dict[str, Any]:
        """
        Validate a translation file
        验证翻译文件
        
        Args:
            file_path: Path to the translation file
            
        Returns:
            Dict with validation results
        """
        try:
            if not file_path.exists():
                return {
                    "valid": False,
                    "error": f"File not found: {file_path}"
                }
                
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            # Check if it's a dictionary
            if not isinstance(data, dict):
                return {
                    "valid": False,
                    "error": "File content must be a JSON object"
                }
                
            # Check all values are strings
            invalid_keys = []
            for key, value in data.items():
                if not isinstance(value, str):
                    invalid_keys.append(key)
                    
            if invalid_keys:
                return {
                    "valid": False,
                    "error": f"Non-string values found for keys: {invalid_keys}"
                }
                
            # Check for format string consistency
            format_errors = []
            for key, value in data.items():
                try:
                    # Try to format with dummy values
                    dummy_args = {
                        "version": "1.0.0",
                        "player": "Player",
                        "count": 0,
                        "rating": 1500,
                        "resource": "resource",
                        "input": "input",
                        "size": 15
                    }
                    value.format(**dummy_args)
                except Exception as e:
                    format_errors.append(f"{key}: {str(e)}")
                    
            if format_errors:
                return {
                    "valid": False,
                    "error": f"Format string errors: {format_errors}"
                }
                
            return {
                "valid": True,
                "key_count": len(data)
            }
            
        except json.JSONDecodeError as e:
            return {
                "valid": False,
                "error": f"Invalid JSON format: {str(e)}"
            }
        except Exception as e:
            return {
                "valid": False,
                "error": f"Validation error: {str(e)}"
            }
            
    @staticmethod
    def validate_directory(dir_path: Path) -> Dict[str, Any]:
        """
        Validate all translation files in a directory
        验证目录中的所有翻译文件
        
        Args:
            dir_path: Path to the directory containing translation files
            
        Returns:
            Dict with validation results for each file
        """
        results = {}
        
        if not dir_path.exists() or not dir_path.is_dir():
            return {
                "valid": False,
                "error": f"Invalid directory: {dir_path}"
            }
            
        for file_path in dir_path.glob("*.json"):
            results[file_path.name] = TranslationValidator.validate_file(file_path)
            
        return results
        
    @staticmethod
    def compare_translations(base_file: Path, target_file: Path) -> Dict[str, Any]:
        """
        Compare two translation files for consistency
        比较两个翻译文件的一致性
        
        Args:
            base_file: Path to the base translation file
            target_file: Path to the target translation file
            
        Returns:
            Dict with comparison results
        """
        try:
            # Load base file
            with open(base_file, "r", encoding="utf-8") as f:
                base_data = json.load(f)
                
            # Load target file
            with open(target_file, "r", encoding="utf-8") as f:
                target_data = json.load(f)
                
            # Compare keys
            base_keys = set(base_data.keys())
            target_keys = set(target_data.keys())
            
            missing_keys = base_keys - target_keys
            extra_keys = target_keys - base_keys
            
            return {
                "valid": len(missing_keys) == 0,
                "missing_keys": list(missing_keys),
                "extra_keys": list(extra_keys),
                "base_count": len(base_keys),
                "target_count": len(target_keys)
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": f"Comparison error: {str(e)}"
            }
            
    @staticmethod
    def check_format_consistency(files: List[Path]) -> Dict[str, Any]:
        """
        Check format string consistency across multiple translation files
        检查多个翻译文件之间的格式字符串一致性
        
        Args:
            files: List of translation file paths
            
        Returns:
            Dict with consistency check results
        """
        try:
            format_specs = {}
            inconsistencies = []
            
            for file_path in files:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                for key, value in data.items():
                    # Extract format specifiers
                    import re
                    specs = set(re.findall(r'{(\w+)}', value))
                    
                    if key in format_specs:
                        if specs != format_specs[key]:
                            inconsistencies.append({
                                "key": key,
                                "file": file_path.name,
                                "expected": format_specs[key],
                                "found": specs
                            })
                    else:
                        format_specs[key] = specs
                        
            return {
                "valid": len(inconsistencies) == 0,
                "inconsistencies": inconsistencies
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": f"Format consistency check error: {str(e)}"
            } 