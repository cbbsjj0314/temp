# external/kafka_producers/run_upbit_producer.py

import os
import logging
from upbit_producer import UpbitKafkaProducer

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    redis_conf = {
        "redis_host": os.getenv("REDIS_HOST", "redis-data"),
        "redis_port": int(os.getenv("REDIS_PORT", 6379)),
        "redis_db": int(os.getenv("REDIS_DB", 0)),
        "redis_password": os.getenv("REDIS_PASSWORD", None),
    }

    kafka_conf = {
        "bootstrap_servers": os.getenv("KAFKA_BOOTSTRAP", "kafka:9092"),
        "topic": os.getenv("KAFKA_TOPIC", "upbit-stream"),
    }

    producer = UpbitKafkaProducer(redis_conf, kafka_conf)
    producer.reload_ws_subscription()

if __name__ == "__main__":
    main()