if DEBUG:
	from .development import *
else:
	from .production import *

from .common import *