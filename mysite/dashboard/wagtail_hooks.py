from django.urls import reverse
from wagtail.admin.menu import MenuItem
from wagtail import hooks
from wagtail.contrib.settings.registry import register_setting
from .models import AnalyticsSettings

@hooks.register('register_admin_menu_item')
def register_dashboard_menu():
    return MenuItem(
        'Дашборд',
        reverse('dashboard:index'),
        icon_name='home',
        order=1
    )

# Регистрируем модель настроек вручную
register_setting(AnalyticsSettings)