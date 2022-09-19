from tokenize import Number
import django_filters
from django_filters.views import FilterView

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse, reverse_lazy

from . import models, forms, mixins as custom_mixins

User = get_user_model()

class ConfirmedView(generic.TemplateView):
  template_name = 'origin/confirmed.html'


class HomeView(generic.TemplateView):
  extra_context = {
    'lawyers': User.lawyers.all()[:9]
  }
  template_name = 'users/home.html'


class LinksView(generic.TemplateView):
  extra_context = {
    'cities': [],
    'areas' : models.Area.objects.all()
  }
  template_name = 'users/links.html'


class SearchView(FilterView):
  model = models.User
  paginate_by = 9
  queryset = models.User.lawyers.all()
  filterset_fields = [
    'areas',
    'consultacy_free',  
    'city'
  ]
  template_name = 'users/search.html'

  def get_context_data(self,*args,**kwargs):
    context = super().get_context_data(*args,**kwargs)
    context.update({'filter_params':self.filter_params})
    return context

  def get_filterset(self,filterset_class):
    kwargs = self.get_filterset_kwargs(filterset_class)

    class ModifiedFilterSet(
      custom_mixins.AddAttributesMixin,
      custom_mixins.AddClassNameMixin,
      filterset_class
    ):
      rate__gte = django_filters.NumberFilter(label='En az değerlendirme',field_name='rate', lookup_expr='gte')
      consultacy_price__gte = django_filters.NumberFilter(label='En az danışma fiyatı',field_name='consultacy_price', lookup_expr='gte')
      consultacy_price__lte = django_filters.NumberFilter(label='En fazla danışma fiyatı',field_name='consultacy_price', lookup_expr='lte')
      custom_attributes = {
        'areas': {
          'id':'slim-select'
        },
        'consultacy_price':{
          'min': 0
        }
      } 
      not_modify_fields = [
        'areas'
      ]
      

    return ModifiedFilterSet(**kwargs)

  @property
  def filter_params(self):
    params = self.request.GET
    print(list(params.lists()))
    return '&'.join([ 
      f'{item[0]}={item[1]}' for item 
      in filter(lambda item: item[0]!='page',self.request.GET.lists()) 
    ])


class ProfileDetailView(generic.DetailView):
  model = models.User
  queryset = models.User.lawyers.all()
  template_name = 'users/profile-detail.html'


class PasswordForgotView(generic.TemplateView):
  template_name = 'users/password-forgot.html'


class PasswordResetView(generic.TemplateView):
  template_name = 'users/password-reset.html'


class AppointmentCreateView(LoginRequiredMixin, generic.TemplateView):
  template_name = 'users/appointment-create.html'


class ReviewCreateView(LoginRequiredMixin, custom_mixins.ReviewFormMixin, generic.CreateView):
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


class ReviewUpdateView(LoginRequiredMixin,custom_mixins.ReviewFormMixin, generic.UpdateView):
  model = models.Review
  fields = ('rate','content')
  extra_context = {'view_type':'update', 'model': models.Review}
  template_name = 'users/review-create-update.html'

  def get_success_url(self):
    messages.success(self.request,'Yorumunuz güncellendi...')
    return reverse_lazy('users:profile-detail',args=[self.get_object().destination.id])


class ReviewDeleteView(LoginRequiredMixin, generic.DeleteView):
  model = models.Review 
  template_name = 'users/review-delete.html'
  # success_url = reverse_lazy('users:confirmed')
  def get_success_url(self):
    messages.success(self.request,'Yorumunuz silindi...')
    return reverse_lazy('users:profile-detail',args=[self.get_object().id])


class ProfileEditView(LoginRequiredMixin, generic.UpdateView):
  model = User
  # form_class = forms.UpdateLawyerForm
  template_name = 'users/profile-edit.html'
  success_url = reverse_lazy('users:profile-edit')
  def get_object(self):
    return self.request.user
  def get_form_class(self):
    return forms.UpdateLawyerForm if self.request.user.is_lawyer else forms.UpdateUserForm 


class FavoritesView(LoginRequiredMixin, generic.ListView):
  model = User
  template_name = 'users/favorites.html'

  def get_queryset(self, *args, **kwargs):
    return self.request.user.favorites.all()


class RegisterView(custom_mixins.AlreadyLoggedInMixin, generic.View):
  form_class = forms.RegisterForm
  template_name = 'users/register.html'
  logged_in_regirect_url = reverse_lazy('users:home')

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

    return redirect('users:home')


class LoginView(custom_mixins.AlreadyLoggedInMixin, generic.View):
  form_class = forms.LoginForm
  template_name = 'users/login.html'
  logged_in_regirect_url = reverse_lazy('users:home')

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

    return redirect('users:home')
