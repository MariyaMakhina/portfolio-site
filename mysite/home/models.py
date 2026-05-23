from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from django.conf import settings

from wagtailmedia.edit_handlers import MediaChooserPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from .blocks import (
    HeroBlock, SelectedProjectsBlock, TemplateBlock, TemplatesBlock,
    EducationItemBlock, SkillItemBlock, EducationSkillsBlock,
    ContactFormBlock, BlogSectionBlock, ButtonUpBlock, SocialLinksBlock,
    TabsBlock, ContentWithIconBlock, ClearFloatBlock,
)
from .blocks import CarouselBlock 


# ============ Блог портфолио ============
class PortfolioBlogIndexPage(Page):
    intro = RichTextField(blank=True)
    posts_per_page = models.IntegerField(default=6, verbose_name="Статей на страницу")
    
    content_panels = Page.content_panels + [FieldPanel('intro')]
    
    def get_context(self, request):
        context = super().get_context(request)
        all_posts = PortfolioBlogPostPage.objects.live().public().order_by('-date')
        paginator = Paginator(all_posts, self.posts_per_page)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            posts = paginator.page(1)
        context['blog_posts'] = posts
        return context
    
    class Meta:
        verbose_name = "Блог портфолио (список статей)"
        verbose_name_plural = "Блоги портфолио (списки статей)"


class PortfolioBlogPostPage(Page):
    date = models.DateField(default=timezone.now)
    intro = models.CharField(max_length=250, blank=True)
    body = RichTextField(blank=True)
    image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    
    search_fields = Page.search_fields + [
        index.SearchField('title', partial_match=True, boost=10),
        index.SearchField('intro', partial_match=True, boost=5),
        index.SearchField('body', partial_match=True),
        index.FilterField('slug'), 
    ]
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([FieldPanel('date'), FieldPanel('intro'), FieldPanel('image')], heading="Информация о статье"),
        FieldPanel('body'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        blog_page = PortfolioBlogIndexPage.objects.live().first()
        context['blog_page_url'] = blog_page.url if blog_page else '/blog/'
        return context
    
    class Meta:
        verbose_name = "Статья блога портфолио"
        verbose_name_plural = "Статьи блога портфолио"


# ============ Главная страница ============
class HomePage(Page):
    """Главная страница портфолио"""
    
    # ЕДИНЫЙ STREAMFIELD ДЛЯ ВСЕХ СЕКЦИЙ
    page_sections = StreamField(
        [
            ('hero', HeroBlock()),
            ('selected_projects', SelectedProjectsBlock()),
            ('templates', TemplatesBlock()),
            ('education_skills', EducationSkillsBlock()),
            ('contact_form', ContactFormBlock()),
            ('blog', BlogSectionBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Секции страницы",
        help_text="Добавляйте, удаляйте и меняйте порядок секций перетаскиванием"
    )
    
    # Глобальные настройки
    from_address = models.EmailField(max_length=255, blank=True, default='noreply@portfolio.com', verbose_name="Email отправителя")
    to_address = models.EmailField(max_length=255, blank=True, verbose_name="Email получателя")
    subject = models.CharField(max_length=255, blank=True, default="Новое сообщение с портфолио", verbose_name="Тема письма")
    show_button_up = models.BooleanField(default=True, verbose_name="Показывать кнопку наверх")
    
    content_panels = Page.content_panels + [
        FieldPanel('page_sections'),
        MultiFieldPanel([
            FieldPanel('from_address'),
            FieldPanel('to_address'),
            FieldPanel('subject'),
        ], heading="Настройки email", classname="collapsible collapsed"),
        MultiFieldPanel([
            FieldPanel('show_button_up'),
        ], heading="Кнопка наверх", classname="collapsible collapsed"),
    ]
    
    class Meta:
        verbose_name = "Главная страница"
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        # Для блога (нужно для blog_section_block)
        latest_posts = PortfolioBlogPostPage.objects.live().public().order_by('-date')[:3]
        context['latest_posts'] = latest_posts
        
        blog_page = PortfolioBlogIndexPage.objects.live().first()
        context['blog_page_url'] = blog_page.url if blog_page else '/blog/'
        
        return context
    
    def save_message_to_file(self, data):
        messages_dir = os.path.join(settings.BASE_DIR, 'messages')
        os.makedirs(messages_dir, exist_ok=True)
        
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'message_{timestamp}.txt'
        filepath = os.path.join(messages_dir, filename)
        
        content = f"""
========================================
        НОВОЕ СООБЩЕНИЕ
========================================

Дата: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
Страница: {self.title}
URL: {self.full_url}

---------------------------------------------------
        КОНТАКТНАЯ ИНФОРМАЦИЯ
---------------------------------------------------
Имя: {data.get('name', 'Не указано')}
Телефон или Email: {data.get('email_or_phone', 'Не указано')}

---------------------------------------------------
        СООБЩЕНИЕ
---------------------------------------------------
{data.get('message', 'Нет текста')}

========================================
        КОНЕЦ СООБЩЕНИЯ
========================================
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def send_email(self, data):
        if not self.to_address:
            return False
        
        email_content = f"""
Новое сообщение с сайта портфолио!

---------------------------------------------------
Отправитель:
Имя: {data.get('name', 'Не указано')}
Телефон или Email: {data.get('email_or_phone', 'Не указано')}

Сообщение:
{data.get('message', 'Нет текста')}
---------------------------------------------------

Страница: {self.title}
URL: {self.full_url if self.full_url else 'Локальная разработка'}
"""
        
        try:
            send_mail(
                subject=self.subject,
                message=email_content,
                from_email=self.from_address,
                recipient_list=[self.to_address],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Ошибка отправки email: {e}")
            return False
    
    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            name = request.POST.get('name', '').strip()
            email_or_phone = request.POST.get('email_or_phone', '').strip()
            message = request.POST.get('message', '').strip()
            
            errors = []
            if not name:
                errors.append('Имя обязательно')
            if not email_or_phone:
                errors.append('Телефон или Email обязателен')
            if not message:
                errors.append('Сообщение обязательно')
            
            if errors:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'Ошибка валидации', 'errors': errors}, status=400)
                else:
                    context = self.get_context(request)
                    context['form_errors'] = errors
                    context['form_data'] = request.POST
                    return super().serve(request, *args, **kwargs)
            
            try:
                filepath = self.save_message_to_file({
                    'name': name,
                    'email_or_phone': email_or_phone,
                    'message': message
                })
                email_sent = self.send_email({
                    'name': name,
                    'email_or_phone': email_or_phone,
                    'message': message
                })
                
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': 'Сообщение успешно отправлено', 'email_sent': email_sent, 'file_saved': filepath})
                
                context = self.get_context(request)
                context['form_success'] = True
                return super().serve(request, *args, **kwargs)
                
            except Exception as e:
                error_msg = f'Ошибка при сохранении: {str(e)}'
                print(error_msg)
                
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': error_msg}, status=500)
                
                context = self.get_context(request)
                context['form_errors'] = [error_msg]
                return super().serve(request, *args, **kwargs)
        
        return super().serve(request, *args, **kwargs)


# ============ Настройки соцсетей ============
@register_setting
class SocialMediaSettings(BaseSiteSetting):
    show_in_header = models.BooleanField(default=True, verbose_name="Показывать в шапке")
    show_in_footer = models.BooleanField(default=True, verbose_name="Показывать в подвале")
    
    phone = models.CharField(max_length=50, blank=True, verbose_name="Телефон")
    whatsapp = models.CharField(max_length=50, blank=True, verbose_name="WhatsApp")
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn")
    telegram_url = models.URLField(blank=True, verbose_name="Telegram")
    instagram_url = models.URLField(blank=True, verbose_name="Instagram")
    vk_url = models.URLField(blank=True, verbose_name="VK")
    mail = models.EmailField(max_length=100, blank=True, verbose_name="Email")
    github_url = models.URLField(blank=True, verbose_name="GitHub")
    mastodon_url = models.URLField(blank=True, verbose_name="Mastodon")
    max_url = models.URLField(blank=True, verbose_name="MAX")
    
    panels = [
        MultiFieldPanel([
            FieldPanel('show_in_header'),
            FieldPanel('show_in_footer'),
        ], heading="Управление отображением"),
        MultiFieldPanel([
            FieldPanel('phone'),
            FieldPanel('whatsapp'),
            FieldPanel('mail'),
        ], heading="Контакты"),
        MultiFieldPanel([
            FieldPanel('linkedin_url'),
            FieldPanel('telegram_url'),
            FieldPanel('instagram_url'),
            FieldPanel('vk_url'),
            FieldPanel('github_url'),
            FieldPanel('mastodon_url'),
            FieldPanel('max_url'),
        ], heading="Социальные сети"),
    ]
    
    class Meta:
        verbose_name = "Настройки соцсетей"


class ProjectRequest(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email", blank=True)
    phone = models.CharField(max_length=50, blank=True, verbose_name="Телефон")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_processed = models.BooleanField(default=False, verbose_name="Обработано")
    
    def __str__(self):
        return f"{self.name} - {self.created_at}"
    
    class Meta:
        verbose_name = "Заявка на проект"
        verbose_name_plural = "Заявки на проекты"

# ============== Список проектов =================

class ProjectsListPage(Page):
    intro = RichTextField(blank=True, help_text="Краткое вступление")
    posts_per_page = models.IntegerField(default=6, verbose_name="Проектов на страницу")
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('posts_per_page'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        
        if request.user.is_authenticated and request.user.is_superuser:
            # Администратор видит все проекты
            all_projects = ProjectPage.objects.all().order_by('-completion_date', '-pk')
        else:
            # Обычные пользователи видят НИЧЕГО (только администратор видит проекты)
            all_projects = ProjectPage.objects.none()
        
        paginator = Paginator(all_projects, self.posts_per_page)
        page = request.GET.get('page')
        
        try:
            projects = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            projects = paginator.page(1)
        
        context['projects'] = projects
        return context
    
    class Meta:
        verbose_name = "Страница проектов веб-портфолио"
        verbose_name_plural = "Страницы проектов веб-портфолио"

# ============ Проект (страница) ============
class ProjectContentBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, help_text="Заголовок блока")
    description = blocks.RichTextBlock(required=False, help_text="Описание")
    image = ImageChooserBlock(required=False, help_text="Изображение")
    
    class Meta:
        icon = 'media'
        label = 'Блок контента'
        template = 'blocks/project_content_block.html'


class ProjectPage(Page):
    card_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name="Фото для карточки", help_text="Если не выбрано, будет использоваться основное фото проекта")
    intro = models.CharField(max_length=250, blank=True, verbose_name="Краткое описание")
    content = StreamField([('content_block', ProjectContentBlock()), ('tabs_block', TabsBlock()), ('carousel_block', CarouselBlock()), ('content_with_icon', ContentWithIconBlock()), ('clear_float', ClearFloatBlock()),], blank=True, use_json_field=True, verbose_name="Контент проекта")
    image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    video = models.ForeignKey('wagtailmedia.Media', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', limit_choices_to={'type': 'video'})
    technologies = models.CharField(max_length=500, blank=True, verbose_name="Технологии")
    completion_date = models.DateField(null=True, blank=True, verbose_name="Дата завершения")
    link_page = models.ForeignKey('wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    external_link = models.URLField(blank=True, verbose_name="Внешняя ссылка")
    github_link = models.URLField(
        blank=True,
        verbose_name="Ссылка на GitHub",
        help_text="Ссылка на репозиторий проекта"
    )
    
    search_fields = Page.search_fields + [
        index.SearchField('title', partial_match=True, boost=10),
        index.SearchField('intro', partial_match=True, boost=5),
        index.SearchField('technologies', partial_match=True),
        index.FilterField('slug'), 
    ]
    
    is_ready = models.BooleanField(
        default=False,
        verbose_name="Проект готов",
        help_text="Отметьте, если проект полностью готов к показу"
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([FieldPanel('card_image'), FieldPanel('intro'), FieldPanel('image'), MediaChooserPanel('video', media_type='video')], heading="Основная информация"),
        MultiFieldPanel([FieldPanel('technologies'), FieldPanel('completion_date')], heading="Детали"),
        MultiFieldPanel([FieldPanel('is_ready')], heading="Статус проекта"),
        MultiFieldPanel([FieldPanel('link_page'), FieldPanel('external_link'), FieldPanel('github_link')], heading="Ссылка"),
        FieldPanel('content'),
    ]
    
    def get_link_url(self):
        if self.link_page:
            return self.link_page.url
        return self.external_link
    
    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        
        
# ============= Поиск ============
class SearchPage(Page):
    """Страница поиска по сайту"""
    intro = RichTextField(blank=True, help_text="Текст над формой поиска")
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
    
    def get_template(self, request):
        return 'search/search_page.html'  # путь к шаблону
    
    def get_context(self, request):
        context = super().get_context(request)
        query = request.GET.get('query', '')
        results = []
        
        if query:
            from home.models import PortfolioBlogPostPage
            
            if request.user.is_authenticated and request.user.is_superuser:
                from home.models import ProjectPage
                projects = ProjectPage.objects.all().search(query)
                articles = PortfolioBlogPostPage.objects.live().public().search(query)
                results = list(projects) + list(articles)
            else:
                # Обычный пользователь видит только статьи блога
                results = PortfolioBlogPostPage.objects.live().public().search(query)
        
        # Пагинация
        paginator = Paginator(results, 10)
        page_number = request.GET.get('page')
        
        try:
            page_results = paginator.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            page_results = paginator.page(1)
        
        context['query'] = query
        context['results'] = page_results
        
        blog_page = PortfolioBlogIndexPage.objects.live().first()
        context['blog_page_url'] = blog_page.url if blog_page else '/'
        
        return context
    
    class Meta:
        verbose_name = "Страница поиска веб-портфолио"
        verbose_name_plural = "Страницы поиска веб-портфолио"