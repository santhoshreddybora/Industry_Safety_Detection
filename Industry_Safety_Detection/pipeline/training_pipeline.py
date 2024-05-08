import sys, os
from Industry_Safety_Detection.logger import logging
from Industry_Safety_Detection.exception import isdException
from Industry_Safety_Detection.configuration.s3_operations import S3Operation
from Industry_Safety_Detection.components.data_ingestion import DataIngestion
from Industry_Safety_Detection.components.data_validation import DataValidation
from Industry_Safety_Detection.components.model_trainer import ModelTrainer
from Industry_Safety_Detection.entity.config_entity import (DataIngestionConfig,
                                                            DataValidationConfig,
                                                            ModelTrainerConfig)


from Industry_Safety_Detection.entity.artifacts_entity import (DataIngestionArtifact,
                                                               DatavalidationArtifact,
                                                               ModelTrainerArtifact)


class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config=DataValidationConfig()
        self.model_trainer_config=ModelTrainerConfig()
        self.s3_operations = S3Operation()


    
    def start_data_ingestion(self)-> DataIngestionArtifact:
        try: 
            logging.info(
                "Entered the start_data_ingestion method of TrainPipeline class"
            )
            logging.info("Getting the data from URL")

            data_ingestion = DataIngestion(
                data_ingestion_config =  self.data_ingestion_config
            )

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the data from URL")
            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )

            return data_ingestion_artifact

        except Exception as e:
            raise isdException(e, sys)
        
    def start_data_validation(self, data_ingestion_artifact)->DatavalidationArtifact:
        try:
            logging.info("Enter the start_data_validation method of trainPipeline class")
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                           data_validation_config=self.data_validation_config)
            data_validation_artifact=data_validation.initiate_data_validation()
            logging.info("Exit the start_data_validation method of trainPipeline class")
            return data_validation_artifact
        except Exception as e:
            logging.info(e)
            raise isdException(e, sys)
        
    def start_model_trainer(self)->ModelTrainerArtifact:
        try:
            logging.info("Enter the start_model_trainer method of trainPipeline class")
            model_trainer=ModelTrainer(model_trainer_config=self.model_trainer_config)
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            logging.info("Exit the start_model_trainer method of trainPipeline class")
            return model_trainer_artifact
        except Exception as e:
            logging.info(e)
            raise isdException(e, sys)

    def run_pipeline(self) -> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact)
            if data_validation_artifact.validation_status==True:     
                model_trainer_artifact=self.start_model_trainer()
            else:
                raise Exception("Your data is not in correct format")

        except Exception as e:
            raise isdException(e, sys)