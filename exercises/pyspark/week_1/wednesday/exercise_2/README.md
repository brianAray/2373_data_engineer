## Exercise 2

Read `transactions.txt`. Calculate the total spend per category. However, before saving, ensure the data is consolidated into **exactly 2 partitions** so that the output results in only two files.

```python
from pyspark import SparkContext
import shutil
import os

sc = SparkContext.getOrCreate()

# 1. LOAD & TRANSFORM: Read transactions.txt and map to (Category, Price)
# 2. SHUFFLE: Use reduceByKey to get totals.
# 3. REPARTITION: Force the RDD into exactly 2 partitions.
# 4. ACTION: Save the result to "category_totals"

output_dir = "category_totals_output"
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

sc.stop()
```