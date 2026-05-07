#!/bin/bash

# Папка с бэкапами
BACKUP_DIR="/home/mariya/Desktop/Progrm/wagtail/backups"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=================================================="
echo "🔄 ВОССТАНОВЛЕНИЕ ПРОЕКТА ИЗ БЭКАПА"
echo "=================================================="
echo ""

# Показываем доступные бэкапы
echo -e "${BLUE}📋 Доступные бэкапы:${NC}"
ls -lh "$BACKUP_DIR" | grep -E "code_.*\.tar\.gz|media_.*\.tar\.gz|db_.*\.sqlite3" | sort -r

echo ""
echo -e "${YELLOW}⚠️  ВНИМАНИЕ: ТЕКУЩИЙ ПРОЕКТ БУДЕТ ПОЛНОСТЬЮ ЗАМЕНЕН!${NC}"
echo -e "${YELLOW}⚠️  Все текущие файлы будут удалены без возможности восстановления!${NC}"
echo ""

# Спрашиваем дату бэкапа
echo -e "${BLUE}Введите дату бэкапа для восстановления (например, 20260305_053439):${NC}"
read BACKUP_DATE

# Проверяем существование файлов
CODE_FILE="$BACKUP_DIR/code_${BACKUP_DATE}.tar.gz"
MEDIA_FILE="$BACKUP_DIR/media_${BACKUP_DATE}.tar.gz"
DB_FILE="$BACKUP_DIR/db_${BACKUP_DATE}.sqlite3"

if [ ! -f "$CODE_FILE" ]; then
    echo -e "${RED}❌ Ошибка: Файл code_${BACKUP_DATE}.tar.gz не найден!${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Найдены файлы:${NC}"
echo "   code: $CODE_FILE"
[ -f "$MEDIA_FILE" ] && echo "   media: $MEDIA_FILE" || echo "   media: не найден (пропускаем)"
[ -f "$DB_FILE" ] && echo "   db: $DB_FILE" || echo "   db: не найден (пропускаем)"

echo ""
echo -e "${YELLOW}⚠️  ПОСЛЕДНЕЕ ПРЕДУПРЕЖДЕНИЕ!${NC}"
echo -e "${YELLOW}   Текущая папка: $(pwd)${NC}"
echo -e "${YELLOW}   Все файлы в этой папке будут УДАЛЕНЫ!${NC}"
echo ""
echo -e "${BLUE}Продолжить восстановление? (yes/NO):${NC}"
read CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo -e "${RED}❌ Восстановление отменено${NC}"
    exit 0
fi

# 1. Останавливаем сервер, если запущен
echo -e "${BLUE}➡️ Останавливаем сервер (если запущен)...${NC}"
pkill -f "manage.py runserver" 2>/dev/null || true
sleep 2

# 2. Деактивируем виртуальное окружение
echo -e "${BLUE}➡️ Деактивируем виртуальное окружение...${NC}"
deactivate 2>/dev/null || true

# 3. Удаляем ВСЁ в текущей папке (кроме venv, если есть)
echo -e "${BLUE}➡️ Удаляем текущие файлы...${NC}"

# Сохраняем путь к venv если есть
VENV_PATH=""
if [ -d "venv" ]; then
    VENV_PATH="venv"
    echo "   📦 Виртуальное окружение будет сохранено"
fi

# Удаляем всё, кроме venv
for item in *; do
    if [ "$item" != "venv" ]; then
        rm -rf "$item"
        echo "   Удалено: $item"
    fi
done

# Скрытые файлы (кроме . и ..)
for item in .[^.]* ..?*; do
    if [ "$item" != ".venv" ] && [ "$item" != "." ] && [ "$item" != ".." ]; then
        rm -rf "$item" 2>/dev/null || true
    fi
done

# 4. Восстанавливаем код
echo -e "${BLUE}➡️ Восстанавливаем код из code_${BACKUP_DATE}.tar.gz...${NC}"
tar -xzf "$CODE_FILE" -C .

# 5. Восстанавливаем медиафайлы (если есть)
if [ -f "$MEDIA_FILE" ]; then
    echo -e "${BLUE}➡️ Восстанавливаем медиафайлы из media_${BACKUP_DATE}.tar.gz...${NC}"
    tar -xzf "$MEDIA_FILE" -C .
else
    echo -e "${YELLOW}⚠️ Медиафайлы пропущены (файл не найден)${NC}"
fi

# 6. Восстанавливаем базу данных (если есть)
if [ -f "$DB_FILE" ]; then
    echo -e "${BLUE}➡️ Восстанавливаем базу данных из db_${BACKUP_DATE}.sqlite3...${NC}"
    cp "$DB_FILE" "./db.sqlite3"
else
    echo -e "${YELLOW}⚠️ База данных пропущена (файл не найден)${NC}"
fi

# 7. Восстанавливаем виртуальное окружение
echo -e "${BLUE}➡️ Настраиваем виртуальное окружение...${NC}"

# Если venv был сохранён, используем его
if [ -n "$VENV_PATH" ] && [ -d "venv" ]; then
    echo "   ✅ Используем существующее venv"
else
    # Создаём новое venv
    echo "   📦 Создаём новое виртуальное окружение..."
    python3 -m venv venv
fi

# Активируем и устанавливаем зависимости
source venv/bin/activate

# Устанавливаем зависимости если есть requirements.txt
if [ -f "requirements.txt" ]; then
    echo "   📦 Устанавливаем зависимости из requirements.txt..."
    pip install -r requirements.txt
elif [ -f "$BACKUP_DIR/requirements_${BACKUP_DATE}.txt" ]; then
    echo "   📦 Устанавливаем зависимости из бэкапа..."
    pip install -r "$BACKUP_DIR/requirements_${BACKUP_DATE}.txt"
else
    echo "   ⚠️ Файл requirements.txt не найден, устанавливаем базовые пакеты..."
    pip install wagtail django
fi

# 8. Применяем миграции (если есть база)
if [ -f "db.sqlite3" ]; then
    echo -e "${BLUE}➡️ Применяем миграции...${NC}"
    python manage.py migrate --noinput
fi

# 9. Собираем статику
echo -e "${BLUE}➡️ Собираем статические файлы...${NC}"
python manage.py collectstatic --noinput

# 10. Проверяем результат
echo ""
echo "=================================================="
echo -e "${GREEN}✅ ВОССТАНОВЛЕНИЕ ЗАВЕРШЕНО!${NC}"
echo "=================================================="
echo ""
echo -e "${BLUE}📁 Содержимое папки после восстановления:${NC}"
ls -la

echo ""
echo -e "${BLUE}🚀 Для запуска сервера выполните:${NC}"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""

# Запускаем сервер?
echo -e "${BLUE}Запустить сервер сейчас? (yes/NO):${NC}"
read RUN_SERVER

if [ "$RUN_SERVER" = "yes" ]; then
    echo -e "${GREEN}🚀 Запускаем сервер...${NC}"
    python manage.py runserver
else
    echo -e "${YELLOW}✅ Готово. Сервер не запущен.${NC}"
fi

#=============================================
# 1. Сделайте скрипт исполняемым:
# bash
# chmod +x /home/mariya/Desktop/Progrm/wagtail/backups/restore_current.sh
# 2. Перейдите в папку проекта, который хотите восстановить:
# bash
# cd /home/mariya/Desktop/Progrm/wagtail/websites/my_portfolio/portfolio_site_4/mysite
# 3. Запустите скрипт восстановления:
# bash
# /home/mariya/Desktop/Progrm/wagtail/backups/restore_current.sh
# 4. Введите дату бэкапа:
# text
# Введите дату бэкапа для восстановления (например, 20260305_053439):
# 20260305_053439
# 5. Подтвердите восстановление:
# text
# ⚠️ ПОСЛЕДНЕЕ ПРЕДУПРЕЖДЕНИЕ!
#    Текущая папка: /home/mariya/Desktop/Progrm/wagtail/websites/my_portfolio/portfolio_site_4/mysite
#    Все файлы в этой папке будут УДАЛЕНЫ!

# Продолжить восстановление? (yes/NO):
# yes