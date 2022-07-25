from abc import ABC, abstractmethod
from typing import Union, List
from random import randint

from django.db.models import Model


def random_phone_number():
	return '05' + ''.join(str(randint(0, 9)) for _ in range(9))


class TestModule(ABC):

    @abstractmethod
    def get(self) -> list :
        pass

    @abstractmethod
    def create(self) -> list :
        pass

    @abstractmethod
    def clear(self) -> list :
        pass


from .users import UsersTestModule, TagsTestModule
from .posts import PostsTestModule


class SuperTestModule(TestModule):

    modules = (
        # TagsTestModule(),
        UsersTestModule(),
        PostsTestModule() 
    )

    def get(self) -> List[List[Model]] :
        return [ module.get() for module in self.modules ]

    def create(self) -> List[List[Model]] :
        return [ module.create() for module in self.modules ]
        
    def clear(self) -> List[List[Model]] :
        return [ module.clear() for module in self.modules ]


module = SuperTestModule()