from .base import *

DEBUG = False

# ManifestStaticFilesStorage is recommended in production, to prevent
# outdated JavaScript / CSS assets being served from cache
# (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/6.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

try:
    from .local import *
except ImportError:
    pass


# ===== Telegram =====
TELEGRAM_BOT_TOKEN = '796xxxxxx:AAH...'  # реальный токен
TELEGRAM_CHAT_ID = '123456789'           # ваш chat_id

# ===== Groq AI =====
GROQ_API_KEY = 'gsk_...'  # реальный ключ