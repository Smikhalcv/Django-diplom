from django.contrib import admin

from shop.models import Good, User, Article, RelationshipUser, TypeGood, RelationshipType


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


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Администрирование статье на главной странице"""
    inlines = [
        RelationshipInlineArticle
    ]
