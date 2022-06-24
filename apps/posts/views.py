from django.views import generic

class PostListView(generic.TemplateView):
	template_name = 'posts/post-list.html'

class PostDetailView(generic.TemplateView):
	template_name = 'posts/post-detail.html'