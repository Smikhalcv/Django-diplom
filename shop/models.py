from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils.timezone import timezone

#Create your models here.
from django.utils.text import slugify


class User(AbstractUser):
    pass

class Score(models.Model): # счётчик звёздочек для товара
    name = models.CharField(max_length=100)
    review = models.CharField(max_length=100)
    score = models.IntegerField()

class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    massage = models.CharField(max_length=100, verbose_name='Сообщение')

class Good(models.Model):
    name = models.CharField(verbose_name='Название', max_length=50)
    slug = models.SlugField(blank=True)
    type_good = models.CharField(verbose_name='Тип товара', max_length=50)
    description = models.TextField(null=True, blank=True)
    view_main = models.BooleanField(null=True, blank=True, unique=True)
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    article = models.ManyToManyField(
        Article,
        related_name='attached_products',
        through='Relationship_Article',
    )
    review = models.ManyToManyField(
        Score,
        related_name='good',
        through='Relationship_Score',
    )
    users = models.ManyToManyField(
        User,
        related_name='cart',
        through='Relationship_User',
    )

    def __init__(self, *args, **kwargs):
        try:
            kwargs['slug'] = slugify(kwargs['name'])
        except KeyError:
            pass
        super(Good, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.name

class Relationship_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE, verbose_name='Корзина')
    date_add_cart = models.DateTimeField(blank=True)

    def __init__(self, *args, **kwargs):
        try:
            kwargs['date_add_cart'] = datetime.now()
        except KeyError:
            pass
        super(Relationship_User, self).__init__(*args, **kwargs)

class Relationship_Score(models.Model):
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)

class Relationship_Article(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)