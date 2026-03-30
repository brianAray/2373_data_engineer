from pyspark.sql import SparkSession
import pyspark.sql.functions as F

spark = SparkSession.builder.appName("SensorAnalysis").getOrCreate()

# 1. Load the Cleaned Parquet
df = spark.read.parquet("/opt/spark-data/cleaned_sensors.parquet")

# 2. Aggregation Logic
summary_df = df.groupby("sensor_id").agg(
    F.avg("temp").alias("avg_temp"),
    F.max("temp").alias("max_temp"),
    F.min("temp").alias("min_temp"),
    F.count("temp").alias("reading_count")
).orderBy("avg_temp", ascending=False)

# 3. Save Summary for Streamlit
summary_df.write.mode("overwrite").parquet("/opt/spark-data/sensor_summary.parquet")
print("Analysis Complete: Summary generated.")