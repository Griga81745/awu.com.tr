from typing import Tuple, Dict

from django.forms.widgets import NumberInput
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

class ReviewFormMixin:
  def get_form(self, form_class=None):
    form = self.get_form_class()(**self.get_form_kwargs())
    form.fields['content'].widget.attrs.update({
      'class':'form-control',
      'style': 'height: 180px', 
      'oninput': '(value=>document.getElementById("textareaCount").innerHTML=value.length)(this.value)'
    })
    form.fields['rate'].widget = NumberInput(attrs={'type':'range'})
    form.fields['rate'].widget.attrs.update({
      'min':'0',
      'max':'5',
      'step':'1',
      'value':'0',
      'data-orientation':'horizontal',
      'id':'food_quality'
    })
    return form
