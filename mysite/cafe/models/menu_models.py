from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class VolumeOption(models.Model):
    """Объем товара (общая таблица объемов)"""
    name = models.CharField(max_length=50, verbose_name="Название объема")
    sort_order = models.IntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    
    panels = [
        FieldPanel('name'),
        FieldPanel('sort_order'),
        FieldPanel('is_active'),
    ]
    
    class Meta:
        verbose_name = "Объем"
        verbose_name_plural = "Объемы"
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name


@register_snippet
class MenuCategory(models.Model):
    """Категория меню"""
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Фото категории"
    )
    sort_order = models.IntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    
    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('image'),
        FieldPanel('sort_order'),
        FieldPanel('is_active'),
    ]
    
    class Meta:
        verbose_name = "Категория меню"
        verbose_name_plural = "Категории меню"
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name


@register_snippet
class MenuItem(models.Model):
    """Товар в меню"""
    category = models.ForeignKey(
        MenuCategory,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Категория"
    )
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    sort_order = models.IntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    
    panels = [
        FieldPanel('category'),
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('sort_order'),
        FieldPanel('is_active'),
    ]
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['category__sort_order', 'sort_order', 'name']
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
    def get_prices(self):
        """Получить все цены для товара"""
        return self.prices.filter(is_active=True).select_related('volume')


@register_snippet
class ItemPrice(models.Model):
    """Цена товара для конкретного объема"""
    item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name='prices',
        verbose_name="Товар"
    )
    volume = models.ForeignKey(
        VolumeOption,
        on_delete=models.CASCADE,
        related_name='prices',
        verbose_name="Объем"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    
    panels = [
        FieldPanel('item'),
        FieldPanel('volume'),
        FieldPanel('price'),
        FieldPanel('is_active'),
    ]
    
    class Meta:
        verbose_name = "Цена"
        verbose_name_plural = "Цены"
        unique_together = ['item', 'volume']
        ordering = ['-id']
    
    def __str__(self):
        return f"{self.item.name} - {self.volume.name}: {self.price} ₽"