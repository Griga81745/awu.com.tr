from django.urls import path, include

from . import views

app_name = 'messenger'

urlpatterns = [
    path('', views.ChatListView.as_view(), name='messages'),
    path('calls/', views.CallListView.as_view(), name='calls'),
    path('chat/<int:peer_id>/', views.ChatDetailView.as_view(), name='chat')
]