from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import forms as base_forms

User = get_user_model()


class FormCreateUser(base_forms.UserCreationForm):
    class Meta(base_forms.UserCreationForm.Meta):
        model = User

    email = forms.EmailField(required=True)
    field_order = ['username', 'email', 'password1', 'password2']
