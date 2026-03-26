from pyspark import SparkContext, SparkConf

# Configuration
# We are purposely setting the  partitions to be low  (2)fora large dataset toforce a spill

conf = SparkConf() \
        .setAppName("Spill_debug_demo") \
        .set("spark.sql.shuffle.partitions", "200") \
        .set("spark.executor.memory", "4g")

sc = SparkContext("local[*]", conf = conf)

large_rdd = sc.parallelize(range(100000000), 10) \
                .map(lambda x: (x % 2, x)) # Only 2 keys (0 and 1)


# wide transformation
# groupByKey forces all 10M records into just 2 partitions (one per key)
# This will likely exceecd the small 1gb executor memory
spilled_rdd = large_rdd.groupByKey().mapValues(len)

result = spilled_rdd.collect()

input()

sc.stop()