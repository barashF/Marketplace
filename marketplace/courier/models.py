from django.db import models
from django.contrib.auth.models import User


class Courier(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    rating = models.IntegerField()

    class Meta:
        verbose_name='Курьер'
        verbose_name_plural = 'Курьеры'
    
    def __str__(self) -> str:
        return f'user: {self.user.pk}, rating: {self.rating}'


class ParcelLocker(models.Model):
    address = models.CharField(max_length=200, verbose_name='Адрес')

    class Meta:
        verbose_name='Постамат'
        verbose_name_plural = 'Постаматы'
    
    def __str__(self) -> str:
        return f'id: {self.pk}, address: {self.address}'
