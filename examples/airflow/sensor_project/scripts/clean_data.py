from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col

spark = SparkSession.builder.appName("SensorCleaning").getOrCreate()

# 1. Load the raw text
raw_path = "/opt/spark-data/raw_sensors_large.txt"
df = spark.read.text(raw_path)

# 2. Parse CSV-style text (sensor_id, temperature)
split_col = split(df['value'], ',')
df = df.withColumn('sensor_id', split_col.getItem(0)) \
       .withColumn('temp', split_col.getItem(1).cast('float'))

# 3. Cleaning Logic
BLACK_LIST = ["SN_09", "SN_13"]
cleaned_df = df.filter(
    (col("temp").isNotNull()) & 
    (~col("sensor_id").isin(BLACK_LIST)) &
    (col("sensor_id").startswith("SN_"))
)

# 4. Save as Parquet (The efficient format)
cleaned_df.write.mode("overwrite").parquet("/opt/spark-data/cleaned_sensors.parquet")
print("Cleaning Complete: Saved to cleaned_sensors.parquet")