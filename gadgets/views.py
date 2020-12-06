from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

# Create your views here.
from feedback.forms import ScoreForm
from shop.models import TypeGood, Good

COUNT_GADGETS_GADGET_PAGE = 20
COUNT_REVIEW_ABOUT_GOOD = 5


def gadgets(request, id):
    """Отображает все товары указанного типа"""
    template = 'smartphones.html'
    gadgets = TypeGood.objects.all()
    type_gadget = get_object_or_404(TypeGood, id=id)
    smartphones = list(type_gadget.goods.all())
    paginator = Paginator(smartphones, COUNT_GADGETS_GADGET_PAGE)
    page = request.GET.get('page')
    list_smartphones = paginator.get_page(page)
    content = {
        'smartphones': list_smartphones,
        'gadgets': gadgets,
    }
    return render(request, template, content)


def phone(request, slug):
    """Выводит телефон и его описание, 5 самых лучших отзывов"""
    template = 'phone.html'
    gadgets = TypeGood.objects.all()
    phone = Good.objects.get(slug=slug)
    reviews = phone.review.all().order_by('-star')
    form = ScoreForm()
    context = {
        'phone_in_shop': phone,
        'form': form,
        'reviews': reviews[:COUNT_REVIEW_ABOUT_GOOD],
        'gadgets': gadgets,
    }
    return render(request, template, context)
