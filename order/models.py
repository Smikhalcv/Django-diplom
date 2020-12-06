from django.db import models

from shop.models import Good


# Create your models here.
class Order(models.Model):
    """Модель заказов"""
    date = models.DateTimeField(auto_now_add=True)
    name_user = models.CharField(max_length=64, verbose_name='Имя заказчика')
    id_user = models.IntegerField()
    amount_goods = models.IntegerField(verbose_name='Количество товара', default=0)
    list_goods = models.ManyToManyField(
        Good,
        related_name='order',
        through='RelationshipOrder'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.name_user


class RelationshipOrder(models.Model):
    """Связь модели заказов и товаров для указание количества единиц товара"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
