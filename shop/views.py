from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

# Create your views here.
from shop.form import ScoreForm
from shop.models import Good, Article


def main(request):
    template = 'index.html'
    smartphones = Good.objects.filter(type_good='phone').all()
    article = Article.objects.last()
    goods = article.attached_products.all()
    content = {
        'smartphones': smartphones,
        'article': article,
        'goods': goods,
    }
    return render(request, template, content)

def login(request):
    template = 'login.html'
    return render(request, template)

def cart(request):
    template = 'cart.html'
    return render(request, template)

def smartphones(request):
    template = 'smartphones.html'
    smartphones = Good.objects.filter(type_good='phone').all()
    content = {
        'smartphones': smartphones
    }
    return render(request, template, context=content)

def empty_section(request):
    template = 'empty_section.html'
    return render(request, template)

def phone(request, slug):
    template = 'phone.html'
    phone = Good.objects.get(slug=slug)
    form = ScoreForm().as_p()
    #form_score = form.score
    context = {
        'phone_in_shop': phone,
        'form': form,
        #'form_score': form_score,
    }
    return render(request, template, context)

def feedback(request, slug):
    product = get_object_or_404(Good, slug=slug)

    return redirect(reverse('phones', args=[slug]))
#     #return redirect(reverse('game', args=[int(f'{game.id}')]))