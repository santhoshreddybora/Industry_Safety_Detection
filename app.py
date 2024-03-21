from Industry_Safety_Detection.logger import logging
from Industry_Safety_Detection.exception import isdException
from Industry_Safety_Detection.pipeline.training_pipeline import TrainPipeline
import sys

try:
    obj=TrainPipeline()
    obj.run_pipeline()
except Exception as e:
    logging.info(e)
    raise isdException(e,sys)
