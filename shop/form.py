from django import forms
from shop.models import Score



class ScoreForm(forms.Form):
    name = forms.CharField(max_length=50, label='Имя', widget=forms.TextInput(attrs={'cols': 20, 'placeholder':
        'Представтесь'}))
    text = forms.TimeField(label='Содержарие', widget=forms.Textarea(attrs={'rows': 3,
                                                                            'placeholder': 'Содержание',}))
    choices = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5),)
    score = forms.IntegerField(label='Оценка', widget=forms.RadioSelect(
        attrs={'id': 'value'},
        choices=choices,
    ))