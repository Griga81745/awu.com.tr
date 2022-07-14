from tokenize import Number
from . import models, forms, mixins as custom_mixins

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model, authenticate, login
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import generic
from django.urls import reverse, reverse_lazy


User = get_user_model()

class ConfirmedView(generic.TemplateView):
  template_name = 'origin/confirmed.html'

class HomeView(generic.TemplateView):
  template_name = 'users/home.html'


class SearchView(generic.ListView):
  model = models.User
  paginate_by = 9
  queryset = models.User.lawyers.all()
  template_name = 'users/search.html'


class ProfileDetailView(generic.DetailView):
  model = models.User
  queryset = models.User.lawyers.all()
  template_name = 'users/profile-detail.html'


class PasswordForgotView(generic.TemplateView):
  template_name = 'users/password-forgot.html'


class PasswordResetView(generic.TemplateView):
  template_name = 'users/password-reset.html'


class AppointmentCreateView(generic.TemplateView):
  template_name = 'users/appointment-create.html'


class ReviewCreateView(custom_mixins.ReviewFormMixin, generic.CreateView):
  model = models.Review
  fields = ('content', 'rate')
  extra_context = {'view_type':'create', 'model': models.Review}
  template_name = 'users/review-create-update.html'

  def get_success_url(self):
    return reverse('users:profile-detail',args=[self.request.path.rpartition('/')[2]])

  def form_valid(self, form,**kwargs):
    instance = form.save(commit=False)
    instance.destination = models.User.objects.get(id=self.request.path.rpartition('/')[2])
    instance.owner = self.request.user
    try:
      instance.save()
      messages.success(self.request,'Yorumunuz oluşturuldu !')
    except Exception as e:
      messages.error(self.request,e.message)
    return HttpResponseRedirect(self.get_success_url())

class ReviewUpdateView(custom_mixins.ReviewFormMixin, generic.UpdateView):
  model = models.Review
  fields = ('rate','content')
  extra_context = {'view_type':'update', 'model': models.Review}
  template_name = 'users/review-create-update.html'

  def get_success_url(self):
    messages.success(self.request,'Yorumunuz güncellendi...')
    return reverse_lazy('users:profile-detail',args=[self.get_object().destination.id])


class ReviewDeleteView(generic.DeleteView):
  model = models.Review 
  template_name = 'users/review-delete.html'
  # success_url = reverse_lazy('users:confirmed')
  def get_success_url(self):
    messages.success(self.request,'Yorumunuz silindi...')
    return reverse_lazy('users:profile-detail',args=[self.get_object().id])


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
