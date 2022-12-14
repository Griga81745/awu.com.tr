from typing import Dict, Any
from . import mixins as custom_mixins

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from apps.users.models import Area

User = get_user_model()


class RegisterForm(custom_mixins.AddClassNameMixin, forms.Form):
  first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Adınız'}))
  last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Soyadınız'}))
  email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'E-Posta'}))
  password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Parola', 'id': 'password1'}))
  password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Parola Onayla', 'id': 'password2'}))

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
  email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'E-Posta', 'id': 'email'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Parola', 'id': 'password'}))
  remember_me = forms.BooleanField(widget=forms.CheckboxInput(), required=False)

class UpdateUserForm(
  custom_mixins.AddClassNameMixin,
  custom_mixins.AddAttributesMixin,
  forms.ModelForm
):
  class_name = 'custom-input'
  class Meta:
    model = User
    fields = [
      'first_name',
      'last_name',
      'email',
      # 'phone_number',
      # 'whatsapp'
    ]
 
class UpdateLawyerForm(
  custom_mixins.AddClassNameMixin,
  custom_mixins.AddAttributesMixin,
  forms.ModelForm
):
  class_name = 'custom-input'
  custom_attributes = {
    'areas': {
      'id':'slim-select'
    }
  }

  class Meta:
    model = User
    fields = [
      'first_name',
      'last_name',
      'email',
      # 'phone_number',
      # 'whatsapp',
      'consultacy_price',
      'city', 
      'website',
      'areas',
      'consultacy_free',
      'bio',
      'avatar',
    ]
  


