from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.
from django.utils.text import slugify


class Type_Good(models.Model):
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
        Type_Good,
        related_name='goods',
        through='Relationship_Type',
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

    def view(self):
        """Выводит тип товара в админке"""
        list_view = []
        for item in Type_Good.objects.filter(goods=self).all():
            list_view.append(item)
        return list_view

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Score(models.Model):
    """Модель отзыва о товаре"""  # счётчик звёздочек для товара
    name = models.CharField(max_length=100)
    review = models.CharField(max_length=100)
    star = models.IntegerField()
    good = models.ManyToManyField(
        Good,
        related_name='review',
        through='Relationship_Score',
    )


class Article(models.Model):
    """Статья на главное странице с привязкой товара"""
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    massage = models.CharField(max_length=100, verbose_name='Сообщение')
    date_make = models.DateField(verbose_name='Дата создания')
    attached_products = models.ManyToManyField(
        Good,
        related_name='article',
        through='Relationship_Article',
    )

    def __init__(self, *args, **kwargs):
        try:
            kwargs['date_make'] = datetime.now()
        except KeyError:
            pass
        super(Article, self).__init__(*args, **kwargs)

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
        through='Relationship_User',
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'


class Relationship_User(models.Model):
    """Связь пользователя и товара для уточнения даты добавления и количества"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE, verbose_name='Корзина')
    date_add_cart = models.DateTimeField(blank=True)
    quantity = models.IntegerField(default=1)

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


class Order(models.Model):
    """Модель заказов"""
    date = models.DateTimeField()
    name_user = models.CharField(max_length=64, verbose_name='Имя заказчика')
    id_user = models.IntegerField()
    amount_goods = models.IntegerField(verbose_name='Количество товара', default=0)
    list_goods = models.ManyToManyField(
        Good,
        related_name='order',
        through='Relationship_Order'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.name_user

    def __init__(self, *args, **kwargs):
        try:
            kwargs['date'] = datetime.now()
        except KeyError:
            pass
        super(Order, self).__init__(*args, **kwargs)


class Relationship_Order(models.Model):
    """Связь модели заказов и товаров для указание количества единиц товара"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Relationship_Type(models.Model):
    type_good = models.ForeignKey(Type_Good, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
