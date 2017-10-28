import logging
from enum import Enum

logger = logging.getLogger('glacibot')

class Logging(Enum):
	INFO = 1
	WARNING = 2
	ERROR = 3