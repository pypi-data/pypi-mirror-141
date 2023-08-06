import os
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    # PyArrow for dtypes conversions
    .config("spark.sql.execution.arrow.pyspark.enabled", "true")

    # Jars compatible with the base-notebook image (Python 3.8.8, PySpark 3.1.1)
    .config('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.1.1,io.delta:delta-core_2.12:1.0.1')

    # Delta Lake credentials
    .config("spark.hadoop.fs.s3a.access.key", os.environ.get("DELTA_LAKE_ACCESS_KEY"))
    .config("spark.hadoop.fs.s3a.secret.key", os.environ.get("DELTA_LAKE_SECRET_ACCESS_KEY"))

    # Delta Lake setup
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.delta.logStore.class", "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore")
    .getOrCreate()
)
