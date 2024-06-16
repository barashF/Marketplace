from django.db import models


class OrderStatus(models.TextChoices):
    FREE = 'Заказ находится на рассмотрении'
    ACCEPTED = 'Заказ находится в работе'
    DELIVERED = 'Заказ доставлен в постамат'
    COMPETED = 'Клиент забрал заказ'
    CANCEL = 'Заказ был отменён'


class ProductCategory(models.TextChoices):
    ELECTRONICS = 'Электроника и бытовая техника'
    CLOTH = 'Одежда и аксессуары'
    INTERIOR = 'Товары для дома и интерьера'
