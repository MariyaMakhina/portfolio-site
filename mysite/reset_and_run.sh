#!/bin/bash
# reset_and_run.sh - Полный сброс и запуск проекта

echo "🧹 Начинаю очистку проекта..."

# 1. Останавливаем все процессы Django/Python
echo "🛑 Останавливаю сервер..."
pkill -f "python manage.py runserver" 2>/dev/null
pkill -f "python3 manage.py runserver" 2>/dev/null
sleep 2

# 1.2. Полностью чистим порт 8000
echo "🔪 Чистка порта 8000..."

# Все возможные команды для освобождения порта
sudo lsof -ti tcp:8000 | xargs sudo kill -9 2>/dev/null
sudo fuser -k 8000/tcp 2>/dev/null
pkill -f "8000" 2>/dev/null
pkill -f "runserver" 2>/dev/null

sleep 2

# 1.3. Проверяем
if lsof -ti tcp:8000 >/dev/null 2>&1; then
    echo "❌ КРИТИЧЕСКАЯ ОШИБКА: Порт 8000 занят!"
    echo "Занявшие процессы:"
    lsof -i tcp:8000
    echo ""
    echo "Завершите процессы вручную и запустите снова"
    exit 1
fi

echo "✅ Порт 8000 свободен"

# 2. Очищаем базу и миграции
echo "🗑️ Удаляю базу данных..."
rm -f db.sqlite3

echo "🗑️ Удаляю старые миграции..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete 2>/dev/null
find . -path "*/migrations/*.pyc" -delete 2>/dev/null

# 3. Очищаем кэш Python
echo "🧼 Очищаю кэш Python..."
find . -name "*.pyc" -delete 2>/dev/null
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# 4. Активируем виртуальное окружение (если есть)
if [ -d ".venwgtl" ]; then
    echo "🔧 Активирую виртуальное окружение..."
    source .venwgtl/bin/activate
elif [ -d "venv" ]; then
    echo "🔧 Активирую виртуальное окружение..."
    source venv/bin/activate
fi

# 5. Создаем миграции
echo "📦 Создаю миграции..."
python manage.py makemigrations

# 6. Применяем миграции
echo "🚀 Применяю миграции..."
python manage.py migrate

# 7. 
echo ""
echo "👤 Создание пользователя mariya..."
echo "Нажмите Enter когда будете готовы вводить данные..."
read

python manage.py createsuperuser --username mariya

echo ""
echo "🚀 ЗАПУСК..."
echo "Админка: http://127.0.0.1:8000/admin"
echo "Логин: mariya"
echo "Пароль: 1234"
echo ""


# 8. Собираем статику (если нужно)
echo "🎨 Собираю статику..."
python manage.py collectstatic --noinput 2>/dev/null || true

# 9. Запускаем сервер в фоне
echo "🚀 Запускаю сервер на http://127.0.0.1:8000..."
echo "📋 Админка: http://127.0.0.1:8000/admin"
echo "👤 Логин: admin"
echo "🔑 Пароль: admin"
echo ""
echo "🛑 Чтобы остановить сервер: Ctrl+C"
echo ""

# Запускаем сервер
python manage.py runserver


# запуск файла - ./reset_and_run.sh


