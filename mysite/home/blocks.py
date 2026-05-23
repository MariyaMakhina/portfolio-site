from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import PageChooserBlock


class HeroBlock(blocks.StructBlock):
    """Hero секция с именем и профессией"""
    name = blocks.CharBlock(max_length=100, help_text="Ваше имя")
    profession = blocks.RichTextBlock(features=['bold', 'italic'], help_text="Ваша профессия/специализация")
    button_text = blocks.CharBlock(max_length=50, required=False, blank=True, help_text="Текст на кнопке")
    button_link = blocks.CharBlock(max_length=200, required=False, blank=True, help_text="Ссылка для кнопки (например, #section-form-back)")
    
    class Meta:
        template = 'blocks/hero_block.html'
        icon = 'user'
        label = 'Hero секция'


class SelectedProjectsBlock(blocks.StructBlock):
    """Блок проектов с выбором из существующих страниц"""
    title = blocks.CharBlock(max_length=200, required=False, default="Мои работы", help_text="Заголовок секции")
    projects = blocks.ListBlock(
        PageChooserBlock(target_model='home.ProjectPage', help_text="Выберите страницу проекта"),
        help_text="Добавьте проекты из списка страниц"
    )
    
    class Meta:
        template = 'blocks/selected_projects_block.html'
        icon = 'image'
        label = 'Проекты (выбор из страниц)'
        collapsed = False


class TemplateBlock(blocks.StructBlock):
    """Блок шаблона"""
    title = blocks.CharBlock(max_length=200, help_text="Название шаблона")
    description = blocks.RichTextBlock(features=['bold', 'italic'], help_text="Описание шаблона")
    image = ImageChooserBlock(help_text="Превью шаблона")
    link_page = PageChooserBlock(required=False, help_text="Выберите страницу шаблона")
    external_link = blocks.URLBlock(required=False, blank=True, help_text="Или внешняя ссылка")
    
    class Meta:
        template = 'blocks/template_block.html'
        icon = 'doc-full'
        label = 'Шаблон'
        collapsed = True


class TemplatesBlock(blocks.StructBlock):
    """Блок со списком шаблонов"""
    title = blocks.CharBlock(max_length=200, help_text="Заголовок секции")
    templates = blocks.ListBlock(TemplateBlock(), help_text="Добавьте шаблоны")
    
    class Meta:
        template = 'blocks/templates_block.html'
        icon = 'list-ul'
        label = 'Секция шаблонов'
        collapsed = True


class EducationItemBlock(blocks.StructBlock):
    """Блок образования/курса"""
    title = blocks.CharBlock(max_length=200, help_text="Название курса/образования")
    institution = blocks.CharBlock(max_length=200, help_text="Учебное заведение/платформа")
    year = blocks.CharBlock(max_length=20, help_text="Год окончания")
    description = blocks.RichTextBlock(features=['bold', 'italic'], required=False, help_text="Описание")
    
    class Meta:
        template = 'blocks/education_item_block.html'
        icon = 'tag'
        label = 'Образование/курс'
        collapsed = True


class SkillItemBlock(blocks.StructBlock):
    """Блок навыка"""
    name = blocks.CharBlock(max_length=100, help_text="Название навыка")
    level = blocks.IntegerBlock(min_value=1, max_value=100, help_text="Уровень владения (1-100)")
    
    class Meta:
        template = 'blocks/skill_item_block.html'
        icon = 'tick'
        label = 'Навык'
        collapsed = True


class EducationSkillsBlock(blocks.StructBlock):
    """Блок с образованием и навыками"""
    education_title = blocks.CharBlock(max_length=200, required=False, default="Образование")
    education = blocks.ListBlock(EducationItemBlock(), required=False, help_text="Образование и курсы")
    skills_title = blocks.CharBlock(max_length=200, required=False, default="Навыки")
    skills = blocks.ListBlock(SkillItemBlock(), required=False, help_text="Навыки")
    
    class Meta:
        template = 'blocks/education_skills_block.html'
        icon = 'tag'
        label = 'Образование и навыки'
        collapsed = True


class ContactFormBlock(blocks.StructBlock):
    """Блок с формой обратной связи"""
    title = blocks.CharBlock(max_length=200, help_text="Заголовок секции")
    intro = blocks.RichTextBlock(features=['bold', 'italic'], required=False, help_text="Текст перед формой")
    button_text = blocks.CharBlock(max_length=50, default="Отправить", help_text="Текст на кнопке")
    thank_you_text = blocks.RichTextBlock(required=False, default="Спасибо! Ваше сообщение отправлено.", help_text="Сообщение после отправки")
    
    class Meta:
        template = 'blocks/contact_form_block.html'
        icon = 'mail'
        label = 'Форма обратной связи'
        collapsed = True


class BlogSectionBlock(blocks.StructBlock):
    """Секция блога"""
    title = blocks.CharBlock(max_length=100, default="Блог", help_text="Заголовок секции")
    button_text = blocks.CharBlock(max_length=50, default="Все статьи", help_text="Текст на кнопке")
    
    class Meta:
        template = 'blocks/blog_section_block.html'
        icon = 'doc-full'
        label = 'Секция блога'
        collapsed = True


class SocialLinksBlock(blocks.StructBlock):
    """Блок с соцсетями"""
    show_in_header = blocks.BooleanBlock(default=True, required=False, help_text="Показывать в шапке")
    show_in_footer = blocks.BooleanBlock(default=True, required=False, help_text="Показывать в подвале")
    
    class Meta:
        template = 'blocks/social_links_block.html'
        icon = 'link'
        label = 'Соцсети'


class ButtonUpBlock(blocks.StructBlock):
    """Блок с кнопкой наверх"""
    
    class Meta:
        template = 'blocks/button_up_block.html'
        icon = 'arrow-up'
        label = 'Кнопка наверх'
        collapsed = True
        

class MediaItemBlock(blocks.StructBlock):
    """Один элемент медиа (изображение, GIF, видео)"""
    media_type = blocks.ChoiceBlock(
        choices=[
            ('image', 'Изображение'),
            ('gif', 'GIF-анимация'),
            ('video', 'Видео'),
        ],
        label="Тип медиа"
    )
    image = ImageChooserBlock(
        required=False,
        label="Изображение или GIF",
        help_text="Загрузите JPG, PNG или GIF"
    )
    video_url = blocks.URLBlock(
        required=False,
        label="Ссылка на видео",
        help_text="YouTube, Vimeo или прямой URL"
    )
    caption = blocks.CharBlock(
        required=False,
        label="Подпись",
        help_text="Краткое описание"
    )
    
    class Meta:
        icon = 'media'
        label = 'Медиа файл'
        template = 'blocks/media_item.html'


class TabItemBlock(blocks.StructBlock):
    """Одна вкладка"""
    title = blocks.CharBlock(
        required=True,
        label="Название вкладки",
        help_text="Например: Редактирование меню"
    )
    content = blocks.RichTextBlock(
        required=True,
        label="Содержимое вкладки",
        help_text="Текст, который будет внутри вкладки"
    )
    icon_svg = ImageChooserBlock(
        required=False,
        label="SVG иконка",
        help_text="Загрузите SVG файл"
    )
    # НОВОЕ ПОЛЕ: галерея внутри вкладки
    gallery = blocks.ListBlock(
        MediaItemBlock(),
        required=False,
        label="Медиа галерея",
        help_text="Добавьте изображения, GIF или видео для этой вкладки"
    )
    
    class Meta:
        icon = 'doc-full'
        label = 'Вкладка'
        template = 'blocks/tab_item.html'


class TabsBlock(blocks.StructBlock):
    """Блок с вкладками (табами)"""
    title = blocks.CharBlock(
        required=False,
        label="Заголовок блока",
        help_text="Отображается над вкладками"
    )
    tabs = blocks.ListBlock(
        TabItemBlock(),
        label="Вкладки",
        help_text="Добавьте от 2 до 5 вкладок"
    )
    
    class Meta:
        icon = 'folder-open-1'
        label = 'Блок с вкладками'
        template = 'blocks/tabs_block.html'
        
class CarouselImageBlock(blocks.StructBlock):
    """Одно изображение для карусели"""
    image = ImageChooserBlock(required=True, label="Изображение")
    caption = blocks.CharBlock(required=False, label="Подпись", help_text="Краткое описание скриншота")
    
    class Meta:
        icon = 'image'
        label = 'Слайд'
        template = 'blocks/carousel_image_block.html'


class CarouselBlock(blocks.StructBlock):
    """Карусель скриншотов"""
    title = blocks.CharBlock(required=False, label="Заголовок блока", help_text="Например: Как выглядит сайт")
    slides = blocks.ListBlock(
        CarouselImageBlock(),
        label="Слайды",
        help_text="Добавьте скриншоты сайта (рекомендуется ширина 1200px+)"
    )
    
    class Meta:
        icon = 'image'
        label = 'Карусель скриншотов'
        template = 'blocks/carousel_block.html'
        
        
class ContentWithIconBlock(blocks.StructBlock):
    """Блок контента с иконкой, текстом и изображением (обтекание)"""
    
    # Заголовок с иконкой
    title = blocks.CharBlock(
        required=True,
        label="Заголовок",
        help_text="Заголовок блока"
    )
    
    # Иконка (можно SVG или эмодзи)
    icon = blocks.CharBlock(
        required=False,
        label="Иконка (эмодзи)",
        help_text="Например: 🚀, 📝, 🖼️, 🔧",
        default="📌"
    )
    
    # Или загрузить свою SVG иконку
    icon_svg = ImageChooserBlock(
        required=False,
        label="SVG иконка",
        help_text="Или загрузите свой SVG файл"
    )
    
    # Текст
    text = blocks.RichTextBlock(
        required=True,
        label="Текст",
        help_text="Основное содержание блока"
    )
    
    # Изображение
    image = ImageChooserBlock(
        required=False,
        label="Изображение",
        help_text="Фото, скриншот или GIF"
    )
    
    # Положение изображения
    image_position = blocks.ChoiceBlock(
        choices=[
            ('left', 'Слева от текста'),
            ('right', 'Справа от текста'),
        ],
        default='left',
        label="Положение изображения",
        help_text="С какой стороны будет изображение относительно текста"
    )
    
    # Ширина изображения
    image_width = blocks.ChoiceBlock(
        choices=[
            ('30', '30%'),
            ('40', '40%'),
            ('50', '50%'),
            ('60', '60%'),
        ],
        default='40',
        label="Ширина изображения",
        help_text="Процент от ширины блока"
    )
    
    class Meta:
        icon = 'image'
        label = 'Блок с обтеканием текстом избржн'
        template = 'blocks/content_with_icon_block.html'
        
class ClearFloatBlock(blocks.StructBlock):
    """Блок для сброса обтекания (останавливает float)"""
    
    line_visible = blocks.BooleanBlock(
        required=False,
        default=True,
        label="Показывать разделитель",
        help_text="Добавить видимую линию между блоками"
    )
    
    class Meta:
        icon = 'horizontalrule'
        label = 'Сброс обтекания'
        template = 'blocks/clear_float_block.html'