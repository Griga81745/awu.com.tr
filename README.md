Place `.env` file to root directory.

Set variables as below :
```ini
DEBUG=<1 OR 2>
SECRET_KEY=<your secret key>
```

In django shell, execute :
```python
from default import create as default_create
from test import module as test_create

default_create()
test_create()
```