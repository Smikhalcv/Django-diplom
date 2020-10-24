from django.contrib import admin
from shop.models import Good, User
#from django.contrib.admin.

# Register your models here.
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     pass

@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'type_good',)

class RelationshipInline(admin.TabularInline):
    model = Good.users.through

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [
        RelationshipInline
    ]