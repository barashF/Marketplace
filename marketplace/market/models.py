from django.db import models
from django.contrib.auth.models import User

from courier.models import Courier, ParcelLocker
from .models_choice import OrderStatus


class Market(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название магазина')
    description = models.TextField(verbose_name='Название описание')
    admin = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Администратор')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
    
    def __str__(self) -> str:
        return f'id: {self.pk}, title: {self.title}'


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название товара')
    description = models.TextField(verbose_name='Описание')
    market = models.ForeignKey(Market, on_delete=models.PROTECT, 
                               verbose_name='Магазин', related_name='products')
    category = models.CharField(max_length=150, verbose_name='Категория товара')
    price = models.FloatField(verbose_name='Цена')
    storage = models.PositiveIntegerField(verbose_name='Количество в наличии')
    image = models.FileField(upload_to='products/')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
    
    def __str__(self) -> str:
        return f'id: {self.pk}, title: {self.title}'


class ImageProduct(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.PROTECT)
    image = models.FileField(upload_to='products/')


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, 
                             related_name='basket', verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
    
    def __str__(self) -> str:
        return f'user: {self.user.pk}, product: {self.product}'
    

class Order(models.Model):
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders',
                                                            verbose_name='Заказчик')
    parcel_locker = models.ForeignKey(ParcelLocker, related_name='orders', 
                                      on_delete=models.PROTECT, verbose_name='Постамат')
    status = models.CharField(max_length=150, choices=OrderStatus.choices, 
                              default=OrderStatus.FREE, verbose_name='Статус заказа')
    courier = models.ForeignKey(Courier, on_delete=models.PROTECT, related_name='orders', 
                                                        verbose_name='Курьер', blank=True)
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    
    def __str__(self) -> str:
        return f'id: {self.pk}, постамат: {self.parcel_locker.pk}, status: {self.status}'


