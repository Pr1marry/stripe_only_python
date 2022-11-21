from django.db import models
from django.utils.translation import gettext_lazy as _


class Item(models.Model):
    class cur_ch(models.TextChoices):
        eur = 'eur', _('euros')
        usd = 'usd', _('dollars')

    currency = models.CharField(
        max_length=10,
        choices=cur_ch.choices,
        default=cur_ch.eur
    )
    name = models.CharField(
        max_length=255,
    )
    description = models.TextField()
    price = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'Товар: {self.id}, {self.name}, {self.currency}'


class Order(models.Model):
    multiply_items = models.ManyToManyField(
        Item,
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
