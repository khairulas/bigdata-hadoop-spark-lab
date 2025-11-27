# Big Data Lab: Apache Spark & HDFS on Docker

A containerized environment for teaching Big Data processing using **Apache Spark (PySpark)**, **JupyterLab**, and **Hadoop HDFS**.

## Architecture
* **Compute:** Apache Spark 3.3 (Master + Worker)
* **Interface:** JupyterLab (Python 3.10)
* **Storage:** Hadoop HDFS (NameNode + DataNode)

## Quick Start

### 1. Start the Cluster
```bash
docker-compose up -d
```

### 2. Unlock HDFS Permissions
Once the containers are running, run this command in your terminal to allow Spark to write to the storage layer:

```Bash

docker exec -it namenode hdfs dfs -chmod -R 777 /
```

### 3. Access JupyterLab
Open your browser to: http://localhost:8888

Critical: How to Connect Spark to HDFS
In every new Notebook, you must use this specific configuration block to ensure Spark talks to the Docker container correctly.

```Python

from pyspark.sql import SparkSession
import os

# 1. Setup Environment
os.environ["HADOOP_USER_NAME"] = "root"

# 2. Initialize Spark with Docker Network Fixes
spark = SparkSession.builder \
    .appName("Student_Lab") \
    .master("spark://spark-master:7077") \
    .config("spark.driver.host", "bigdata-jupyter") \
    .config("spark.driver.bindAddress", "0.0.0.0") \
    .config("spark.driver.port", "20002") \
    .config("spark.blockManager.port", "20003") \
    .config("spark.executor.memory", "512m") \
    .config("spark.hadoop.dfs.client.use.datanode.hostname", "true") \
    .getOrCreate()

print("Spark Connected!")
```

## Lab Exercises
Ingest: Upload a CSV to the Jupyter interface.

Process: Use Pandas to read the CSV and convert it to a Spark DataFrame.

Store: Write the DataFrame to HDFS (hdfs://namenode:9000/user/data/...).

Analyze: Read the Parquet file back from HDFS and run SQL queries.