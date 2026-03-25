from pyspark import SparkContext

# 0. THE ENTRY POINT
# SparkContext represents the connection to a spark cluster
# "local" tells spark to run on your laptop using one thread
# in production, this would connect to a cluster manager like YARN or Kubernetes
# it is responsible for creating RDDs and distributing the code to worker nodes
sc = SparkContext("local", "RDD_Example")

# 1. SHARED VARIABLES
# Broadcast: A read-only variable sent to all nodes (e.g., a tax rate)
# This shouldn't be used with only a single value, it is meant to be an efficient way to send variables across different tasks
# This reduces load if the broadcast variable is large and needs to be shared across the jobs
# Instead of having a new copy for each job, they can just reference the broadcast variable
# If the value is small, then there is no need for the overhead that comes from using broadcast variables
tax_rate = sc.broadcast(0.05) 

# Accumulator: A write-only "counter" (e.g., counting errors)
# A global variable that workers can only increment (write-only)
# only the driver program can read the final value.
# good for debugging or counting errors across a distributed dataset without complex joins
invalid_rows = sc.accumulator(0)

# 2. DATA LOADING (RDD)
# Loading a simple list into an RDD (parallelized)
# sc.parallelize takes a local python collection and turns it into an RDD
# this is called "distributing" the data
# Spark breaks this list into "Partitions" the basic unit of parallelism
# Each partition is handled by a different CPU core or worker node
raw_data = ["Apples,10", "Oranges,20", "Apples,5", "BAD_DATA", "Oranges,10"]
rdd = sc.parallelize(raw_data)

# 3. TRANSFORMATIONS (Lazy Evaluation)
# Transformations createa  lineage or a recipe (DAG)
# Spark doesn't actually execute these lines when they are defined
# it just verifies the logic and adds it to the  plan
def parse_line(line):
    try:
        parts = line.split(",")
        # Creating a KEY-VALUE PAIR: (Product, Price)
        #  These are essential for aggregations like reduceByKey
        return (parts[0], float(parts[1]))
    except:
        invalid_rows.add(1) # Updating the Accumulator
        return None

# Filter out None and transform
# Map/Filter are transformations
# narrow transformations
cleaned_rdd = rdd.map(parse_line).filter(lambda x: x is not None)

# Apply tax using the Broadcast Variable
taxed_rdd = cleaned_rdd.mapValues(lambda price: price * (1 + tax_rate.value))


# Key-Value Pair Transformation: Total by Key
# reduceByKey merges values for each key
# This triggers a "Shuffling" to move the data across different worker nodes
# Spark needs to ensure that all values for the same key (e.g. all apples) end up on the same partition so they can be summed together
# This is the primary bottleneck in Spark
# Disk I/O as Data is written to and read from the disk of the worker nodes
# Network I/O as large amounts of data are sent across the cluster
# Serialization as data must be converted into a format that can be sent over the network and then "unpacked" on the other side

# Narrow vs wide
# narrow transformations e.g. map
# no data movement as it stays within the partition
# very fast
# only the lost partition needs recomputing if it fails

# wide transformations e.g. reduceByKey
# High data movement as it moves across nodes (shuffle)
# slow as it is resource intensive
# may require re-computing multiple stages if it fails
totals_rdd = taxed_rdd.reduceByKey(lambda x, y: x + y)

# 4. ACTIONS (Eager Evaluation - Triggers the work)
# This is the go button, Spark looks at the RDDlineagea nd optimize the execution
# .collect() pulls the entire distributed datast into the drivers memory as a python list
# if the dataset is 1tb and your ram is 8gb, it will crash
results = totals_rdd.collect() # Brings data to the driver

# once collected, your back to standard python
print(f"Final Totals: {results}")
print(f"Invalid Rows Encountered: {invalid_rows.value}")

# 5. SAVING DATA
# saveAsTextFile is an ACTION that writes data directly from the workers to storage
# it does notgo trhough the  driver (unlike collect)
# it creates a directory because each partition writes its own file simultaneously
totals_rdd.saveAsTextFile("output/sales_totals")

sc.stop()