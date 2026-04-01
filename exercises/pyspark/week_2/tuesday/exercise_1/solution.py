from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("Exercise1") \
    .config("spark.sql.shuffle.partitions", "2") \
    .getOrCreate()

# Load and Flatten
df = spark.read.json("user_profiles.json", multiLine=True)

flat_df = df.select(
    col("user_id"),
    col("details.city").alias("city"),
    col("details.tier").alias("tier")
)

# SQL Approach
flat_df.createOrReplaceTempView("v_profiles")

results = spark.sql("""
    SELECT city, COUNT(*) as user_count
    FROM v_profiles
    GROUP BY city
    ORDER BY user_count DESC
""")

results.show()