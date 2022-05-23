from typing import Tuple, Dict


class AddClassNameMixin:
  class_name: str = 'form-control'

  def __init__(self, *args: Tuple, **kwargs: Dict) -> None:
    result = super().__init__(*args, **kwargs)

    for field in self.visible_fields():
      field.field.widget.attrs['class'] = 'form-control'

    return result
