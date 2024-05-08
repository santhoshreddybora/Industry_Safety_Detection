import os,sys
from Industry_Safety_Detection.entity.config_entity import ModelPusherConfig
from Industry_Safety_Detection.entity.artifacts_entity import ModelpusherArtifact,ModelTrainerArtifact
from Industry_Safety_Detection.exception import isdException
from Industry_Safety_Detection.logger import logging
from Industry_Safety_Detection.configuration.s3_operations import S3Operation


class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig ,
                 model_trainer_artifact: ModelTrainerArtifact,
                 s3: S3Operation):
        try:
            self.model_pusher_config = model_pusher_config
            self.model_trainer_artifact=model_trainer_artifact
            self.s3 = s3
        except Exception as e:
            logging.info(e)
            raise isdException(e,sys)
    
    def initiate_model_pusher(self)->ModelpusherArtifact:
        """
        Method Name :   initiate_model_pusher

        Description :   This method initiates model pusher. 
        
        Output      :    Model pusher artifact 
        """
        logging.info("Entered initiate_model_pusher method of Modelpusher class")
        try:
            self.s3.upload_file(self.model_trainer_artifact.trained_model_file_path,
                                self.model_pusher_config.S3_MODEL_KEY_PATH,
                                self.model_pusher_config.MODEL_BUCKET_NAME,
                                remove=False)
            logging.info("Uploaded best model to s3 bucket")
            logging.info("Exited initiate_model_pusher method of ModelTrainer class")
            model_pusher_artifact = ModelpusherArtifact(
                bucket_name=self.model_pusher_config.MODEL_BUCKET_NAME,
                s3_model_path=self.model_pusher_config.S3_MODEL_KEY_PATH,
            )

            return model_pusher_artifact
        except Exception as e:
            logging.info(e)
            raise isdException(str(e))
        
            