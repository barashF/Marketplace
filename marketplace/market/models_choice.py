from django.db import models


class OrderStatus(models.TextChoices):
    FREE = 'Заказ находится на рассмотрении'
    ACCEPTED = 'Заказ находится в работе'
    DELIVERED = 'Заказ доставлен в постамат'
    COMPETED = 'Клиент забрал заказ'
    CANCEL = 'Заказ был отменён'