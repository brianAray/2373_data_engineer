from pyspark import SparkContext

sc = SparkContext("local[2]", "ui_test_job")

data = sc.parallelize(range(100), 4) #  4 partitions
result = data.map(lambda x: x *2).reduce(lambda x, y: x + y)

print(f"results: {result}")

# We are going to ask the user to press enter to stop the  app

print("\nSpark UI is live")
input()

sc.stop()