from pyspark import SparkContext, SparkConf
import time
import math

# DRIVER CLASS CONFIGURATION
conf = SparkConf().setAppName("Large_Sensor_Analysis")
sc = SparkContext("local[*]", conf=conf)

# SHARED VARIABLES
blacklist = sc.broadcast({"SN_09", "SN_13"})
error_counter = sc.accumulator(0)

# DATA LOADING (RDD)
# minPartitions=4 ensures the large file is split immediately
raw_rdd = sc.textFile("raw_sensors_large.txt", minPartitions=4)

def process_sensor(line):
    try:
        parts = line.split(",")
        if len(parts) != 2: raise ValueError
        return (parts[0], float(parts[1]))
    except:
        error_counter.add(1)
        return None

# TRANSFORMATIONS (Lazy)
# Note: mapValues keeps the keys partitioned, making the shuffle more efficient
results_rdd = (raw_rdd
               .map(process_sensor)
               .filter(lambda x: x is not None and x[0] not in blacklist.value and not math.isnan(x[1]))
               .mapValues(lambda x: (x, 1))
               .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))
               .mapValues(lambda x: round(x[0] / x[1], 2)))

# ACTION (Triggering the work)
start_time = time.time()
final_results = results_rdd.collect()
end_time = time.time()

# OUTPUT
print(f"PROCESSED IN: {end_time - start_time:.2f} seconds")
print(f"CORRUPT ROWS FOUND: {error_counter.value}")

for sensor, avg in sorted(final_results):
    print(f"Sensor {sensor}: {avg}°C")

# Keep UI open to inspect partitions
print("\nCheck http://localhost:4040 to see the 4 partitions. Press Enter to exit.")
input()
sc.stop()