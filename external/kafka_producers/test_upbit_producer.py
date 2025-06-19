# external/kafka_producers/test_upbit_producer.py

from upbit_producer import UpbitKafkaProducer

redis_conf = {
    "redis_host": "localhost",
    "redis_port": 6379,
    "redis_db": 0,
    "redis_password": None
}

kafka_conf = {
    "bootstrap_servers": "localhost:9092",
    "topic": "upbit-stream"
}

producer = UpbitKafkaProducer(redis_conf, kafka_conf)
producer.reload_ws_subscription()