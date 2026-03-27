from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql.functions import col, avg, count, when, round

# Entry point
# SparkSession is the modern entry point for Spark (Replacing SparkContext)
# It combines SQL, Dataframes and data assets into one interface
spark = SparkSession.builder \
    .appName("dataframe_basics") \
    .getOrCreate()

# Define the schema
sensor_schema = StructType([
    StructField("sensor_id", StringType(), True),
    StructField("temperature", DoubleType(), True)
])

# Data loading
# RDDs: You manually parse strings
# DataFrames: You use spark.read, and it automatically handles headers if its there
# You can also infer datatypes and build a schema off of it, but this is an issue with large
# datasets
df = spark.read.csv("raw_sensors_large.txt", header=False, schema=sensor_schema, mode="PERMISSIVE") \
    .toDF("sensor_id", "temperature")

# Dataframe transformations
# Unlike RDDs, these operations are optimized by the Catalyst Optimizer
# It reorders filters and selects to reduce the amount of data processed
# ~ acts as a logical NOT operator for Spark
cleaned_df = df.filter(
    (col("temperature").isNotNull()) &
    (~col("temperature").isNaN()) &
    (~col("sensor_id").isin(["SN_09", "SN_13"]))
)

cleaned_df.show(10)

# Adding a column
# withColumn is a way to transform without writing complex maps

status_df = cleaned_df.withColumn(
    "temp_status",
    when(col("temperature") > 30, "Hot").otherwise("Normal")
)

status_df.show(10)

# Aggregate functions
# This is where Dataframes really are the best
# Spark uses something called "Tungsten" which is essentially (off-heap memory) to make these aggregations
# This is significantly faster than manual RDD reduceByKey

sensor_stats = status_df.groupBy("sensor_id").agg(
    round(avg("temperature"), 2).alias("avg_temp"),
    count("temperature").alias("reading_count")
)

# Action
# .show() to trigger the DF
sensor_stats.sort("avg_temp", ascending=False).show(10)

# Data Saving
# Writing to parquet, the industry standard
# It is compressed and fast
sensor_stats.write.mode("overwrite").parquet("output/sensor_stats.parquet")

spark.stop()