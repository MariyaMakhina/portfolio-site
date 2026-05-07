from wagtail.admin.menu import MenuItem
from wagtail import hooks


@hooks.register('register_admin_menu_item')
def register_dashboard_menu():
    return MenuItem(
        'Дашборд',
        '/admin/dashboard/',  # Используем прямой URL
        icon_name='home',
        order=1
    )