from Industry_Safety_Detection.logger import logging
from Industry_Safety_Detection.exception import isdException
import sys

try:
    c=1/0
except Exception as e:
    logging.info(e)
    raise isdException(e,sys)
