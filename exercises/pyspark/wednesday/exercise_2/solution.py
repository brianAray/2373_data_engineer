from pyspark import SparkContext
import os
import shutil

sc = SparkContext.getOrCreate()

# 1. LOAD: Read the expanded transactions.txt
raw_data = sc.textFile("transactions.txt")

# 2. TRANSFORM (Narrow): Create (Key, Value) pairs
# We split the string "Category,Price" into a tuple ("Category", float(Price))
pairs = raw_data.map(lambda line: (line.split(",")[0], float(line.split(",")[1])))

# 3. SHUFFLE (Wide Transformation): reduceByKey
# This is where the magic (and the heavy lifting) happens. 
# Spark sums values locally first (Map-side combine) then shuffles 
# the data to get the final total per category.
category_totals = pairs.reduceByKey(lambda x, y: x + y)

# 4. REPARTITION (Wide Transformation): Force 2 output files
# This ensures that no matter how many workers we have, we end up 
# with exactly two part-files in our output folder.
final_rdd = category_totals.repartition(2)

# 5. ACTION: Save to a directory
output_dir = "category_totals_output"
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

final_rdd.saveAsTextFile(output_dir)

sc.stop()