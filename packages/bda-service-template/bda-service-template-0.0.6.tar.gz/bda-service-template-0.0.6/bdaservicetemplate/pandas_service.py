from .spark_service import SparkService
import os
import glob
import pandas as pd

class PandasService(SparkService):
    def __init__(self):
        super().__init__()

    def get_dataset(self):
        spark_df = super().get_dataset()

        # Save dataset to tmp file and read it using pandas
        path = "/tmp/spark_input_dataset"
        spark_df.repartition(1).write.format("com.databricks.spark.csv").option("header", "false").save(path)
        os.chdir(path)
        result = glob.glob('*.{}'.format("csv"))
        return pd.read_csv(result[0])


    def save_dataset(self, dataset):
        super().save_dataset(self.spark.createDataFrame(dataset))
