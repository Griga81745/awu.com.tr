from . import views
from django.urls import path, include

app_name = 'api'
urlpatterns = [
  path('toggle-favorite/<int:id>', views.ToggleFavorite.as_view(), name='toggle-favorite'),
]
