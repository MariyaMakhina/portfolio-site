from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index

from ..blocks import (
    MenuGalleryBlock,
    GalleryCarouselBlock,
    ContactBlock,
    BookingFormBlock,
)


class CafePage(Page):
    """Главная страница кафе"""
    
    # === 1. Hero секция ===
    hero_background = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Фоновое изображение"
    )
    cafe_name = models.CharField(
        max_length=200,
        verbose_name="Название кафе"
    )
    slogan = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Слоган"
    )
    description = models.TextField(
        "Описание",
        blank=True,
    )
    hero_booking_button_text = models.CharField(
        max_length=50,
        default="Забронировать стол",
        verbose_name="Текст кнопки бронирования"
    )
    hero_menu_button_text = models.CharField(
        max_length=50,
        default="Наше меню",
        verbose_name="Текст кнопки меню"
    )
    
    # === 2. Меню (галерея) ===
    show_menu_section = models.BooleanField(
        default=True,
        verbose_name="Показывать секцию меню"
    )
    menu_title = models.CharField(
        max_length=200,
        default="Наше меню",
        verbose_name="Заголовок секции меню (на странице)"
    )
    menu_nav_title = models.CharField(
        max_length=200,
        default="Меню",
        verbose_name="Название в навигации сайта",
        help_text="Как этот раздел будет называться в меню сайта"
    )
    menu_background = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Фоновое изображение для секции меню"
    )
    menu_gallery = StreamField(
        [('menu_gallery', MenuGalleryBlock())],
        blank=True,
        use_json_field=True,
        verbose_name="Галерея меню"
    )
    
    # === 3. Галерея ===
    show_gallery_section = models.BooleanField(
        default=True,
        verbose_name="Показывать секцию галереи"
    )
    gallery_title = models.CharField(
        max_length=200,
        default="Фотогалерея",
        verbose_name="Заголовок секции галереи (на странице)"
    )
    gallery_nav_title = models.CharField(
        max_length=200,
        default="Галерея",
        verbose_name="Название в навигации сайта",
        help_text="Как этот раздел будет называться в меню сайта"
    )
    gallery_background = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Фоновое изображение для секции галереи"
    )
    gallery_carousel = StreamField(
        [('gallery_slide', GalleryCarouselBlock())],
        blank=True,
        use_json_field=True,
        verbose_name="Слайды галереи"
    )
    
    # === 4. Форма бронирования ===
    show_booking_section = models.BooleanField(
        default=True,
        verbose_name="Показывать секцию бронирования"
    )
    booking_title = models.CharField(
        max_length=200,
        default="Забронировать стол",
        verbose_name="Заголовок секции бронирования (на странице)"
    )
    booking_nav_title = models.CharField(
        max_length=200,
        default="Бронь",
        verbose_name="Название в навигации сайта",
        help_text="Как этот раздел будет называться в меню сайта"
    )
    booking_background = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Фоновое изображение для секции бронирования"
    )
    booking_intro = RichTextField(
        features=['bold', 'italic'],
        blank=True,
        verbose_name="Текст перед формой"
    )
    booking_form = StreamField(
        [('booking_form', BookingFormBlock())],
        blank=True,
        use_json_field=True,
        verbose_name="Настройки формы"
    )
    booking_button_text = models.CharField(
        max_length=50,
        default="Забронировать",
        verbose_name="Текст кнопки"
    )
    booking_success_message = RichTextField(
        blank=True,
        verbose_name="Сообщение после отправки",
        default="<p>Спасибо! Мы свяжемся с вами для подтверждения брони.</p>"
    )
    
    # === 5. Контакты ===
    show_contacts_section = models.BooleanField(
        default=False,
        verbose_name="Показывать секцию контактов"
    )
    contacts_title = models.CharField(
        max_length=200,
        default="Контакты",
        verbose_name="Заголовок секции контактов (на странице)"
    )
    contacts_nav_title = models.CharField(
        max_length=200,
        default="Контакты",
        verbose_name="Название в навигации сайта",
        help_text="Как этот раздел будет называться в меню сайта"
    )
    contacts_background = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Фоновое изображение для секции контактов"
    )
    contacts = StreamField(
        [('contact_block', ContactBlock())],
        blank=True,
        use_json_field=True,
        verbose_name="Блок контактов"
    )
    
    # === Настройки email ===
    from_address = models.EmailField(
        max_length=255,
        blank=True,
        default='noreply@cafe.com',
        verbose_name="Email отправителя"
    )
    to_address = models.EmailField(
        max_length=255,
        blank=True,
        verbose_name="Email получателя"
    )
    email_subject = models.CharField(
        max_length=255,
        blank=True,
        default="Новая заявка на бронирование",
        verbose_name="Тема письма"
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_background'),
            FieldPanel('cafe_name'),
            FieldPanel('slogan'),
            FieldPanel('description'),
            FieldPanel('hero_booking_button_text'),
            FieldPanel('hero_menu_button_text'),
        ], heading="Hero секция", classname="collapsible"),
        
        MultiFieldPanel([
            FieldPanel('show_menu_section'),
            FieldPanel('menu_title'),
            FieldPanel('menu_nav_title'),
            FieldPanel('menu_background'),
            FieldPanel('menu_gallery'),
        ], heading="Меню", classname="collapsible collapsed"),
        
        MultiFieldPanel([
            FieldPanel('show_gallery_section'),
            FieldPanel('gallery_title'),
            FieldPanel('gallery_nav_title'),
            FieldPanel('gallery_background'),
            FieldPanel('gallery_carousel'),
        ], heading="Галерея", classname="collapsible collapsed"),
        
        MultiFieldPanel([
            FieldPanel('show_booking_section'),
            FieldPanel('booking_title'),
            FieldPanel('booking_nav_title'),
            FieldPanel('booking_background'),
            FieldPanel('booking_intro'),
            FieldPanel('booking_form'),
            FieldPanel('booking_button_text'),
            FieldPanel('booking_success_message'),
        ], heading="Бронирование", classname="collapsible collapsed"),
        
        MultiFieldPanel([
            FieldPanel('show_contacts_section'),
            FieldPanel('contacts_title'),
            FieldPanel('contacts_nav_title'),
            FieldPanel('contacts_background'),
            FieldPanel('contacts'),
        ], heading="Контакты", classname="collapsible collapsed"),
        
        MultiFieldPanel([
            FieldPanel('from_address'),
            FieldPanel('to_address'),
            FieldPanel('email_subject'),
        ], heading="Настройки email", classname="collapsible collapsed"),
    ]
    
    class Meta:
        verbose_name = "Страница кафе"

    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            from ..utils import handle_booking_form
            return handle_booking_form(self, request)
        return super().serve(request, *args, **kwargs)
    
    def get_menu_slides(self):
        """
        Генерирует слайды для меню.
        Один слайд = один блок.
        Если товаров много, категория разбивается на несколько блоков.
        """
        from .menu_models import MenuCategory, VolumeOption

        # Получаем все активные категории
        categories = MenuCategory.objects.filter(is_active=True).prefetch_related(
            'items', 'items__prices', 'items__prices__volume'
        ).order_by('sort_order')

        if not categories:
            return []

        ITEMS_PER_BLOCK = 5  # Сколько товаров в одном блоке
        slides = []  # Здесь будут все слайды (каждый слайд = один блок)

        for category in categories:
            items = list(category.items.filter(is_active=True).order_by('sort_order'))

            if not items:
                continue

            # Получаем все volume_id, которые используются в товарах этой категории
            used_volume_ids = set()
            for item in items:
                for price in item.prices.all():
                    if price.is_active:
                        used_volume_ids.add(price.volume_id)

            # Получаем объекты Volume для этой категории
            category_volumes = VolumeOption.objects.filter(
                id__in=used_volume_ids,
                is_active=True
            ).order_by('sort_order')

            # Разбиваем товары категории на блоки по ITEMS_PER_BLOCK
            for i in range(0, len(items), ITEMS_PER_BLOCK):
                chunk = items[i:i + ITEMS_PER_BLOCK]
                slides.append({
                    'category': category,
                    'items': chunk,
                    'volumes': category_volumes,  # Только объемы этой категории
                    'is_first': i == 0,
                    'is_last': i + ITEMS_PER_BLOCK >= len(items),
                    'block_index': i // ITEMS_PER_BLOCK + 1,
                    'total_blocks': (len(items) + ITEMS_PER_BLOCK - 1) // ITEMS_PER_BLOCK,
                    'category_name': category.name,
                    'category_image': category.image
                })

        return slides

    def get_context(self, request, *args, **kwargs):
        """Добавляет данные в контекст шаблона"""
        context = super().get_context(request, *args, **kwargs)
        
        try:
            from home.models import SocialMediaSettings
            context['social_settings'] = SocialMediaSettings.for_request(request)
        except ImportError:
            context['social_settings'] = None
        
        # Добавляем слайды для меню
        context['menu_slides'] = self.get_menu_slides()
        
        return context