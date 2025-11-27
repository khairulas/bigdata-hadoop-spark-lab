# --- RUN THIS AS ONE BLOCK TO AVOID ERRORS ---

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, desc
import pandas as pd
import matplotlib.pyplot as plt
import os
import time

# 1. SETUP
os.environ["HADOOP_USER_NAME"] = "root"

print("Initializing Spark...")
spark = SparkSession.builder \
    .appName("Lab1_Combined_Fix") \
    .master("spark://spark-master:7077") \
    .config("spark.driver.host", "bigdata-jupyter") \
    .config("spark.driver.bindAddress", "0.0.0.0") \
    .config("spark.driver.port", "20002") \
    .config("spark.blockManager.port", "20003") \
    .config("spark.executor.memory", "512m") \
    .config("spark.hadoop.dfs.client.use.datanode.hostname", "true") \
    .getOrCreate()

# 2. INGEST
print("Reading CSV...")
pdf = pd.read_csv("/home/jovyan/work/raw_sales_data.csv")
df_raw = spark.createDataFrame(pdf)

# 3. TRANSFORM
df_processed = df_raw.withColumn("revenue", col("price") * col("quantity"))

# 4. LOAD (Write to HDFS)
hdfs_path = f"hdfs://namenode:9000/user/data/processed_sales_{int(time.time())}"
print(f"Writing to HDFS: {hdfs_path}")
df_processed.write.mode("overwrite").parquet(hdfs_path)

# 5. ANALYZE
print("Aggregating Data...")
df_lake = spark.read.parquet(hdfs_path)
df_report = df_lake.groupBy("category") \
    .agg(_sum("revenue").alias("total_revenue")) \
    .orderBy(desc("total_revenue"))

# 6. VISUALIZE (Matplotlib)
print("Generating Chart...")
pdf_report = df_report.toPandas()

plt.figure(figsize=(10, 6))
plt.bar(pdf_report['category'], pdf_report['total_revenue'], color='#2ca02c')
plt.xlabel('Category')
plt.ylabel('Total Revenue ($)')
plt.title('Total Revenue by Product Category')
plt.ticklabel_format(style='plain', axis='y')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()

spark.stop()