from .models import Ticket

from apps.users.models import User

from django.utils.crypto import get_random_string

from rest_framework import status as response_status
from rest_framework.request import Request
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class GetTicket(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request: Request) -> Response:
    user = request.user

    if (ticket := Ticket.objects.filter(user=user)):
      ticket.delete()

    ticket = Ticket.objects.create(
      user=user,
      ticket=get_random_string(32)
    )

    return Response({'ticket': ticket.ticket})

class ToggleFavorite(APIView):
  '''
  View for toggling favorites

  Codes: \n
    201 - added favorite \n
    204 - deleted favorite \n
    406 - non-valid user id or limit reached \n
  '''
  permission_classes = [IsAuthenticated]

  def is_user_favorite(self, user: User) -> bool:
    return True if user in self.request.user.favorites.all() else False

  def is_user_valid(self, user: User) -> bool:
    return True if user and user.id != self.request.user.id else False

  def favorite_add(self, user: User) -> bool:
    if self.request.user.favorites.count() < User.LIMIT_FAVORITES:
      self.request.user.favorites.add(user)
      return True
    return False

  def favorite_remove(self, user: User) -> bool:
    self.request.user.favorites.remove(user)
    return True

  def get(self, request: Request, id: int) -> Response:
    target = User.lawyers.filter(id=id).first()
    status = 0
    if self.is_user_valid(target):
      if self.is_user_favorite(target):
        status = response_status.HTTP_204_NO_CONTENT if self.favorite_remove(target) else response_status.HTTP_406_NOT_ACCEPTABLE
      else:
        status = response_status.HTTP_201_CREATED if self.favorite_add(target) else response_status.HTTP_406_NOT_ACCEPTABLE
        pass
    else:
      status = response_status.HTTP_406_NOT_ACCEPTABLE
    return Response({},status=status)