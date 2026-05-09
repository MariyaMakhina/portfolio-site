from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from home.models import PortfolioBlogPostPage, PortfolioBlogIndexPage, ProjectPage, ProjectsListPage
from django.utils import timezone
from datetime import timedelta
import json


@staff_member_required
def dashboard_view(request):
    """Главная страница дашборда"""
    
    # Получаем ID страницы блога
    blog_page = PortfolioBlogIndexPage.objects.first()
    blog_page_id = blog_page.id if blog_page else None
    
    # Получаем ID Яндекс.Метрики
    yandex_metrika_id = None
    try:
        from dashboard.models import AnalyticsSettings
        analytics_settings = AnalyticsSettings.for_request(request)
        yandex_metrika_id = analytics_settings.yandex_metrika_id
    except:
        pass
    
    # === СТАТИСТИКА ПРОЕКТОВ ===
    all_projects = ProjectPage.objects.all()
    total_projects = all_projects.count()
    
    # Опубликованные (live=True)
    published_projects = all_projects.filter(live=True).count()
    
    # В работе (live=True, но не готовы)
    in_work_projects = all_projects.filter(live=True, is_ready=False).count()
    
    # Черновики (не опубликованы)
    draft_projects = all_projects.filter(live=False).count()
    
    # Список проектов в работе (для выпадающего списка)
    in_work_projects_list = all_projects.filter(live=True, is_ready=False).order_by('-first_published_at')
    
    # Список черновиков
    draft_projects_list = all_projects.filter(live=False).order_by('-first_published_at')
    
    # === СТАТИСТИКА СТАТЕЙ ===
    all_posts = PortfolioBlogPostPage.objects.all()
    total_blog_posts = all_posts.count()
    published_blog_posts = all_posts.filter(live=True).count()
    draft_blog_posts = total_blog_posts - published_blog_posts
    
    # Черновики статей
    draft_posts_list = all_posts.filter(live=False).order_by('-first_published_at')
    
    # === ГРАФИК ===
    today = timezone.now().date()
    publications = []
    labels = []
    
    for i in range(6, 0, -1):
        month_start = today.replace(day=1) - timedelta(days=(i-1)*30)
        month_start = month_start.replace(day=1)
        
        count = PortfolioBlogPostPage.objects.filter(
            date__year=month_start.year,
            date__month=month_start.month
        ).count()
        
        publications.append(count)
        labels.append(month_start.strftime('%b %Y'))
    
    chart_data = {
        'labels': labels,
        'values': publications,
    }
    
    # === РОДИТЕЛЬСКАЯ СТРАНИЦА ДЛЯ ПРОЕКТОВ ===
    projects_parent = ProjectsListPage.objects.first()
    projects_parent_id = projects_parent.id if projects_parent else None
    
    # === СОЗДАЁМ КОНТЕКСТ ===
    context = {
        'total_blog_posts': total_blog_posts,
        'published_blog_posts': published_blog_posts,
        'draft_blog_posts': draft_blog_posts,
        'draft_posts_list': draft_posts_list,
        'total_projects': total_projects,
        'published_projects': published_projects,
        'in_work_projects': in_work_projects,
        'draft_projects': draft_projects,
        'in_work_projects_list': in_work_projects_list,
        'draft_projects_list': draft_projects_list,
        'blog_page_id': blog_page_id,
        'projects_parent_id': projects_parent_id,
        'yandex_metrika_id': yandex_metrika_id,
        'chart_data_json': json.dumps(chart_data),
    }
    
    return render(request, 'dashboard/index.html', context)