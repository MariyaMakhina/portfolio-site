from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from wagtail.contrib.sitemaps.views import sitemap

from wagtail.models import Page

from wagtail.images.views.serve import ServeView

def sitemap_view(request):
    pages = Page.objects.live().public()
    return TemplateView.as_view(
        template_name='sitemap.xml',
        extra_context={'pages': pages, 'request': request},
        content_type='application/xml'
    )(request)


urlpatterns = [
    path('', include('chat_bot.urls')),
    # Используем переменные из настроек
    path(settings.DJANGO_ADMIN_URL, admin.site.urls),
    path(settings.DASHBOARD_URL, include('dashboard.urls')),
    path(settings.WAGTAIL_ADMIN_URL, include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.png', permanent=True)),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('sitemap.xml', sitemap_view),
    re_path(r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$', ServeView.as_view(), name='wagtailimages_serve'),
]

# Отдельно добавляем wagtail_urls, чтобы они были последними
urlpatterns += [
    re_path(r'', include(wagtail_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns