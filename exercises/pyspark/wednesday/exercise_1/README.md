## Exercise 1

Read `logs.txt`, filter for "ERROR" and “FATAL”, and instead of just counting them, **save** those error lines into a directory called `critical_logs_output`.

```python
from pyspark import SparkContext
import shutil
import os
sc = SparkContext.getOrCreate()

# 1. LOAD: logs.txt
# 2. TRANSFORM: Filter for "ERROR" or "FATAL"
# 3. ACTION: Save the RDD to "critical_logs"
# NOTE: Check your folder; you'll see how Spark creates a directory, not just a file.
output_dir = "critical_logs_output"
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

sc.stop()
```