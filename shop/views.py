from django.shortcuts import render

# Create your views here.
from shop.models import Good


def main(request):
    template = 'index.html'
    return render(request, template)

def login(request):
    template = 'login.html'
    return render(request, template)

def cart(request):
    template = 'cart.html'
    return render(request, template)

def smartphones(request):
    template = 'smartphones.html'
    smartphones = Good.objects.all()
    content = {
        'smartphones': smartphones
    }
    return render(request, template, context=content)

def empty_section(request):
    template = 'empty_section.html'
    return render(request, template)

def phone(request):
    template = 'phone.html'
    phone = Good.objects.get(id=1)
    context = {
        'phone_in_shop': phone
    }
    return render(request, template, context)