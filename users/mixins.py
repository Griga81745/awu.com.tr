from typing import Tuple, Dict

from django.shortcuts import redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse


class AddClassNameMixin:
  class_name: str = 'form-control'

  def __init__(self, *args: Tuple, **kwargs: Dict) -> None:
    result = super().__init__(*args, **kwargs)

    for field in self.visible_fields():
      field.field.widget.attrs['class'] = 'form-control'

    return result


class AlreadyLoggedInMixin:
  logged_in_regirect_url: str = None

  def get(self, request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated and self.logged_in_regirect_url:
      return redirect(self.logged_in_regirect_url)
