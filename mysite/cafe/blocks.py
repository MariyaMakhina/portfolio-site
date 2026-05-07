from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock


class ContactInfoBlock(blocks.StructBlock):
    """Блок контактной информации"""
    title = blocks.CharBlock(required=True, label="Заголовок")
    # value = blocks.TextBlock(required=True, label="Значение")
    # icon = blocks.CharBlock(required=False, label="Иконка (CSS класс)")
    
    class Meta:
        icon = 'info-circle'
        label = 'Контактная информация'
        template = 'cafe/blocks/contact_info.html'


class MapBlock(blocks.StructBlock):
    """Блок карты"""
    title = blocks.CharBlock(required=False, label="Заголовок")
    map_code = blocks.TextBlock(
        required=True,
        label='Код карты',
        help_text='Вставьте iframe код карты (Яндекс.Карты или Google Maps)'
    )
    
    class Meta:
        icon = 'site'
        label = 'Карта'
        template = 'cafe/blocks/map_block.html'


class MenuGalleryBlock(blocks.StructBlock):
    """Блок галереи меню"""
    title = blocks.CharBlock(
        required=False,
        label="Заголовок блока",
        help_text="Заголовок, который отображается на странице"
    )
    categories = blocks.ListBlock(
        SnippetChooserBlock('cafe.MenuCategory'),
        label="Категории для отображения"
    )
    
    class Meta:
        icon = 'grip'
        label = 'Галерея меню'
        template = 'cafe/blocks/menu_gallery.html'


class GalleryCarouselBlock(blocks.StructBlock):
    """Слайд галереи"""
    title = blocks.CharBlock(
        required=False,
        label="Заголовок на странице"
    )
    image = ImageChooserBlock(required=True, label="Фото")
    description = blocks.RichTextBlock(
        required=False,
        label="Описание",
    )
    
    class Meta:
        icon = 'image'
        label = 'Слайд галереи'
        template = 'cafe/blocks/gallery_slide.html'


class ContactBlock(blocks.StructBlock):
    """Блок контактов"""
    title = blocks.CharBlock(
        required=False,
        label="Заголовок на странице"
    )
    left_content = blocks.StreamBlock([
        ('contact_info', ContactInfoBlock()),
    ], label="Левая колонка")
    
    right_content = blocks.StreamBlock([
        ('map', MapBlock()),
    ], max_num=1, label="Правая колонка (карта)")
    
    class Meta:
        icon = 'site'
        label = 'Блок контактов'
        template = 'cafe/blocks/contact_block.html'


class BookingFormBlock(blocks.StructBlock):
    """Настройки формы бронирования"""
    title = blocks.CharBlock(
        required=False,
        label="Заголовок на странице"
    )
    name_label = blocks.CharBlock(default="Имя", label="Подпись поля Имя")
    name_placeholder = blocks.CharBlock(default="Введите ваше имя", label="Placeholder")
    
    phone_label = blocks.CharBlock(default="Телефон", label="Подпись поля Телефон")
    phone_placeholder = blocks.CharBlock(default="+7 (999) 123-45-67", label="Placeholder")
    
    date_label = blocks.CharBlock(default="Дата", label="Подпись поля Дата")
    time_label = blocks.CharBlock(default="Время", label="Подпись поля Время")
    
    persons_label = blocks.CharBlock(default="Количество персон", label="Подпись поля")
    persons_placeholder = blocks.CharBlock(default="2", label="Placeholder")
    
    wishes_label = blocks.CharBlock(default="Пожелания", label="Подпись поля Пожелания")
    wishes_placeholder = blocks.CharBlock(default="Особые пожелания...", label="Placeholder")
    
    class Meta:
        icon = 'form'
        label = 'Настройки формы'
        template = 'cafe/blocks/booking_form_settings.html'