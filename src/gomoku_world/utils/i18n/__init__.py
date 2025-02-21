"""
Internationalization module
国际化模块
"""

from .translator import Translator
from .locale import LocaleManager
from .messages import MessageCatalog
from .instances import translator, locale_manager, message_catalog

__all__ = [
    # Classes
    'Translator',
    'LocaleManager',
    'MessageCatalog',
    # Global instances
    'translator',
    'locale_manager',
    'message_catalog'
]

# Create global instances
translator = Translator()
locale_manager = LocaleManager()
message_catalog = MessageCatalog() 