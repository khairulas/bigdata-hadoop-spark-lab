# Big Data Lab: Apache Spark & HDFS on Docker

A containerized environment for teaching Big Data processing using **Apache Spark (PySpark)**, **JupyterLab**, and **Hadoop HDFS**.

## Architecture
* **Compute:** Apache Spark 3.3 (Master + Worker)
* **Interface:** JupyterLab (Python 3.10)
* **Storage:** Hadoop HDFS (NameNode + DataNode)
## 📥 Installation

1. **Clone the Repository**
    Open your terminal (PowerShell or CMD) and run:
    ```bash
    git clone https://github.com/khairulas/bigdata-hadoop-spark-lab.git
    ```

2.  **Navigate to the Directory**
    ```bash
    cd bigdata-hadoop-hive-lab

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
Open your browser to: http://localhost:8888  *Go to section Getting Jupyter Token below to get Jupyter token.

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
**Using Jupyter Notebook, open LabExample.ipynb notebook.**

Ingest: Upload a CSV to the Jupyter interface.

Process: Use Pandas to read the CSV and convert it to a Spark DataFrame.

Store: Write the DataFrame to HDFS (hdfs://namenode:9000/user/data/...).

Analyze: Read the Parquet file back from HDFS and run SQL queries.

# Getting Jupyter Token

## Option 1: Get the Token (Immediate Fix)
1. Open your PowerShell terminal again.

2. Run this command to see the logs inside the Jupyter container:

```PowerShell

docker logs bigdata-jupyter
```

3. Scroll to the bottom. You will see a block of text that looks like this:

```Plaintext

http://127.0.0.1:8888/lab?token=c8de56fa... (long string of characters)
```

4. Copy only the token part (the long string of characters after token=) and paste it into the "Password or token" box in your browser.

5. Click "Log in".

## Option 2: Disable the Token (For Convenience)
Since this is a local learning lab, you probably don't want to copy-paste a token every time you restart Docker. You can disable the password requirement permanently.

1. Open your docker-compose.yml file.

2. Find the jupyter service section.

3. Add the line command: start-notebook.sh --IdentityProvider.token='' at the end of that section.

# Data Visualization
### 1. How to Visualize with Python (Streamlit)
Students can build interactive web dashboards directly inside the container.

Install Library: In Jupyter, run pip install streamlit.

Create App: Create a file dashboard.py in Jupyter:

```Python

import streamlit as st
import pandas as pd
import numpy as np

st.title('Big Data Sales Dashboard')

# Simulate reading from HDFS or Spark processing result
df = pd.DataFrame({
    'Category': ['Electronics', 'Clothing', 'Home'],
    'Revenue': [50000, 30000, 45000]
})

st.bar_chart(df.set_index('Category'))
```

Run it: Open a Terminal inside Jupyter and run:

```Bash

streamlit run dashboard.py
```

View it: Open http://localhost:8501 in your Windows browser.

### 2. How to Visualize with Power BI
Since we added the spark-thrift-server, Power BI can now query your cluster.

1. Prerequisite: Install the Simba Spark ODBC Driver (available from Databricks or widely online) on your Windows machine.

2. Configure ODBC:

  * Open "ODBC Data Sources (64-bit)" on Windows.

  * Add a new System DSN for Spark.

  * Host: localhost

  * Port: 10000

  * Auth Mechanism: User Name (use admin, no password).

3. Connect in Power BI:

  * Get Data -> ODBC.

  * Select your Spark DSN.

  * In the "Advanced Options" SQL statement box, you can query data directly from HDFS using SparkSQL:

```SQL

-- Example: Read a Parquet file sitting in HDFS
SELECT * FROM parquet.`hdfs://namenode:9000/user/data/processed_sales`
```

  * Click Load.