# chat_bot/utils/ai.py
from gigachat import GigaChat
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Ты — помощник Марии, веб-программиста на Wagtail/Django.

Что важно знать о Марии:
- Разрабатывает сайты и чат-ботов для бизнеса: лендинги, корпоративные сайты, портфолио, AI-боты
- Цены: лендинг от 50 000 ₽, AI-бот от 80 000 ₽, Telegram бот от 40 000 ₽
- Стек: Python, Django, Wagtail, PostgreSQL, Nginx, Gunicorn
- Контакты: Telegram и почта указаны на сайте

Как отвечать:
- Коротко и по делу, без воды
- Если вопрос сложный или нужен точный расчёт — предложи оставить заявку, Мария свяжется
- Не придумывай лишнего, не обещай того чего нет
- Не упоминай что Мария новичок"""


def ask_ai(user_message, timeout=10):
    """
    Запрос к GigaChat API.
    Возвращает текст ответа или None при ошибке.
    """
    client_id = getattr(settings, 'GIGACHAT_CLIENT_ID', '')
    client_secret = getattr(settings, 'GIGACHAT_CLIENT_SECRET', '')
    model = getattr(settings, 'GIGACHAT_MODEL', 'GigaChat')

    if not client_id or not client_secret:
        logger.warning("GigaChat не настроен")
        return None

    try:
        client = GigaChat(
            credentials=(client_id, client_secret),
            model=model,
            timeout=timeout,
            verify_ssl_certs=False,
        )

        response = client.chat([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ])

        answer = response.choices[0].message.content.strip()
        return answer

    except Exception as e:
        logger.error(f"GigaChat error: {e}")
        return None