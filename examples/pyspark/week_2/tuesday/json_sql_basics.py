from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# initialize the session
spark = SparkSession.builder \
        .appName("JSON_SQL_BASICS") \
        .config("spark.sql.shuffle.partitions", "5" ) \
        .getOrCreate()

df = spark.read.json("raw_data.json", multiLine=True)

df.printSchema()


# Create a dataset( fields)

structured_df = df.select(
    col("id"),
    col("info.name").alias("user_name"),
    col("info.city").alias("location")
)

# Spark SQL
# To use pure SQL, we must register the dataframe as a Temp View
structured_df.createOrReplaceTempView("v_users")

# Now we can write SQL queries
sql_results =  spark.sql("""
    SELECT location, COUNT(*) as user_count
    FROM v_users
    WHERE user_name IS NOT NULL
    GROUP BY location
    ORDER BY user_count DESC
""")

sql_results.show()

spark.stop()