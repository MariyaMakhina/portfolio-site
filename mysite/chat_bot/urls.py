# chat_bot/urls.py
from django.urls import path
from chat_bot.views.chat_api import chat_api

app_name = 'chat_bot'

urlpatterns = [
    path('api/chat/', chat_api, name='chat_api'),
]