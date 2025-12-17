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