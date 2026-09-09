import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


from pyspark.sql import SparkSession  
from pyspark.sql.functions import col, when  

spark = SparkSession.builder.appName("orders_analysis").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

data = [
    (1, "Ali Khan", 49.99),
    (2, "Sara Ahmed", 120.50),
    (3, "Zainab Fayyaz", 15.00),
    (4, "Bilal Ahmed", 200.00),
    (5, "Hina Malik", 30.00),
]
columns = ["order_id", "customer_name", "amount"]

df = spark.createDataFrame(data, columns)

print("--- Show the DataFrame ---")
df.show()

print("--- Schema (like DESCRIBE TABLE) ---")
df.printSchema()

print("--- Filter: amount > 100 ---")
df.filter(col("amount") > 100).show()

print("--- Add a classification column ---")
df_classified = df.withColumn(
    "classification",
    when(col("amount") > 100, "High order value")
    .when(col("amount") >= 20, "Medium order value")
    .otherwise("Low order value")
)
df_classified.show()

spark.stop()
