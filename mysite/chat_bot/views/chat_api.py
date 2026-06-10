# chat_bot/views/chat_api.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from chat_bot.utils.telegram import notify_chat
from chat_bot.utils.ai import ask_ai


WELCOME = {
    'text': (
        'Привет! Я Мария, веб-программист на Wagtail/Django.\n\n'
        'Делаю сайты и чат-ботов, которые помогают бизнесу '
        'получать больше клиентов без лишней рутины.\n'
        'Чем могу помочь?'
    ),
    'buttons': ['portfolio', 'price', 'chatbot', 'contacts'],
}

FALLBACK = {
    'portfolio': {
        'text': (
            'Вот что я делаю:\n\n'
            '• Сайты для бизнеса — лендинги, портфолио, сайты услуг'
            '• Портфолио-сайт для фотостудии — галерея работ, запись на съёмку\n'
            '• AI-боты на сайт — отвечают клиентам 24/7\n\n'
            'Что интересует подробнее?'
        ),
        'buttons': ['price', 'chatbot', 'contacts', 'back'],
    },
    'price': {
        'text': (
            'Цены зависят от задачи. Примерные ориентиры:\n\n'
            '• Лендинг — от 50 000 ₽\n'
            '• Корпоративный сайт — от 100 000 ₽\n'
            '• AI-бот на сайт — от 80 000 ₽\n'
            '• Telegram/WhatsApp бот — от 40 000 ₽\n\n'
            'Хотите точный расчёт под ваш проект?'
        ),
        'buttons': ['calc', 'phone', 'back'],
    },
    'chatbot': {
        'text': (
            'Я делаю чат-ботов для бизнеса:\n\n'
            'AI-консультант — отвечает клиентам 24/7\n'
            'Квалификатор лидов — собирает заявки\n'
            'Бот-запись — бронирование с уведомлениями\n\n'
            'Работаю с Telegram, WhatsApp, сайтом.'
        ),
        'buttons': ['ai', 'qualify', 'calendar', 'back'],
    },
    'contacts': {
        'text': (
            'На связи:\n\n'
            'Telegram: @ваш_логин\n'
            'Почта: mail@mariyamakhina.ru\n\n'
            'Или напишите вопрос прямо здесь — отвечу лично.'
        ),
        'buttons': ['question', 'back'],
    },
    'calc': {
        'text': (
            'Давайте уточним детали. Напишите:\n'
            '1. Что нужно сделать?\n'
            '2. Примерный бюджет?\n'
            '3. Сроки?\n\n'
            'Я подготовлю расчёт и отвечу в течение дня.'
        ),
        'buttons': ['back'],
    },
    'unknown': {
        'text': (
            'Я передала ваш вопрос — отвечу лично в течение часа.\n'
            'А пока можете посмотреть портфолио и цены:'
        ),
        'buttons': ['portfolio', 'price', 'contacts'],
    },
}

# Маппинг кодов кнопок → текст и иконки
BUTTON_MAP = {
    'portfolio':    {'text': 'Портфолио',    'icon': 'portfolio'},
    'price':        {'text': 'Стоимость',    'icon': 'price'},
    'chatbot':      {'text': 'Чат-боты',     'icon': 'chatbot'},
    'contacts':     {'text': 'Контакты',     'icon': 'contacts'},
    'back':         {'text': 'В начало',     'icon': 'back'},
    'calc':         {'text': 'Расчёт',       'icon': 'calc'},
    'phone':        {'text': 'Созвониться',  'icon': 'phone'},
    'ai':           {'text': 'AI-консультант','icon': 'ai'},
    'qualify':      {'text': 'Квалификатор', 'icon': 'qualify'},
    'calendar':     {'text': 'Бот-запись',   'icon': 'calendar'},
    'question':     {'text': 'Написать',     'icon': 'question'},
}


def find_fallback(user_message):
    """Ищет ответ по ключевым словам И по кодам кнопок"""
    msg = user_message.lower().strip()
    
    # Сначала проверяем точное совпадение с кодами кнопок
    button_responses = {
        'portfolio': 'portfolio',
        'price': 'price',
        'chatbot': 'chatbot',
        'contacts': 'contacts',
        'calc': 'calc',
        'back': 'back',
        'phone': 'calc',
        'ai': 'chatbot',
        'qualify': 'chatbot',
        'calendar': 'chatbot',
        'question': 'contacts',
    }
    
    # Если это код кнопки — сразу возвращаем нужный ответ
    if msg in button_responses:
        key = button_responses[msg]
        if key == 'back':
            return WELCOME
        return FALLBACK.get(key, FALLBACK['unknown'])
    
    # Дальше поиск по ключевым словам (как было)
    if any(w in msg for w in ['портфолио', 'проект', 'работы', 'примеры', 'кейс']):
        return FALLBACK['portfolio']
    elif any(w in msg for w in ['стоимост', 'цена', 'сколько', 'прайс', 'услуг']):
        return FALLBACK['price']
    elif any(w in msg for w in ['чат-бот', 'чат бот', 'ai', 'бот', 'консультант']):
        return FALLBACK['chatbot']
    elif any(w in msg for w in ['контакт', 'телефон', 'почт', 'связь', 'телеграм']):
        return FALLBACK['contacts']
    elif any(w in msg for w in ['расчёт', 'рассчитать', 'запросить']):
        return FALLBACK['calc']
    elif any(w in msg for w in ['назад', 'в начало']):
        return WELCOME
    else:
        return FALLBACK['unknown']


@csrf_exempt
@require_POST
def chat_api(request):
    data = json.loads(request.body)
    user_message = data.get('message', '').strip()
    session_id = data.get('session_id', 'unknown')
    page_url = data.get('page_url', '')

    if not user_message:
        return JsonResponse(WELCOME)

    ai_answer = ask_ai(user_message, timeout=5)

    if ai_answer:
        return JsonResponse({
            'text': ai_answer,
            'buttons': ['portfolio', 'price', 'contacts'],
        })

    notify_chat(session_id, user_message, page_url)
    fallback = find_fallback(user_message)
    return JsonResponse(fallback)