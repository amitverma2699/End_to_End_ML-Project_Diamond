from src.components.data_ingestion import DataIngestion
from src.logger import logging
from src.exception import Customexception
import os
import sys
import pandas as pd

obj=DataIngestion()

obj.initiate_data_ingestion()