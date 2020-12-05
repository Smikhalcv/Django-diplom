from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.


from shop.models import Good, User, RelationshipUser, TypeGood


def add_to_cart(request, slug):
    """Промежуточное представление, создаёт инстанс связи между товаром и пользователем
    Если товар добавлен ещё раз обновляется дата добавления и увеличивается количествоединиц товара
    Если пользователь не авторизован, его перекинет на страницу авторизации"""
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    else:
        if request.method == 'POST':
            good = Good.objects.get(slug=slug)
            user = User.objects.get(username=request.user)
            if good in user.cart.all():
                relationship = RelationshipUser.objects.get(good=good, user=user)
                relationship.quantity += 1
                relationship.date_add_cart = datetime.now()
                relationship.save()
            else:
                user.cart.add(good)
    return redirect(reverse('main'))


def cart(request):
    """Сортирует товары в корзине по дате добавления,
    дата обновлется если увеличивать количество штук товара в другом представлении"""
    gadgets = TypeGood.objects.all()
    content = {
        'gadgets': gadgets,
    }
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    else:
        user = User.objects.get(username=request.user)
        template = 'cart.html'
        content['goods_in_cart'] = user.relationshipuser_set.all().order_by('-date_add_cart')
    parametr = request.GET.get('parametr')
    item = request.GET.get('item')
    if parametr and item:
        good = RelationshipUser.objects.get(user=user, good=Good.objects.get(slug=item))
        if parametr == 'plus':
            good.quantity += 1
            good.save()
        elif parametr == 'minus':
            if good.quantity == 1:
                good.delete()
            else:
                good.quantity -= 1
                good.save()
        elif parametr == 'delete':
            good.delete()

    return render(request, template, content)
