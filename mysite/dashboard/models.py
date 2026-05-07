from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


@register_setting
class AnalyticsSettings(BaseSiteSetting):
    """Настройки аналитики"""
    yandex_metrika_id = models.CharField(
        max_length=50, 
        blank=True, 
        verbose_name="ID Яндекс.Метрики",
        help_text="Вставьте только цифровой ID (например, 12345678)"
    )
    
    panels = [
        MultiFieldPanel([
            FieldPanel('yandex_metrika_id'),
        ], heading="Яндекс.Метрика"),
    ]
    
    class Meta:
        verbose_name = "Настройки аналитики"
        verbose_name_plural = "Настройки аналитики"