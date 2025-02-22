"""
Internationalization package
国际化包
"""

from .manager import I18nManager

# Create global i18n manager instance
i18n_manager = I18nManager()

__all__ = ['i18n_manager', 'I18nManager'] 