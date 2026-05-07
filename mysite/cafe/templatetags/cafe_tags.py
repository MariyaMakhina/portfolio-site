from django import template
import re 

register = template.Library()


@register.filter
def get_price_for_volume(prices, volume_id):
    """Фильтр для получения цены товара по объему"""
    if not prices:
        return None
    try:
        volume_id = int(volume_id)
        for price in prices:
            if price.volume_id == volume_id and price.is_active:
                return price
    except (ValueError, TypeError):
        pass
    return None


@register.simple_tag
def image_url(image, filter_spec):
    """Возвращает URL изображения с применением фильтра"""
    if not image:
        return ''
    return image.get_rendition(filter_spec).url


@register.filter
def get_item(dictionary, key):
    """Получение элемента из словаря по ключу"""
    return dictionary.get(key, '')

@register.filter
def format_phone(phone):
    """
    Форматирует номер телефона в красивый вид
    +7 (999) 123-45-67
    """
    if not phone:
        return phone
    
    # Удаляем все нецифровые символы
    digits = re.sub(r'\D', '', str(phone))
    
    # Проверяем длину и форматируем
    if len(digits) == 11:  # Россия: 7XXXXXXXXXX
        return f"+{digits[0]} ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    elif len(digits) == 10:  # 10 цифр
        return f"+7 ({digits[0:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:10]}"
    else:
        return phone  # Если не получается отформатировать, возвращаем как есть