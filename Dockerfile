# Start from the same image you were using
FROM jupyter/pyspark-notebook:spark-3.3.0

# Switch to root to install packages if needed (optional but often safer for permissions)
USER root

# Install Streamlit and any other libraries you need
RUN pip install streamlit

# Switch back to the default user (jovyan) to avoid permission issues at runtime
USER ${NB_UID}