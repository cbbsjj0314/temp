FROM apache/airflow:2.10.4

USER root

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt

USER airflow
WORKDIR /opt/airflow

RUN pip install --no-cache-dir -r /requirements.txt