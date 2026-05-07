#!/bin/bash

# Папка для бэкапов
BACKUP_DIR="/home/mariya/Desktop/Progrm/wagtail/backups"
DATE=$(date +%Y%m%d_%H%M%S)
CURRENT_DIR=$(pwd)

echo "📁 Бэкап из текущей папки: $CURRENT_DIR"

# Создаем папку для бэкапов
mkdir -p "$BACKUP_DIR"

# 1. Бэкап базы данных
if [ -f "db.sqlite3" ]; then
    cp "db.sqlite3" "$BACKUP_DIR/db_$DATE.sqlite3"
    echo "✅ База данных: db.sqlite3"
elif [ -f "../db.sqlite3" ]; then
    cp "../db.sqlite3" "$BACKUP_DIR/db_$DATE.sqlite3"
    echo "✅ База данных: ../db.sqlite3"
else
    echo "⚠️ База данных не найдена"
fi

# 2. Бэкап MEDIA файлов (то, что загружено через админку)
MEDIA_FOUND=0
if [ -d "media" ]; then
    tar -czf "$BACKUP_DIR/media_$DATE.tar.gz" media/
    echo "✅ MEDIA файлы: media/ (загруженные пользователями)"
    MEDIA_FOUND=1
elif [ -d "../media" ]; then
    tar -czf "$BACKUP_DIR/media_$DATE.tar.gz" -C .. media/
    echo "✅ MEDIA файлы: ../media/ (загруженные пользователями)"
    MEDIA_FOUND=1
fi

if [ $MEDIA_FOUND -eq 0 ]; then
    echo "⚠️ Папка media не найдена"
fi

# 3. Бэкап STATIC файлов (CSS, JS, изображения дизайна)
STATIC_FOUND=0
# Создаем временную папку для сбора всех static
TEMP_STATIC="/tmp/static_backup_$DATE"
mkdir -p "$TEMP_STATIC"

# Ищем все папки static в проекте
echo "🔍 Ищем STATIC файлы (CSS, JS, изображения дизайна)..."

# Текущая папка
if [ -d "static" ]; then
    cp -r "static" "$TEMP_STATIC/static_root/"
    echo "  - static/ (корневая)"
    STATIC_FOUND=1
fi

# Приложения с static
for app in home cafe blog search; do
    if [ -d "$app/static" ]; then
        mkdir -p "$TEMP_STATIC/apps/$app"
        cp -r "$app/static" "$TEMP_STATIC/apps/$app/"
        echo "  - $app/static/"
        STATIC_FOUND=1
    fi
done

# Родительская папка (если static выше)
if [ -d "../static" ]; then
    cp -r "../static" "$TEMP_STATIC/static_parent/"
    echo "  - ../static/ (родительская)"
    STATIC_FOUND=1
fi

if [ $STATIC_FOUND -eq 1 ]; then
    # Архивируем все собранные static файлы
    tar -czf "$BACKUP_DIR/static_$DATE.tar.gz" -C "$TEMP_STATIC" .
    echo "✅ STATIC файлы: static_$DATE.tar.gz"
    rm -rf "$TEMP_STATIC"
else
    echo "⚠️ STATIC файлы не найдены"
fi

# 4. Бэкап кода (без виртуального окружения и медиа)
echo "📦 Архивирую код из текущей папки..."
tar -czf "$BACKUP_DIR/code_$DATE.tar.gz" \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    --exclude='media' \
    --exclude='*.tar.gz' \
    .

# 5. Список пакетов
if [ -d "venv" ] && [ -f "venv/bin/activate" ]; then
    source "venv/bin/activate"
    pip freeze > "$BACKUP_DIR/requirements_$DATE.txt"
    deactivate
    echo "✅ Список пакетов: venv/"
elif [ -d "../venv" ] && [ -f "../venv/bin/activate" ]; then
    source "../venv/bin/activate"
    pip freeze > "$BACKUP_DIR/requirements_$DATE.txt"
    deactivate
    echo "✅ Список пакетов: ../venv/"
else
    echo "⚠️ Виртуальное окружение не найдено"
fi

# Результат
echo ""
echo "✅ РЕЗЕРВНОЕ КОПИРОВАНИЕ ЗАВЕРШЕНО!"
echo "📁 Бэкапы сохранены в: $BACKUP_DIR"
echo ""
echo "📋 Созданы файлы:"
ls -lh "$BACKUP_DIR" | grep "$DATE" | awk '{print "  " $9 " (" $5 ")"}'

# Сделай скрипт исполняемым:

# bash
# chmod +x backup.sh

# Запусти:

# bash
# ./backup.sh