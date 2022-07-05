from typing import Union
from apps.api.models import Ticket

from channels.auth import AuthMiddlewareStack
from channels.sessions import CookieMiddleware
from channels.middleware import BaseMiddleware

from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

User = get_user_model()


@database_sync_to_async
def get_user(ticket: str) -> Union[User, AnonymousUser]:

  if (ticket_object := Ticket.objects.filter(ticket=ticket)):
    user = ticket_object[0].user
    ticket_object.delete()
    return user

  return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):

  def __init__(self, app: CookieMiddleware) -> None:
    self.app = app
    return super().__init__(app)

  async def __call__(self, scope, receive, send) -> None:
    ticket = scope['path'].strip('/').split('/')[-1]
    scope['user'] = await get_user(ticket)
    return await self.app(scope, receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
