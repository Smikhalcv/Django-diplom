from django.db import models

# Create your models here.
from shop.models import Good


class Score(models.Model):
    """Модель отзыва о товаре"""  # счётчик звёздочек для товара
    STAR_CHOICES = [
        (5, '★★★★★'),
        (4, '★★★★'),
        (3, '★★★'),
        (2, '★★'),
        (1, '★'),
    ]
    name = models.CharField(max_length=100)
    review = models.CharField(max_length=100)
    star = models.IntegerField(choices=STAR_CHOICES)
    good = models.ManyToManyField(
        Good,
        related_name='review',
        through='RelationshipScore',
    )


class RelationshipScore(models.Model):
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
