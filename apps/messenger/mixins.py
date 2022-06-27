import orjson
from typing import Union, Dict


class JsonParser:
  error_decode_message: str = None or "Can't decode JSON"

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
    self.send_json({'status': 'error', 'message': self.error_decode_message})
