from datetime import datetime
import random

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, get_user_model, login
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as Base_User

# Create your views here.
from shop.form import ScoreForm, FormCreateUser
from shop.models import Good, Article, Score, User, Relationship_User, Order, Relationship_Order


def main(request):
    """Передаёт на главную страницу 6 товаров типа телефон,
    публикует статью с прикреплёнными товарами"""
    template = 'index.html'
    smartphones = list(Good.objects.all())
    random.shuffle(smartphones)
    articles = Article.objects.all().order_by('-date_make')
    content = {
        'smartphones': smartphones[:6],
        'articles': articles,
    }
    return render(request, template, content)


def cart(request):
    """Сортирует товары в корзине по дате добавления,
    дата обновлется если если увличивать количество штук товара в другом представлении"""
    content = {}
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    else:
        user = User.objects.get(username=request.user).relationship_user_set.all().order_by('-date_add_cart')
        template = 'cart.html'
        content['goods_in_cart'] = user

    return render(request, template, content)


def smartphones(request):
    """Отображает все товары типа телефон"""
    template = 'smartphones.html'
    smartphones = list(Good.objects.filter(type_good='smartphone').all())
    paginator = Paginator(smartphones, 20)
    page = request.GET.get('page')
    list_smartphones = paginator.get_page(page)
    content = {
        'smartphones': list_smartphones
    }
    return render(request, template, context=content)


def empty_section(request):
    template = 'empty_section.html'
    return render(request, template)


def phone(request, slug):
    """Выводит телефон и его описание, 5 самых лучших отзывов"""
    template = 'phone.html'
    phone = Good.objects.get(slug=slug)
    reviews = phone.review.all().order_by('-star')
    form = ScoreForm()
    context = {
        'phone_in_shop': phone,
        'form': form,
        'reviews': reviews[:5],
    }
    return render(request, template, context)


def feedback(request, slug):
    """Промежуточное представление, которое создаёт инстанс модели
    отзыва в БД из пост запроса и перенаправляет на страницу телефона"""
    product = get_object_or_404(Good, slug=slug)
    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            review = Score.objects.create(
                name=cleaned_data['name'],
                review=cleaned_data['review'],
                star=cleaned_data['star']
            )
            product.review.add(review)

    return redirect(reverse('phone', args=[slug]))


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
                relationship = Relationship_User.objects.get(good=good, user=user)
                relationship.quantity += 1
                relationship.date_add_cart = datetime.now()
                relationship.save()
            else:
                user.cart.add(good)
    return redirect(reverse('cart'))

def registration(request):
    template = 'registration.html'
    if request.method == 'POST':
        form = FormCreateUser(request.POST)
        email = request.POST.get('email')
        User = get_user_model()
        if User.objects.filter(email=email).exists():

            messages.error(request, 'Пользователь с таким Email уже существует.')
            return redirect(reverse('registration'))
        else:
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                email = form.cleaned_data['email']
                if password == form.cleaned_data['password2']:
                    User.objects.create_user(username=username, password=password, email=email)
                    user = authenticate(username=username, password=password, email=email)
                    login(request, user)
                    messages.success(request, 'Вы успешно зарегистрировались!')
                    return redirect(reverse('main'))
                else:
                    messages.error(request, 'Пароли не совпадают.')
                    return redirect(reverse('registration'))
            else:
                messages.error(request, 'Не корректные данные.')
                return redirect(reverse('registration'))
    else:
        form = FormCreateUser()
        context = {
            'form': form,
        }
        return render(request, template, context)


def order(request, id):
    user = User.objects.get(id=id)
    order = Order.objects.create(name_user=user.username, id_user=user.id)
    for good in user.cart.all():
        rel = Relationship_Order.objects.create(
            good=good,
            order=order,
            quantity=Relationship_User.objects.get(good=good, user=user).quantity
        )


    return redirect(reverse('main'))
