from django.db import models
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images import get_image_model_string

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from wagtail.search import index



class BlogHomePage(Page):
    """Главная страница студии"""
    
    # 1. Фоновое фото
    background_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        help_text='Фоновое изображение на всю страницу'
    )
    
    # 2. Название студии
    studio_name = models.CharField(
        max_length=100,
        default='СЕВЕРНЫЙ СВЕТ',
        help_text='Название студии (по центру)'
    )
    
    # 3. Описание под названием
    studio_tagline = models.CharField(
        max_length=200,
        default='архитектура · интерьеры · события · детали',
        help_text='Короткое описание под названием'
    )
    
    # 4. Телефон
    phone_text = models.CharField(
        max_length=20,
        default='+7 999 123-45-67',
        help_text='Номер телефона'
    )
    
    # 5. Атрибуция фото
    photo_credit = models.CharField(
        max_length=100,
        default='Фото: Freepik',
        help_text='Подпись об авторстве фото'
    )
    
    # 6. Страница портфолио (на неё будут вести все категории)
    portfolio_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Страница портфолио',
        help_text='Страница, на которую будут вести категории (обычно /portfolio/)'
    )
    
    # 7. Названия категорий (без slug)
    category_1_name = models.CharField(
        max_length=50, 
        default='Отели',
        verbose_name='Категория 1',
        help_text='Название первой категории'
    )
    
    category_2_name = models.CharField(
        max_length=50, 
        default='Фасады',
        verbose_name='Категория 2'
    )
    
    category_3_name = models.CharField(
        max_length=50, 
        default='События',
        verbose_name='Категория 3'
    )
    
    category_4_name = models.CharField(
        max_length=50, 
        default='Детали',
        verbose_name='Категория 4'
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('background_image'),
                FieldPanel('photo_credit'),
            ],
            heading="Фон и атрибуция"
        ),
        
        MultiFieldPanel(
            [
                FieldPanel('studio_name'),
                FieldPanel('studio_tagline'),
            ],
            heading="Название и описание"
        ),
        
        MultiFieldPanel(
            [
                FieldPanel('phone_text'),
            ],
            heading="Контакты"
        ),
        
        MultiFieldPanel(
            [
                FieldPanel('portfolio_page'),
            ],
            heading="Страница портфолио"
        ),
        
        MultiFieldPanel(
            [
                FieldPanel('category_1_name'),
                FieldPanel('category_2_name'),
                FieldPanel('category_3_name'),
                FieldPanel('category_4_name'),
            ],
            heading="Категории (названия)"
        ),
    ]
    # Разрешаем добавлять только проекты (ProjectPage), блог 'blog.BlogIndexPage' как дочерние
    subpage_types = ['blog.BlogPortfolioPage', 'blog.BlogIndexPage', 'blog.BlogAboutPage', 'blog.ContactPage']
    
    class Meta:
        verbose_name = "Главная страница фотостудии"
        verbose_name_plural = "Главные страницы фотостудии"
        
# ========== НОВЫЕ МОДЕЛИ ДЛЯ ПОРТФОЛИО ==========

class BlogPortfolioPage(Page):
    """Страница портфолио — список проектов"""
    
    intro = RichTextField(
        blank=True,
        help_text='Краткое вступление на странице портфолио (можно оставить пустым)'
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        
        # Получаем все проекты
        all_projects = BlogProjectPage.objects.live().public().order_by('-date')
        
        # Фильтр по категории
        category_number = request.GET.get('category')
        if category_number:
            all_projects = all_projects.filter(category_number=category_number)
        
        # Пагинация
        paginator = Paginator(all_projects, 6)  # 6 проектов на страницу
        page_number = request.GET.get('page')
        
        try:
            projects = paginator.page(page_number)
        except PageNotAnInteger:
            projects = paginator.page(1)
        except EmptyPage:
            projects = paginator.page(paginator.num_pages)
        
        context['projects'] = projects
        context['current_category'] = category_number
        
        return context
    
    # Разрешаем добавлять только проекты (ProjectPage) как дочерние
    subpage_types = ['blog.BlogProjectPage']
    class Meta:
        verbose_name = "Страница портфолио фотостудии"
        verbose_name_plural = "Страницы портфолио фотостудии"


class BlogProjectPage(Page):
    """Детальная страница отдельного проекта (съёмки)"""
    
    # Дата съёмки
    date = models.DateField(
        "Дата съёмки",
        help_text="Дата проведения съёмки"
    )
    
    # Категория проекта (связь с категориями на главной)
    category_number = models.IntegerField(
        choices=[
            (1, 'Отели'),
            (2, 'Фасады'),
            (3, 'События'),
            (4, 'Детали'),
        ],
        default=1,
        help_text='Выберите категорию проекта'
    )
    
    # Главное изображение (для шапки проекта)
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        help_text='Главное изображение проекта (будет крупным вверху страницы)'
    )
    
    # Описание проекта под главным изображением
    mini_description = RichTextField(
        blank=True,
        help_text='Описание главного изображения'
    )
    
    # Фото для карточки проекта
    title_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        help_text='Изображение проекта на карточке в портфолио'
    )
        
    # Краткое описание (показывается на карточке в портфолио)
    short_description = models.CharField(
        max_length=200,
        blank=True,
        help_text='Краткое описание для карточки проекта'
    )
    
    # Полное описание проекта
    description = RichTextField(
        blank=True,
        help_text='Полное описание проекта'
    )
    
    # Галерея изображений (гибкий блок)
    gallery = StreamField([
        ('image', ImageChooserBlock(icon="image")),
    ], use_json_field=True, blank=True, help_text='Дополнительные фотографии проекта')
    
    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('category_number'),
        FieldPanel('title_image'),
        FieldPanel('short_description'),
        FieldPanel('main_image'),
        FieldPanel('mini_description'),
        FieldPanel('description'),
        FieldPanel('gallery'),
    ]
    
    def get_category_name(self):
        """Возвращает название категории по номеру"""
        return dict(self._meta.get_field('category_number').choices).get(self.category_number, '')
    
    # Разрешаем создавать проекты только внутри этих страниц
    parent_page_types = ['blog.BlogHomePage', 'blog.BlogPortfolioPage']
    
    # Запрещаем добавлять дочерние страницы к проекту
    subpage_types = []
    
    class Meta:
        verbose_name = "Проект в портфолио фотостудии"
        verbose_name_plural = "Проекты в портфолио фотостудии"
        ordering = ['-date']  # сортировка по дате (новые сверху)
        
# Модель для тегов (как в портфолио, но без категорий)
class BlogTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', on_delete=models.CASCADE, related_name='tagged_items')


class BlogIndexPage(Page):
    """Страница списка постов блога"""
    intro = RichTextField(blank=True, help_text="Вступительный текст")

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    # Ограничиваем: только BlogPage может быть дочерней
    subpage_types = ['blog.BlogPage']
    parent_page_types = ['blog.BlogHomePage', 'wagtailcore.Page']  # или ваша домашняя страница

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        all_posts = BlogPage.objects.child_of(self).live().order_by('-date')
        
        # Пагинация: 6 постов на страницу
        paginator = Paginator(all_posts, 6)
        page_number = request.GET.get('page')
        
        try:
            blogpages = paginator.page(page_number)
        except PageNotAnInteger:
            blogpages = paginator.page(1)
        except EmptyPage:
            blogpages = paginator.page(paginator.num_pages)
        
        context['blogpages'] = blogpages
        return context
    
    class Meta:
        verbose_name = "Страница блога для фотостудии"
        verbose_name_plural = "Страницы блога для фотостудии"


class BlogPage(Page):
    """Страница отдельного поста"""
    date = models.DateField("Дата публикации")
    intro = models.CharField(max_length=250, blank=True, help_text="Краткое описание")
    body = RichTextField(blank=True, help_text="Основной текст поста")
    
    # Теги (как в портфолио)
    tags = ClusterTaggableManager(through=BlogTag, blank=True)
    
    # Для поиска
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
    # Главнеое фото поста
    post_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        help_text='Главное изображение поста'
    )
    
    # Панели в админке
    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        FieldPanel('tags'),
        FieldPanel('post_image'),
        InlinePanel('gallery_images', label="Галерея изображений"),
    ]
    
    # Ограничиваем: только под BlogIndexPage
    parent_page_types = ['blog.BlogIndexPage']
    subpage_types = []
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Получаем галерею для этого поста
        context['gallery_images'] = self.gallery_images.all()
        return context


class BlogPageGalleryImage(Orderable):
    """Галерея изображений для поста"""
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
        related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250, help_text="Подпись к фото")

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

# ====================================================

class BlogAboutPage(Page):
    """Страница «О студии»"""
    
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        help_text='Главное изображение'
    )
    
    mini_title = models.CharField(max_length=200, default='Подзаголовок')
    
    content_blocks = StreamField([
        ('text_block', blocks.RichTextBlock(
            required=True,
            label='Текстовый блок',
        )),
    ], blank=True, use_json_field=True, verbose_name="Блоки контента")
    
    team_title = models.CharField(max_length=100, default='Команда')
    team_subtitle = models.CharField(max_length=200, default='Люди, которые создают эту красоту')
    
    team_members = StreamField([
        ('member', blocks.StructBlock([
            ('name', blocks.CharBlock(required=True, label='Имя')),
            ('position', blocks.CharBlock(required=True, label='Должность')),
            ('description', blocks.TextBlock(required=True, label='Описание')),
            ('photo', ImageChooserBlock(required=False, label='Фото')),
        ])),
    ], use_json_field=True, blank=True, verbose_name="Члены команды")
    
    footer_text = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('mini_title'),
            FieldPanel('main_image'),
            FieldPanel('content_blocks'),
        ], heading="Основной блок"),
        
        MultiFieldPanel([
            FieldPanel('team_title'),
            FieldPanel('team_subtitle'),
            FieldPanel('team_members'),
        ], heading="Команда"),
        
        MultiFieldPanel([
            FieldPanel('footer_text'),
        ], heading="Нижний текст"),
    ]
    
    class Meta:
        verbose_name = "Страница О студии"
        verbose_name_plural = "Страницы О студии"
        
class ContactPage(Page):
    """Страница Контакты"""
    
    # Короткое описание под заголовком
    intro = RichTextField(
        blank=True,
        help_text='Короткое описание под заголовком'
    )
    
    # Контактная информация
    name_and_inn = models.CharField(
        max_length=50,
        blank=True,
        default='ИП Северный свет · ИНН 1234567890',
        verbose_name='Наименование юрюлица и ИНН'
    )
    address = models.CharField(
        max_length=200,
        blank=True,
        default='Санкт-Петербург, Невский проспект, д. 10',
        verbose_name='Адрес'
    )
    
    # карта
    map_iframe = models.TextField(
        blank=True,
        verbose_name='Код карты (iframe)',
        help_text='Скопируйте готовый iframe код карты из Яндекс.Карт'
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('intro'),
        ], heading="Описание"),
        
        MultiFieldPanel([
            FieldPanel('name_and_inn'),
            FieldPanel('address'),
            FieldPanel('map_iframe'), # Поле для кода карты
        ], heading="Контактная информация и карта"),
    ]
    
    class Meta:
        verbose_name = "Страница Контакты-фотостудии"
        verbose_name_plural = "Страницы Контакты-фотостудии"