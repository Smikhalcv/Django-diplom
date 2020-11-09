from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

# Create your views here.
from shop.form import ScoreForm, FormCreateUser
from shop.models import Good, Article, Score, User, Relationship_User


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


def cart(request):
    content = {}
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    else:
        user = User.objects.get(username=request.user)
        template = 'cart.html'
        content['user'] = user

    return render(request, template, content)


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
    reviews = phone.review.all().order_by('-star')
    form = ScoreForm()
    context = {
        'phone_in_shop': phone,
        'form': form,
        'reviews': reviews[:5],
    }
    return render(request, template, context)


def feedback(request, slug):
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


def login_site(request):
    if request.method == 'POST':
        form = FormCreateUser(request.POST)
        if form.is_valid():
            pass
        return redirect('/')
    else:
        return redirect(reverse('login'))


def add_to_cart(request, slug):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    else:
        if request.method == 'POST':
            good = Good.objects.get(slug=slug)
            user = User.objects.get(username=request.user)
            if good in user.cart.all():
                relationship = Relationship_User.objects.get(good=good, user=user)
                relationship.quantity += 1
                relationship.save()
            else:
                user.cart.add(good)
    return redirect(reverse('cart'))
