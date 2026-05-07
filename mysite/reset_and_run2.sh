

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

# Запускаем сервер
python manage.py runserver


# запуск файла - ./reset_and_run2.sh

(
python manage.py makemigrations
python manage.py migrate
)


