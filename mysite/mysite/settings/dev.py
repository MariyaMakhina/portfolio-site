from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-w!v9eqvli8#55(ih#cvehbxu%e+2(@=*n=aj$@+v5_849uu=*_"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass


# ===== Telegram (уведомления о заявках) =====
TELEGRAM_BOT_TOKEN = '8731667975:AAGkN8i6sx4r5W2WhcR5qclydtrrhN8Au6dA'  
TELEGRAM_CHAT_ID = '1669583035'   

# ===== GIGA CHAT (бесплатный AI для бота) =====
GIGACHAT_CLIENT_ID = '019eb09d-47c5-7134-bd30-56ac6fc8c247'
GIGACHAT_CLIENT_SECRET = 'MDE5ZWIwOWQtNDdjNS03MTM0LWJkMzAtNTZhYzZmYzhjMjQ3OjczNmQzN2JiLWRhYTUtNDRmMC05N2QyLTdmMTc2YWFjYTY5Mw'
GIGACHAT_MODEL = 'GigaChat'