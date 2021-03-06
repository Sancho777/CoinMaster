from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    first_name = forms.CharField(label='Nome', max_length=100, required=True)
    last_name = forms.CharField(
        label='Sobrenome', max_length=100, required=True)
    email = forms.EmailField(
        max_length=250, help_text='ex.  seuemail@mail.com')

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'password1', 'password2', 'email')
