from src.pipelines.prediction_pipeline import CustomData

obj=CustomData(0.7,61.2,57.0,5.69,5.73,3.5,'Ideal','G','VS1')
print(obj.get_data_as_dataframe())
