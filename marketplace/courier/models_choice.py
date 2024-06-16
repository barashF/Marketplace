from django.db import models


class StatusParcelLocker(models.TextChoices):
    FREE = 'Свободен'
    BUSY = 'Занят'