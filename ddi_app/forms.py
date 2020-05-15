from django import forms
from django.forms.widgets import TextInput
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from .models import UserProfile

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'date_birth', 'about_user']


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Фамилия пользователя'}), max_length=30, required=False,)
    # first_name = forms.CharField(widget=TextInput(attrs={'placeholder': 'Имя пользователя'}),max_length=30, required=False,)
    # middle_name = forms.CharField(widget=TextInput(attrs={'placeholder': 'Фамилия пользователя'}),max_length=30, required=False,)
    # last_name = forms.CharField(widget=TextInput(attrs={'placeholder': 'Отчество пользователя'}),max_length=30, required=False,)

    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Пароль',
            'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Подтвердите пароль',
            'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        # fields = ('username', 'first_name', 'middle_name', 'last_name', 'password1', 'password2', )
        fields = ('username', 'password1', 'password2', )