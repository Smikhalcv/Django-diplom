from datetime import datetime
import random

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, get_user_model, login

# Create your views here.
from shop.form import FormCreateUser
from shop.models import Good, Article, TypeGood

COUNT_GOOD_MAIN_PAGE = 6


def main_page(request):
    """Передаёт на главную страницу 6 товаров типа,
    публикует статью с прикреплёнными товарами"""
    template = 'index.html'
    smartphones = list(Good.objects.all())
    random.shuffle(smartphones)
    gadgets = TypeGood.objects.all()
    articles = Article.objects.all().order_by('-date_make')
    content = {
        'smartphones': smartphones[:COUNT_GOOD_MAIN_PAGE],
        'articles': articles,
        'gadgets': gadgets,
    }
    return render(request, template, content)


def empty_section(request):
    template = 'empty_section.html'
    gadgets = TypeGood.objects.all()
    content = {
        'gadgets': gadgets,
    }
    return render(request, template, content)


def registration(request):
    """Создаёт инстанс пользователя при регистрации
    в случаи успешной регистрации перенаправляет на главную страницу"""
    template = 'registration.html'
    massage_password = '''
    Your password must contain at least 8 characters.
    Your password can't be a commonly used password.
    Your password can't be entirely numeric.
    '''
    form = FormCreateUser()
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = FormCreateUser(request.POST)
        email = request.POST.get('email')
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким Email уже существует.')
            return render(request, template, context)
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
                    return render(request, template, context)
            else:
                messages.error(request, massage_password)
                return render(request, template, context)
    else:
        return render(request, template, context)
