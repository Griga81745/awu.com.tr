from django.views import generic

class AboutUsView(generic.TemplateView):
	template_name = 'we/about-us.html'

class ContactUsView(generic.TemplateView):
	template_name = 'we/contact-us.html'

class FAQView(generic.TemplateView):
	template_name = 'we/faq.html'