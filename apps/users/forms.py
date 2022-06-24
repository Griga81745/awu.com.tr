from typing import Dict, Any
from . import mixins as custom_mixins

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class RegisterForm(custom_mixins.AddClassNameMixin, forms.Form):
  first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
  last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
  email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
  password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'id': 'password1'}))
  password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'id': 'password2'}))

  def clean(self) -> Dict:
    cleaned_data = super().clean()

    if cleaned_data['password1'] != cleaned_data['password2']:
      raise ValidationError('Passwords do not match!')

    return cleaned_data

  def clean_email(self) -> Any:
    email = self.cleaned_data['email']

    if User.objects.filter(email=email).exists():
      raise ValidationError('This email is already taken!')

    return email


class LoginForm(custom_mixins.AddClassNameMixin, forms.Form):
  email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'id': 'email'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'id': 'password'}))
  remember_me = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
