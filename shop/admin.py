from django.contrib import admin
from shop.models import Good, User, Article, RelationshipUser, Order, RelationshipOrder, RelationshipType, TypeGood


# from django.contrib.admin.


class RelationshipInlineType(admin.TabularInline):
    model = RelationshipType


@admin.register(TypeGood)
class TypeAdmin(admin.ModelAdmin):
    """Администрирование разделов"""
    ...


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    """Администрирование товара"""
    list_display = ('name', 'type_good_admin',)
    inlines = [
        RelationshipInlineType
    ]


class RelationshipInline(admin.TabularInline):
    model = RelationshipUser
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
    model = RelationshipOrder


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
