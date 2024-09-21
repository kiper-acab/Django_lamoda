from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse



ORDER_STATUS_CHOICES = (
                        ('Decorated', 'Оформлен'),
                        ('Wait_pay', 'Ожидает оплату'), 
                        ('Paid', 'Оплачен'), 
                        ('Confirmed', 'Подтвержден'), 
                        ('On_the_way', 'В пути'), 
                        ('Ready', 'Можете забрать на пункте выдачи')
                        )


class User(AbstractUser):
    image = models.ImageField(upload_to='photos/photo_users/', verbose_name='Фотография пользователя')
    

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
    thing_slug = models.SlugField(unique=True, max_length=255, verbose_name='Сла(г) Вещей')
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


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    size = models.CharField(max_length=25,)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'Корзина для {self.user.username} | Вещь {self.thing.name} | Размер {self.size}'
    
    class Meta:
        verbose_name = 'Корзина товаров'
        verbose_name_plural = 'Корзины товаров'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name="Заказчик")
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    delivery_type = models.CharField(max_length=40, choices=(('self','Самовывоз'),('delivery','Доставка')), default='self', verbose_name="Тип доставки")
    comments = models.TextField(blank=True)
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default='Decorated', verbose_name="Статус")
    total_cost = models.IntegerField(verbose_name="Итоговая стоимость")
    things = models.ManyToManyField(Basket)


    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ №{self.pk} | для {self.first_name}"
    


