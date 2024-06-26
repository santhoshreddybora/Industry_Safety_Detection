from Industry_Safety_Detection.entity.artifacts_entity import ModelTrainerArtifact
from Industry_Safety_Detection.entity.config_entity import ModelTrainerConfig
import os,sys
import yaml
from Industry_Safety_Detection.utils.main_utils import read_yaml_file
from six.moves import urllib
from Industry_Safety_Detection.exception import isdException
from Industry_Safety_Detection.logger import logging
from Industry_Safety_Detection.constant.training_pipeline import *

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig):
        self.model_trainer_config = model_trainer_config
    

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")
        try:
            logging.info("Unzipping data")
            os.system(f"unzip {DATA_INGESTION_S3_DATA_NAME}")
            os.system(f"rm {DATA_INGESTION_S3_DATA_NAME}")

            #prepare image path in text file

            train_img_path=os.path.join(os.getcwd(),"images","train")
            val_img_path=os.path.join(os.getcwd(),"images","val")

            #trianing images
            with open('train.txt','a+') as f:
                img_list=os.listdir(train_img_path)
                for img in img_list:
                    f.write(os.path.join(train_img_path,img)+'\n')
                print("Done Training images" )
            #validation images
            with open('val.txt','a+') as f:
                img_list=os.listdir(val_img_path)
                for img in img_list:
                    f.write(os.path.join(val_img_path,img)+'\n')
                print("Done Testing images" ) 
            

            #download coco starting checkpoint
            url=self.model_trainer_config.weight_name
            file_name=os.path.basename(url)
            urllib.request.urlretrieve(url,os.path.join("yolov7-1",file_name))

            #training
            logging.info("started training")
            os.system(f"cd yolov7-1 & python train.py --batch {self.model_trainer_config.batch_size} --cfg cfg/training/custom_yolov7.yaml --epochs {self.model_trainer_config.no_epochs} --data data/custom.yaml --weights 'yolov7.pt'")
            logging.info("finished training")
            os.system(f"cp yolov7-1/runs/train/exp/weights/best.pt yolov7-1/")
            logging.info("copy best.pt to yolov7-1 folder")
            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
            logging.info("created a directory for storing best.pt")
            os.system(f"cp yolov7-1/runs/train/exp/weights/best.pt {self.model_trainer_config.model_trainer_dir}/")
            logging.info("copied best.pt to created folder")
            os.system("rm -rf yolov7-1/runs")
            os.system("rm -rf images")
            os.system("rm -rf labels")
            os.system("rm -rf classes.names")
            os.system("rm -rf train.txt")
            os.system("rm -rf val.txt")
            os.system("rm -rf train.cache")
            os.system("rm -rf val.cache")
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path="yolov7-1/best.pt",
            )

            logging.info("Exited initiate_model_trainer method of ModelTrainer class")
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact
    
        except Exception as e:
            logging.info(e)
            raise isdException(e, sys)