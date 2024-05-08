from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    data_zip_file_path:str
    feature_store_path:str

@dataclass
class DatavalidationArtifact:
    validation_status:str


@dataclass
class ModelTrainerArtifact:
    trained_model_file_path:str


@dataclass
class ModelpusherArtifact:
    bucket_name:str
    s3_model_path:str

