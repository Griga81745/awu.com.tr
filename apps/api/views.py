from .models import Ticket
from django.utils.crypto import get_random_string

from rest_framework.request import Request
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
