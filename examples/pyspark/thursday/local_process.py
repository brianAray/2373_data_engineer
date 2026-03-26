from pyspark import SparkConf, SparkContext
import os

# Driver class configuration
conf = SparkConf() \
    .setAppName("local_testing") \
    .set("spark.sql.shuffle.partitions", 4) # keep partitions for local dev

sc = SparkContext(conf=conf)

# Internal executors when we are working with threads
#Each thread acts as a worker

data = [1, 2, 3, 4, 5, 6, 7, 8]
rdd = sc.parallelize(data, numSlices=4) # Distribute the data into 4 chunks (tasks)

squared_rdd = rdd.map(lambda x: x*x)

results = squared_rdd.collect()

print(f"local execution results: {results}")

sc.stop()