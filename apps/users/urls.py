from . import views
from django.urls import path

app_name = 'users'

urlpatterns = [
  path('', views.HomeView.as_view(), name='home'),
  path('confirmed/',views.ConfirmedView.as_view(), name='confirmed'),
  path('search/', views.SearchView.as_view(), name='search'),
  path('profile/<int:pk>', views.ProfileDetailView.as_view(), name='profile-detail'),
  path('password-forgot/', views.PasswordForgotView.as_view(), name='password-forgot'),
  path('password-reset/', views.PasswordResetView.as_view(), name='password-reset'),
  path('book-appointment/', views.AppointmentCreateView.as_view(), name='appointment-create'),
  path('leave-review/<int:id>', views.ReviewCreateView.as_view(), name='review-create'),
  path('delete-review/<int:pk>', views.ReviewDeleteView.as_view(), name='review-delete'),
  path('update-review/<int:pk>', views.ReviewUpdateView.as_view(), name='review-update'),
  path('account/', views.ProfileEditView.as_view(), name='profile-edit'),
  path('register/', views.RegisterView.as_view(), name='register'),
  path('login/', views.LoginView.as_view(), name='login'),
  path('logout/', views.logout_view, name='logout')
]
