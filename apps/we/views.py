from django.views import generic

from . import models 

class AboutUsView(generic.TemplateView):
	template_name = 'we/about-us.html'

class ContactUsView(generic.TemplateView):
	template_name = 'we/contact-us.html'

class FAQView(generic.ListView):
	model = models.FAQ
	template_name = 'we/faq.html'
