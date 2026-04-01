from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, expr

spark = SparkSession.builder \
    .appName("TransformationsMaster") \
    .getOrCreate()

# 1  Load  in the data
df = spark.read.csv("data/users_active.csv", header=True, inferSchema=True)

selected_df = df.selectExpr("user_id", "upper(name) as name_upper", "status")

# 2 Adding & Removing Columns
#  withColumn cana dd a constant or a calculation
enhanced_df = selected_df.withColumn("platform", lit("Web")) \
                        .withColumn("is_active", col("status") == "Active")

# Removing a column
final_df = enhanced_df.drop("status")

# Filtering
filtered_df = final_df.filter("user_id > 1").where(col("name_upper") != "BOB")

# Set Operations
df_new = spark.read.csv("data/users_new.csv", header=True, inferSchema=True)

# unionByName is safer than union() because it matches column names
# Even if they are in a different order in the CSV
combined_users  =  df.unionByName(df_new, allowMissingColumns=True)



# Caching
combined_users.cache()

combined_users.show()  # Actions trigger caching


# Sorting & partitioning (Disk  Optimization)
logs_df = spark.read.parquet("data/logs.parquet")

# Repartitioning in memory: repartition (shuffle) vs coalesce (No shuffle)

# Use repartition to increase parallelism, coalesce to decrease it before saving
fast_logs = logs_df.repartition(5, "user_id")

# Saving with partitioning (Logical folders)
# Best for columns used in WHERE clauses like year
fast_logs.write.mode("overwrite").partitionBy("year").parquet("data/logs_partitioned")

# Saving with bucketing (fixed hash files)
# MUST save as a table to use bucketing effectively
fast_logs.write.mode("overwrite").bucketBy(10, "user_id").sortBy("log_id").saveAsTable("bucketed_logs")

combined_users.unpersist()
spark.stop()