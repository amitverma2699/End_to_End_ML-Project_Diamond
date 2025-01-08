import pandas as pd
import numpy as np
from src.logger import logging
from src.exception import Customexception
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from src.utils.utiles import save_object
from dataclasses import dataclass
from pathlib import Path
import os
import sys

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path= os.path.join("Artifacts","preprocessor.pkl")
    


class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_tranformation(self):
        try:
            logging.info("Data Transformation started")

            categorical_cols = ['cut', 'color','clarity']
            numerical_cols = ['carat', 'depth','table', 'x', 'y', 'z']
            
            # Define the custom ranking for each ordinal variable
            cut_categories = ['Fair', 'Good', 'Very Good','Premium','Ideal']
            color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            clarity_categories = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']
            
            logging.info('Pipeline Initiated')
            
            num_pipeline=Pipeline([
                ('Imputer',SimpleImputer(strategy='median')),
                ('Std_scaler',StandardScaler())
            ])

            cat_pipeline=Pipeline([

                ('Imputer',SimpleImputer(strategy='most_frequent')),
                ('OrdinalEncoder',OrdinalEncoder(categories=[cut_categories,color_categories,clarity_categories]))
                ('Std_scaler',StandardScaler())
            ])

            preprocessor=ColumnTransformer([
                ('Num_pipline',num_pipeline,numerical_cols),
                ('Cat_pipeline',cat_pipeline,categorical_cols)
            ])

            return preprocessor


        except Exception as e:
            logging.info("Error occured in Get Data Transformation")
            raise Customexception(e,sys)
        
    def initiate_data_transformation(self,train_data_path,test_data_path):
        
        try:
            train_df=pd.read_csv(train_data_path)
            test_df=pd.read_csv(test_data_path)
            logging.info("Read the Train and Test Dataset.")
            logging.info(f"Train Dataframe Head:\n {train_df.head().to_string()}")
            logging.info(f"Train Dataframe Head:\n {test_df.head().to_string()}")
            
            preprocessing_obj=self.get_data_tranformation()

            target_column='price'
            drop_columns=[target_column,'id']

            input_feature_train_df=train_df.drop(columns=drop_columns,axis=1)
            target_feature_train_df=train_df[target_column]

            input_feature_test_df=test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df=test_df[target_column]

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            logging.info("Applying preprocessing object on training and testing datasets")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )



        except Exception as e:
            logging.info("Error occured in Initiate Data Transformation")
            raise Customexception(e,sys)