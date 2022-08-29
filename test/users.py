from django.utils import timezone

import names
from typing import List, Union
from random import randint, choice

from . import TestModule, random_phone_number
from apps.users.models import User, Area


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
				consultacy_free = True,
				license_date = timezone.now(),
			)
			object.save()
			for i in range(3):
				object.areas.add(choice(list(Area.objects.all())))
			objects.append(object)
		return objects

	def clear(self) -> None :
		return [object.delete() for object in self.get()]

