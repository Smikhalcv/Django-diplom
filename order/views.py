from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.
from django.urls import reverse

from shop.models import User, Order, RelationshipUser, RelationshipOrder


def order(request, id):
    """Создаёт заказ из корзины и очищает её"""
    user = User.objects.get(id=id)
    order = Order.objects.create(name_user=user.username, id_user=user.id)
    list_goods = user.cart.all()
    for good in list_goods:
        rel_user = RelationshipUser.objects.get(good=good, user=user)
        rel = RelationshipOrder.objects.create(
            good=good,
            order=order,
            quantity=rel_user.quantity
        )
        order.amount_goods += rel_user.quantity
        rel_user.delete()
    order.save()
    messages.success(request, 'Заказ оформлен!')
    return redirect(reverse('main'))