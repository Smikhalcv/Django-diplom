from django.contrib import admin
from shop.models import Good, User, Article, Relationship_User, Order, Relationship_Order


# from django.contrib.admin.

# Register your models here.
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     pass

@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    """Администрирование товара"""
    list_display = ('name', 'type_good',)


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
    ordering = ('date',)
    inlines = [
        RelationshipInlineOrder
    ]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Администрирование статье на главной странице"""
    inlines = [
        RelationshipInlineArticle
    ]


# @admin.register(Relationship_User)
# class Relationship_UserAdmin(admin.ModelAdmin):
#     pass
