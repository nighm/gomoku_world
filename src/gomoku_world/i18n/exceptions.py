"""
Internationalization exceptions.

国际化异常。

This module defines all exceptions that can be raised by the i18n system.
本模块定义了i18n系统可能抛出的所有异常。
"""

class I18nError(Exception):
    """
    Base exception for all i18n related errors.
    所有i18n相关错误的基类。
    """
    pass

class TranslationNotFoundError(I18nError):
    """
    Raised when a translation key is not found.
    当找不到翻译键时抛出。
    """
    def __init__(self, key: str, language: str):
        self.key = key
        self.language = language
        super().__init__(f"Translation not found for key '{key}' in language '{language}' / "
                        f"在语言'{language}'中未找到键'{key}'的翻译")

class LanguageNotSupportedError(I18nError):
    """
    Raised when trying to use an unsupported language.
    当尝试使用不支持的语言时抛出。
    """
    def __init__(self, language: str, supported_languages: list):
        self.language = language
        self.supported_languages = supported_languages
        super().__init__(f"Language '{language}' is not supported. Supported languages: {supported_languages} / "
                        f"不支持语言'{language}'。支持的语言：{supported_languages}")

class TranslationFileError(I18nError):
    """
    Raised when there is an error with translation files.
    当翻译文件出现错误时抛出。
    """
    def __init__(self, file_path: str, error: str):
        self.file_path = file_path
        self.error = error
        super().__init__(f"Error in translation file '{file_path}': {error} / "
                        f"翻译文件'{file_path}'出错：{error}")

class FormatterError(I18nError):
    """
    Raised when there is an error formatting a translation string.
    当格式化翻译字符串时出错时抛出。
    """
    def __init__(self, template: str, args: dict, error: str):
        self.template = template
        self.args = args
        self.error = error
        super().__init__(f"Error formatting string '{template}' with args {args}: {error} / "
                        f"使用参数{args}格式化字符串'{template}'时出错：{error}")

class ValidationError(I18nError):
    """
    Raised when translation validation fails.
    当翻译验证失败时抛出。
    """
    def __init__(self, message: str, details: dict = None):
        self.details = details or {}
        super().__init__(f"{message} Details: {details} / "
                        f"{message} 详细信息：{details}")

class CacheError(I18nError):
    """
    Raised when there is an error with the translation cache.
    当翻译缓存出错时抛出。
    """
    def __init__(self, operation: str, error: str):
        self.operation = operation
        self.error = error
        super().__init__(f"Cache {operation} failed: {error} / "
                        f"缓存{operation}失败：{error}") 