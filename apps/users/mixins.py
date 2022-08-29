from typing import Tuple, Dict, List

from django.forms.widgets import NumberInput
from django.shortcuts import redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse

class AddClassNameMixin:
  '''
  Mixin to add html classes to form fields
  Usable for both Form and FilterSet(django_filters) objects
  '''
  class_name: str = 'form-control'
  class_name__checkbox: str = 'checkbox'
  not_modify_fields: List[str] = []

  def __init__(self, *args: Tuple, **kwargs: Dict):
    result = super().__init__(*args, **kwargs)
    form = self if hasattr(self,'visible_fields') else self.form

    for field in filter(lambda field: field.name not in self.not_modify_fields, form.visible_fields()):
      if getattr(field.field.widget,'input_type',None) == 'checkbox':
        field.field.widget.attrs['class'] = self.class_name__checkbox
      else:
        field.field.widget.attrs['class'] = self.class_name

    return result

class AddAttributesMixin:
  '''
  Mixin to add html attributes to form fields 
  Usable for both Form and FilterSet(django_filters) objects
  '''
  custom_attributes: Dict = {}

  def __init__(self, *args: Tuple, **kwargs: Dict):
    result = super().__init__(*args, **kwargs)
    form = self if hasattr(self,'fields') else self.form

    for field in form.visible_fields():
      if self.custom_attributes.get(field.name):
        for attr in self.custom_attributes[field.name]:
          field.field.widget.attrs[attr] = self.custom_attributes[field.name][attr] 
      

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
