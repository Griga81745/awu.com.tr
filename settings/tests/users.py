from django.utils import timezone

import names
from typing import List, Union
from random import randint, choice
from taggit.models import Tag

from . import TestModule, random_phone_number
from apps.users.models import User


class TagsTestModule(TestModule):
	
	def get(self) -> List[Tag] :
		return list(Tag.objects.all())

	def create(self,count:int=100) -> List[Tag] :
		objects = list()
		for i in range(count+1):
			object = Tag(
				name = names.get_first_name()+f'{i}'
			)
			object.save()
			objects.append(object)
		return objects

	def clear(self) -> None :
		return [object.delete() for object in self.get()]


class UsersTestModule(TestModule):

	ADMIN_USER_MAIL = 'nsit2002@gmail.com'
	TEST_MAIL_PREFIX = 'test'

	def get(self) -> List[User] :
		return list(
			User.objects.all()\
				.exclude(email=self.ADMIN_USER_MAIL)\
				.filter(email__istartswith=self.TEST_MAIL_PREFIX)
		) 

	def create(self,amount:int=50) -> List[User] :
		objects = list()
		for i in range(amount+1):
			object = User(
				first_name = names.get_first_name(),
				last_name = names.get_last_name(),
				email = f'test{i}@mail.com',
				phone_number = random_phone_number(),
				whatsapp = random_phone_number(),
				is_lawyer = True,
				free_consultacy = True,
				license_date = timezone.now(),
			)
			object.save()
			for i in range(3):
				object.tags.add(choice(list(Tag.objects.all())))
			objects.append(object)
		return objects

	def clear(self) -> None :
		return [object.delete() for object in self.get()]


users_module = UsersTestModule()
tags_module = TagsTestModule()