from . import views
from django.urls import path

app_name = 'users'
urlpatterns = [
  path('', views.HomeView.as_view(), name='home'),
  path('search/', views.SearchView.as_view(), name='search'),
  path('password-forgot/', views.PasswordForgotView.as_view(), name='password-forgot'),
  path('password-reset/', views.PasswordResetView.as_view(), name='password-reset'),
  path('profile/', views.ProfileDetailView.as_view(), name='profile-detail'),
  path('book-appointment/', views.AppointmentCreateView.as_view(), name='appointment-create'),
  path('leave-review/', views.ReviewCreateView.as_view(), name='review-create'),
  path('account/', views.ProfileEditView.as_view(), name='profile-edit'),
  path('register/', views.RegisterView.as_view(), name='register'),
  path('login/', views.LoginView.as_view(), name='login')
]
