from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast, col

spark = SparkSession.builder.appName("JoinOptimization").getOrCreate()

# Load in the massive dataset
big_sales_df = spark.read.parquet("data/huge_sales.parquet")

#  Load in the small dataset
small_stores_df = spark.read.json("data/stores.json",  multiLine=True)

# 1. Standard Join (Inner)
# Spark will perform a 'SortMergeJoin' (Standard Shuffle)
standard_join = big_sales_df.join(small_stores_df, "store_id", "inner")

standard_join.show(10)

# Broadcast  Join
optimized_join = big_sales_df.join(broadcast(small_stores_df), "store_id")

optimized_join.show(10)

# Other Join Types
# Left Anti: Show me sales for stores that are not in my store listed
# Great for finding data errors and orphaned records
error_df = big_sales_df.join(small_stores_df, "store_id", "left_anti")

error_df.show(10)

# Joining on multiple keys / different names
# If column names are different
# final_df = big_sales_df.join(
#     small_stores_df,
#     big_sales_df.store_id ==  small_stores_df.id,
#     "left"
# ).drop(small_stores_df.id) # drop the redundant column

final_df.show(5)


spark.stop()