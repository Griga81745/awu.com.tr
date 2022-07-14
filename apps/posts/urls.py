from . import views
from django.urls import path

app_name = 'blog'
urlpatterns = [
	path('', views.PostListView.as_view(), name='posts'),
	path('post/<str:slug>', views.PostDetailView.as_view(), name='post-detail'),
]
