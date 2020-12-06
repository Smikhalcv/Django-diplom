from django import forms

from feedback.models import Score


class ScoreForm(forms.Form):
    """Форма для создания отзыва о товаре"""
    name = forms.CharField(max_length=50, label='Имя', widget=forms.TextInput(attrs={'cols': 20, 'placeholder':
        'Представтесь'}))
    review = forms.CharField(label='Содержарие', widget=forms.Textarea(attrs={'rows': 3,
                                                                              'placeholder': 'Содержание', }))
    choices = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5),)
    star = forms.IntegerField(widget=forms.RadioSelect(
        attrs={'id': 'value'},
        choices=choices,
    ))

    class Meta(object):
        model = Score
