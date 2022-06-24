from . import views
from settings.views import page_404 
from django.urls import path

app_name = 'we'

urlpatterns = [
	path('', views.AboutUsView.as_view(), name='about-us'),
	path('contact-us/', views.ContactUsView.as_view(), name='contact-us'),
	path('faq/', views.FAQView.as_view(), name='faq'),
	path('404/', page_404)
]