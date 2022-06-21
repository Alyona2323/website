from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment
from django.utils.translation import gettext_lazy as _


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'category', 'img',)
        exclude = ("published_date", "user",)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class LoginForm(forms.Form):
    login = forms.CharField(label=_("Логін"), max_length=16, min_length=3)
    password = forms.CharField(widget=forms.PasswordInput, label=_("Пароль"), max_length=16, min_length=5)


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label=_('Імя користувача (не більше 150 символів. Тільки букви, цифри та символи @/./+/-/_.'))
    password = forms.CharField(widget=forms.PasswordInput,
                               label=_('Пароль (мінімальна допустима кількість символів - 5)'))
    password2 = forms.CharField(widget=forms.PasswordInput, label=_('Введіть пароль повторно'))
    email = forms.EmailField(widget=forms.EmailInput, label=_('Введіть електронну пошту'))

    class Meta:
        model = User
        fields = ('username', 'email', )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
