from . import forms

from django.views import generic
from django.shortcuts import render
from django.contrib.auth import get_user_model, login
from django.contrib.auth.hashers import make_password

from django.http.request import HttpRequest
from django.http.response import HttpResponse

User = get_user_model()


class RegisterView(generic.View):
  form_class = forms.RegisterForm
  template_name = 'users/register.html'

  def get(self, request: HttpRequest) -> HttpResponse:
    return render(request, self.template_name, {'form': self.form_class()})

  def post(self, request: HttpRequest) -> HttpResponse:
    form = self.form_class(request.POST)

    if form.is_valid():
      user = User.objects.create(
        first_name=form.cleaned_data['first_name'],
        last_name=form.cleaned_data['last_name'],
        email=form.cleaned_data['email'],
        password=make_password(form.cleaned_data['password1'])
      )
      login(request, user)
    else:
      return render(request, self.template_name, {'form': form})

    return HttpResponse('Success')
