#!/usr/bin/env python
"""
Генератор осмысленного, но безопасного URL для админки Wagtail.
Запуск: python generate_admin_url.py
"""

import secrets
import random

# Словари для генерации
adjectives = [
    'brave', 'calm', 'eager', 'fancy', 'grand', 'jolly', 'kind', 'lucky',
    'mighty', 'noble', 'proud', 'quiet', 'rapid', 'smart', 'swift', 'vivid',
    'witty', 'zealous', 'amber', 'cosmic', 'daring', 'elite', 'fierce',
    'glowing', 'hidden', 'iron', 'jazzy', 'keen', 'legacy', 'magic',
    'neon', 'optic', 'prime', 'quantum', 'radiant', 'silver', 'titan',
    'ultra', 'velvet', 'wizard', 'zenith'
]

nouns = [
    'astra', 'bridge', 'cloud', 'dawn', 'echo', 'falcon', 'glade', 'harbor',
    'island', 'jade', 'kaizen', 'lumen', 'meadow', 'nexus', 'oasis', 'peak',
    'quasar', 'ridge', 'star', 'tower', 'umbra', 'valley', 'wave', 'xenon',
    'yard', 'zen', 'alpha', 'beta', 'gamma', 'delta', 'omega', 'sigma',
    'pulse', 'flare', 'cipher', 'legend', 'phantom', 'rogue', 'spark',
    'thorn', 'unity', 'vector', 'whisper', 'zero'
]

def generate_admin_url(style='word-word-number', length=3):
    """
    Генерирует осмысленный, но безопасный URL для админки
    
    Стили:
    - 'word-word-number': слово-слово-число (по умолчанию)
    - 'word-number': слово-число
    - 'word-number-word': слово-число-слово
    - 'adjective-noun-number': прилагательное-существительное-число
    """
    
    # Случайное число (100-999)
    number = random.randint(100, 999)
    
    if style == 'word-word-number':
        word1 = secrets.choice(adjectives + nouns)
        word2 = secrets.choice(nouns)
        return f"{word1}-{word2}-{number}"
    
    elif style == 'word-number':
        word = secrets.choice(adjectives + nouns)
        return f"{word}-{number}"
    
    elif style == 'word-number-word':
        word1 = secrets.choice(adjectives + nouns)
        word2 = secrets.choice(nouns)
        return f"{word1}-{number}-{word2}"
    
    elif style == 'adjective-noun-number':
        adj = secrets.choice(adjectives)
        noun = secrets.choice(nouns)
        return f"{adj}-{noun}-{number}"
    
    else:
        # По умолчанию
        return f"{secrets.choice(adjectives)}-{secrets.choice(nouns)}-{number}"

def main():
    print("\n" + "="*50)
    print("🔐 Генератор безопасного URL для админки Wagtail")
    print("="*50)
    
    # Генерируем несколько вариантов
    print("\n📋 Варианты (выберите один):\n")
    
    variants = [
        ('word-word-number', generate_admin_url('word-word-number')),
        ('word-number', generate_admin_url('word-number')),
        ('word-number-word', generate_admin_url('word-number-word')),
        ('adjective-noun-number', generate_admin_url('adjective-noun-number')),
    ]
    
    for style, url in variants:
        print(f"   {url}")
    
    # Супер-безопасный вариант (со случайной строкой)
    random_part = secrets.token_urlsafe(12).replace('-', '_')
    print(f"\n🔒 Супер-безопасный вариант: adm-{random_part}")
    
    print("\n" + "="*50)
    print("💡 Как использовать:")
    print("   1. Скопируйте понравившийся URL")
    print("   2. Добавьте в .env: WAGTAIL_ADMIN_URL=выбранный-url/")
    print("   3. Убедитесь, что в конце есть слеш")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
    
    
#  Как запустить
# В терминале (в папке проекта):

# bash
# python generate_admin_url.py