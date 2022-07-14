from apps.posts.models import Post

post = Post(
    title='test',
    content='lorem',
    published=True
)

post.save()