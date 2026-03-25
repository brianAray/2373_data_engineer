from pyspark import SparkContext
import shutil
import os

sc = SparkContext.getOrCreate()

# 1. LOAD
raw_logs = sc.textFile("logs.txt")

# 2. TRANSFORM (Narrow)
# Every line is checked locally; no data moves between nodes.
critical_logs = raw_logs.filter(lambda line: "ERROR" in line or "FATAL" in line)

# 3. ACTION (Eager)
# This triggers the filter and writes the result to a directory.
# If "error_logs" already exists, this will throw an error!
output_dir = "critical_logs_output"
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

critical_logs.saveAsTextFile(output_dir)

print("Logs have been saved to the 'critical_logs_output' directory.")
sc.stop()