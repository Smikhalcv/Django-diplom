from django.contrib import admin

# Register your models here.
from order.models import Order, RelationshipOrder


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
