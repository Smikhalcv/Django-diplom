from django.db import models
from django.contrib.auth.models import AbstractUser

#Create your models here.
from django.utils.text import slugify


class User(AbstractUser):
    cart = models.IntegerField() # id товаров в корзине пользователя

class Good(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True)
    type_good = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')

    users = models.ManyToManyField(
        User,
        related_name='goods',
        through='Relationship',
    )

    def __init__(self, *args, **kwargs):
        try:
            kwargs['slug'] = slugify(kwargs['name'])
        except KeyError:
            pass
        super(Good, self).__init__(*args, **kwargs)

class Score(models.Model): # счётчик звёздочек для товара
    name = models.CharField(max_length=100)
    score = models.IntegerField()
    good = models.ForeignKey(Good, on_delete=models.CASCADE)

class Relationship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)

