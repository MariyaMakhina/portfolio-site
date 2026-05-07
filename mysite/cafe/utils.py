from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
import os
from django.conf import settings


def handle_booking_form(page, request):
    """Обработка формы бронирования"""
    
    # Получаем данные
    name = request.POST.get('name', '').strip()
    phone = request.POST.get('phone', '').strip()
    booking_date = request.POST.get('booking_date', '').strip()
    booking_time = request.POST.get('booking_time', '').strip()
    persons = request.POST.get('persons', '').strip()
    wishes = request.POST.get('wishes', '').strip()
    
    # Валидация
    errors = []
    if not name:
        errors.append('Имя обязательно')
    if not phone:
        errors.append('Телефон обязателен')
    if not booking_date:
        errors.append('Дата бронирования обязательна')
    if not booking_time:
        errors.append('Время бронирования обязательно')
    if not persons or not persons.isdigit() or int(persons) < 1:
        errors.append('Укажите корректное количество персон')
    
    if errors:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': errors}, status=400)
        
        context = page.get_context(request)
        context['form_errors'] = errors
        context['form_data'] = request.POST
        return page.render(request, context)
    
    try:
        # Сохраняем в файл
        save_booking(page, {
            'name': name, 'phone': phone, 'booking_date': booking_date,
            'booking_time': booking_time, 'persons': persons, 'wishes': wishes
        })
        
        # Отправляем email
        send_booking_email(page, {
            'name': name, 'phone': phone, 'booking_date': booking_date,
            'booking_time': booking_time, 'persons': persons, 'wishes': wishes
        })
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Бронирование отправлено'})
        
        context = page.get_context(request)
        context['form_success'] = True
        return page.render(request, context)
        
    except Exception as e:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        
        context = page.get_context(request)
        context['form_errors'] = [f'Ошибка: {str(e)}']
        return page.render(request, context)


def save_booking(page, data):
    """Сохраняет бронирование в файл"""
    bookings_dir = os.path.join(settings.BASE_DIR, 'bookings')
    os.makedirs(bookings_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'booking_{timestamp}.txt'
    filepath = os.path.join(bookings_dir, filename)
    
    content = f"""
НОВОЕ БРОНИРОВАНИЕ
Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}
Страница: {page.title}

Имя: {data['name']}
Телефон: {data['phone']}
Дата брони: {data['booking_date']}
Время: {data['booking_time']}
Персон: {data['persons']}
Пожелания: {data['wishes']}
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def send_booking_email(page, data):
    """Отправляет email с бронированием"""
    if not page.to_address:
        return
    
    subject = page.email_subject
    message = f"""
Новая заявка на бронирование!

Имя: {data['name']}
Телефон: {data['phone']}
Дата: {data['booking_date']}
Время: {data['booking_time']}
Количество персон: {data['persons']}

Пожелания:
{data['wishes']}

Страница: {page.title}
URL: {page.full_url or 'Локальная разработка'}
"""
    
    send_mail(
        subject=subject,
        message=message,
        from_email=page.from_address,
        recipient_list=[page.to_address],
        fail_silently=True,
    )