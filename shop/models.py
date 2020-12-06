from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


# Create your models here.


class TypeGood(models.Model):
    view = models.CharField(max_length=50, verbose_name='Тип товара')

    def __str__(self):
        return self.view

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'


class Good(models.Model):
    """Модель товара"""
    name = models.CharField(verbose_name='Название', max_length=50)
    slug = models.SlugField(blank=True)
    type_good = models.ManyToManyField(
        TypeGood,
        related_name='goods',
        through='RelationshipType',
    )
    description = models.TextField(null=True, blank=True)
    view_main = models.BooleanField(null=True, blank=True, unique=True)
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')

    def __init__(self, *args, **kwargs):
        try:
            kwargs['slug'] = slugify(kwargs['name'])
        except KeyError:
            pass
        super(Good, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.name

    def type_good_admin(self):
        """Выводит тип товара в админке"""
        list_view = []
        for item in TypeGood.objects.filter(goods=self).all():
            list_view.append(item)
        return list_view

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Article(models.Model):
    """Статья на главное странице с привязкой товара"""
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    massage = models.CharField(max_length=100, verbose_name='Сообщение')
    date_make = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    attached_products = models.ManyToManyField(
        Good,
        related_name='article',
        through='RelationshipArticle',
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья главной страницы'
        verbose_name_plural = 'Статья главной страницы'


class User(AbstractUser):
    """Пользователь"""
    cart = models.ManyToManyField(
        Good,
        related_name='users',
        through='RelationshipUser',
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'


class RelationshipUser(models.Model):
    """Связь пользователя и товара для уточнения даты добавления и количества"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE, verbose_name='Корзина')
    date_add_cart = models.DateTimeField(blank=True, auto_now_add=True)
    quantity = models.IntegerField(default=1)


class RelationshipArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)


class RelationshipType(models.Model):
    type_good = models.ForeignKey(TypeGood, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
