from . import forms, mixins as custom_mixins

from django.views import generic
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model, authenticate, login

from django.http.request import HttpRequest
from django.http.response import HttpResponse

User = get_user_model()

class HomeView(generic.TemplateView):
  template_name = 'users/home.html'

class SearchView(generic.TemplateView):
  template_name = 'users/search.html'

class PasswordForgotView(generic.TemplateView):
  template_name = 'users/password-forgot.html'

class PasswordResetView(generic.TemplateView):
  template_name = 'users/password-reset.html'

class ProfileDetailView(generic.TemplateView):
  template_name = 'users/profile-detail.html'

class AppointmentCreateView(generic.TemplateView):
  template_name = 'users/appointment-create.html'

class ReviewCreateView(generic.TemplateView):
  template_name = 'users/review-create.html'

class ProfileEditView(generic.TemplateView):
  template_name = 'users/profile-edit.html'

class ProfilePasswordEditView(generic.TemplateView):
  template_name = 'users/profile-password-edit.html'


class RegisterView(custom_mixins.AlreadyLoggedInMixin, generic.View):
  form_class = forms.RegisterForm
  template_name = 'users/register.html'
  logged_in_regirect_url = None

  def get(self, request: HttpRequest) -> HttpResponse:
    if (result := super().get(request)):
      return result

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


class LoginView(custom_mixins.AlreadyLoggedInMixin, generic.View):
  form_class = forms.LoginForm
  template_name = 'users/login.html'
  logged_in_regirect_url = None

  def get(self, request: HttpRequest) -> HttpResponse:
    if (result := super().get(request)):
      return result

    return render(request, self.template_name, {'form': self.form_class()})

  def post(self, request: HttpRequest) -> HttpResponse:
    form = self.form_class(request.POST)

    if form.is_valid():

      if not (user := authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])):
        form.add_error(field='email', error='Incorrect Email or Password')
        return render(request, self.template_name, {'form': form})

      login(request, user)

      if not form.cleaned_data['remember_me']:
        request.session.set_expiry(0)

    else:
      return render(request, self.template_name, {'form': form})

    return HttpResponse('Success')
