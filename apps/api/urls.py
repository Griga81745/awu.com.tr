from . import views
from django.urls import path, include

app_name = 'api'
urlpatterns = [
  path('ticket/', views.GetTicket.as_view(), name='get_ticket')
]
