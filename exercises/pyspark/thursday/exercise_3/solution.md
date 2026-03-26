# Solution

The `local[2]` is limiting the number of threads available to Spark.

The `coalesce(10)` is bottlenecking Spark in how many partitions it can use to read in the data.

The `groupByKey(numPartitions=2)` is also limiting Spark in how many partitions it can use.

There are only 2 keys in the RDD, and Spark uses a hashing algorithm to distribute the values across the partitions. Even if you have access to 40 partitions, 2 keys will only distribute to 2 partitions leading to them taking on the majority of the work. To solve this, we need to salt the keys to help Spark distribute it evenly.

```python
from pyspark import SparkContext
import random

sc = SparkContext("local[*]", "spill_test")

raw_data = sc.textFile("heavy_data.txt")

# 1. ADD SALT: Turn "KEY_A" into "KEY_A_0", "KEY_A_1", etc.
# This forces the Hash Partitioner to send them to DIFFERENT tasks.
# This assumes 40 threads are being used, but base it on how many Spark creates when reading in your text file
salted_rdd = raw_data.map(lambda x: x.split(",")).map(lambda x: (f"{x[0]}_{random.randint(0, 39)}", x[1]))

# 2. INTERMEDIATE REDUCE: Group by the salted keys
intermediate_counts = salted_rdd.groupByKey().mapValues(len)

# 3. REMOVE SALT: Turn "KEY_A_0" back into "KEY_A"
# Remember to call an action so that the transformations are applied, otherwise Spark will not do anything
final_counts = (intermediate_counts.map(lambda x: (x[0].split("_")[0], x[1])).reduceByKey(lambda a, b: a + b)).collect()

print("Check the Spark UI  for shuffle spill")
input()
sc.stop()
```