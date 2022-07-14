from . import models

from django.contrib import messages
from django.views import generic
from django.shortcuts import render

class PostListView(generic.ListView):
	model = models.Post
	paginate_by = 4
	queryset = models.Post.published_posts.all()
	template_name = 'posts/post-list.html'

class PostDetailView(generic.DetailView):
	model = models.Post
	queryset = models.Post.published_posts.all()
	template_name = 'posts/post-detail.html'

	def post(self,request,*args,**kwargs):
		if request.user.is_authenticated and request.POST['comment'] and len(request.POST['comment'])<200 and not request.user.comments.filter(post=self.get_object()):
			comment = models.Comment(
				user = request.user,
				post = self.get_object(),
				content = request.POST['comment']
			)
			comment.save()
			messages.success(request,message='Yorumunuz başarı ile oluşturuldu')
		else:
			messages.error(request,message='Bir yazı için sadece bir yorum yapabilirsiniz ve bu yorum 200 simbolden daha uzun olmamalıdır...')
		return super().get(self,request,*args,**kwargs)