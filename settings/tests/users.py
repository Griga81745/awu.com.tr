from apps.users.models import User, Area
from django.utils import timezone
from random import randint

import names

class UsersTestModule:

	ADMIN_USER_MAIL = 'nsit2002@gmail.com'
	TEST_MAIL_PREFIX = 'test'

	def random_number(self) -> str :
		return '05' + ''.join(str(randint(0, 9)) for _ in range(9))

	def get_all_users(self) -> list :
		return list(
			User.objects.all()\
				.exclude(email=self.ADMIN_USER_MAIL)\
				.filter(email__istartswith=self.TEST_MAIL_PREFIX)
		) 

	def create_users(self,amount:int=50) -> list:
		users = list()
		for i in range(amount+1):
			user = User(
				first_name = names.get_first_name(),
				last_name = names.get_last_name(),
				email = f'test{i}@mail.com',
				phone_number = self.random_number(),
				whatsapp = self.random_number(),
				is_lawyer = True,
				free_consultacy = True,
				license_date = timezone.now(),
			)
			user.save()
			users.append(user)
		return users

	def remove_all_users(self) -> None :
		return [user.delete() for user in self.get_all_users()]

	def get_all_areas(self) -> list :
		return list(Area.objects.all())

	def create_areas(self,amount:int=10) -> list :
		areas = list()
		for i in range(amount+1):
			area = Area(
				title = names.get_first_name()
			)
			area.save()
			areas.append(area)
		return areas

	def remove_all_users(self) -> None :
		return [area.delete() for area in self.get_all_areas()]

module = UsersTestModule()

# for i in range(1,)
