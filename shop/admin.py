from django.contrib import admin
from shop.models import Good, User, Article, Relationship_User, Order, Relationship_Order, Relationship_Type, Type_Good


# from django.contrib.admin.


class RelationshipInlineType(admin.TabularInline):
    model = Relationship_Type


@admin.register(Type_Good)
class TypeAdmin(admin.ModelAdmin):
    """Администрирование разделов"""


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    """Администрирование товара"""
    list_display = ('name', 'view',)
    inlines = [
        RelationshipInlineType
    ]


class RelationshipInline(admin.TabularInline):
    model = Relationship_User
    ordering = ('date_add_cart',)


class RelationshipInlineArticle(admin.TabularInline):
    model = Good.article.through


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Администрирование пользователя"""
    inlines = [
        RelationshipInline
    ]


class RelationshipInlineOrder(admin.TabularInline):
    model = Relationship_Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Администрирование заказов"""
    ordering = ('-date',)
    list_display = ('name_user', 'amount_goods',)
    inlines = [
        RelationshipInlineOrder
    ]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Администрирование статье на главной странице"""
    inlines = [
        RelationshipInlineArticle
    ]
