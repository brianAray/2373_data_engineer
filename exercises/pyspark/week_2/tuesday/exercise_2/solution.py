from pyspark.sql import SparkSession
from pyspark.sql.functions import col, broadcast, when

spark = SparkSession.builder.appName("Exercise2").getOrCreate()

# Load Data
sales_df = spark.read.parquet("sales_data.parquet")
profiles_df = spark.read.json("user_profiles.json", multiLine=True) \
    .select(col("user_id"), col("details.tier").alias("tier"))

tiers_df = spark.read.json("tier_metadata.json")

# 1. Inner Join
inner_df = sales_df.join(profiles_df, "user_id", "inner")
print("Inner Join Sample:")
inner_df.show(5)

# 2. Left Anti Join (Finding Orphans)
orphans_df = sales_df.join(profiles_df, "user_id", "left_anti")
print("Unique Orphaned IDs:")
orphans_df.select("user_id").distinct().show()

# 3. Broadcast Join with Calculation
# We join on tier == tier_name
final_df = inner_df.join(
    broadcast(tiers_df), 
    inner_df.tier == tiers_df.tier_name, 
    "left"
)

# 4. Final Calculation
final_df = final_df.withColumn(
    "final_price",
    when(col("discount").isNotNull(), col("price") * (1 - col("discount")))
    .otherwise(col("price"))
)

print("Final Discounted Sales:")
final_df.select("user_id", "tier", "price", "final_price").show(10)

spark.stop()