# import os
# import sys
# os.environ["PYSPARK_PYTHON"] = sys.executable
# os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

# from pyspark.sql import SparkSession
# from pyspark.sql.functions import col, when, rand, floor

# spark = SparkSession.builder.appName("big_orders").getOrCreate()
# spark.sparkContext.setLogLevel("ERROR")

# df = spark.range(0, 500000).withColumnRenamed("id", "order_id")
# df = df.withColumn("customer_id", (floor(rand() * 1000)).cast("int"))
# df = df.withColumn("amount", (rand() * 500).cast("double"))

# print("--- Row count ---")
# print(df.count())

# print("--- Sample rows ---")
# df.show(5)

# # Convert to pandas and let pandas write the Parquet file (bypasses Hadoop entirely)
# pandas_df = df.toPandas()
# pandas_df.to_parquet("big_orders_parquet_single.parquet")
# print("Written via pandas to big_orders_parquet_single.parquet")

# spark.stop()

# Read the Parquet file back in Spark
import os, sys, time
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("read_big_orders").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df = spark.read.parquet("big_orders_parquet_single.parquet")

start = time.time()
high_value_count = df.filter(col("amount") > 400).count()
elapsed = time.time() - start

print(f"Found {high_value_count} high-value orders (>400) in {elapsed:.3f} seconds")
spark.stop()