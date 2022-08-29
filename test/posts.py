import names
from typing import List
from django.utils.lorem_ipsum import paragraph

from . import TestModule
from apps.posts.models import Post
from apps.users.models import Area
from random import choice

class PostsTestModule(TestModule):

    def get(self) -> List[Post] :
        return list(Post.objects.all())

    def create(self,count:int=10) -> List[Post] :
        objects = list()
        for i in range(count+1):
            object = Post(
                title = f'{names.get_first_name()} {names.get_last_name()}',
                content = paragraph(),
                published = True
            )
            object.save()
            for i in range(3):
                object.tags.add(choice(list(Area.objects.all())))
            objects.append(object)
        return objects

    def clear(self) -> List[Post] :
        return [object.delete() for object in self.get()]


module = PostsTestModule()