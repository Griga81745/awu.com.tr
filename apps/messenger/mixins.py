import orjson
from typing import Union, Dict


class JsonParser:
  ''' Миксин, чтобы декодировать входящие / выходящие сообщения через orjson
      У channels была ошибка для JsonWebsocketConsumer, когда отправляешь
      не JSON, исключение вылетает из кода и всё ломает, пришлось писать свой try / except '''

  error_decode_message: str = None or "Can't decode JSON"  # Можно переписать текст ошибки у родителя (consumers.py)

  def encode_json(self, json: Dict) -> Union[str, None]:

    try:
      result = orjson.dumps(json).decode()
    except orjson.JSONEncodeError:
      return self.validation_error()

    return result

  def decode_json(self, raw_data: str) -> Union[Dict, None]:

    try:
      result = orjson.loads(raw_data.encode())
    except orjson.JSONDecodeError:
      return self.validation_error()

    return result

  def validation_error(self) -> None:
    ''' На случай, если прилетел не JSON '''
    self.send_json({'status': 'error', 'message': self.error_decode_message})
