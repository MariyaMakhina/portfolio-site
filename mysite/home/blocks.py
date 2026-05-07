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