from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Answer


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterFrom(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    email = forms.CharField(label='E-mail', widget=forms.EmailInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',
                  'correct',
                  'question',
                  )

    def clean_correct(self):
        correct = self.cleaned_data['correct']
        if all(correct) == 0 or all(correct) == 1:
            raise ValidationError('Все правильные ответы быть не могут, также как и все непрпавильные')
        return correct

