import requests
from django.conf import settings
from django.utils import timezone


def _send_to_telegram(text, chat_id=None):
    """Внутренняя функция отправки сообщения"""
    bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    target_chat = chat_id or getattr(settings, 'TELEGRAM_CHAT_ID', '')

    if not bot_token or not target_chat:
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    try:
        response = requests.post(url, json={
            'chat_id': target_chat,
            'text': text,
            'parse_mode': 'HTML',
        }, timeout=10)
        return response.json().get('ok', False)
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")
        return False


def notify_lead(name, contact, message, page_url=''):
    """Уведомление о заявке с формы"""
    text = (
        f"📨 <b>Новая заявка с сайта!</b>\n\n"
        f"<b>Имя:</b> {name}\n"
        f"<b>Контакты:</b> {contact}\n"
        f"<b>Сообщение:</b> {message}\n"
        f"<b>Страница:</b> {page_url}\n"
        f"<b>Время:</b> {timezone.now().strftime('%d.%m.%Y %H:%M')}"
    )
    return _send_to_telegram(text)


def notify_chat(session_id, user_message, page_url=''):
    """Уведомление о сообщении из чат-виджета"""
    text = (
        f"💬 <b>Новое сообщение в чате сайта</b>\n\n"
        f"<b>Сообщение:</b> {user_message}\n"
        f"<b>Сессия:</b> {session_id}\n"
        f"<b>Страница:</b> {page_url}\n"
        f"<b>Время:</b> {timezone.now().strftime('%d.%m.%Y %H:%M')}"
    )
    return _send_to_telegram(text)