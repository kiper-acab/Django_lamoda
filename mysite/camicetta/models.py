from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name='Название категории')
    slug = models.SlugField(unique=True, max_length=255, verbose_name='Слаг')
    photo = models.ImageField(upload_to='photos/', verbose_name='Изоображение')
    
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Thing(models.Model):
    brand = models.CharField(null=False, max_length=255, unique=False, verbose_name='Брэнд')
    name = models.CharField(null=False, max_length=255, verbose_name='Название вещи')
    thing_slug = models.SlugField(unique=True, max_length=255, verbose_name='Слаг Вещей')
    price = models.IntegerField(null=True, unique=False, verbose_name='Цена')
    discount = models.IntegerField(default=0, null=True, verbose_name='Скидка')
    image = models.ImageField(upload_to='photos/', verbose_name='Изоображение')
    size = models.CharField(null=True, max_length=255, verbose_name='Размеры', blank=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, max_length=255)
    
    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('thing', kwargs={'thing_slug': self.thing_slug})
    
    class Meta:
        verbose_name = 'Вещь'
        verbose_name_plural = 'Вещи'
        ordering = ['id']