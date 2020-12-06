from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse

from feedback.forms import ScoreForm
from feedback.models import Score
from shop.models import Good


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
