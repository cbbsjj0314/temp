# external/kafka_producers/upbit_producer.py

import logging
from symbol_utils.upbit_ws import get_upbit_ws_symbols
from ws_clients.upbit_ws_client import UpbitWSClient


class UpbitKafkaProducer:
    def __init__(self, redis_config: dict, kafka_config: dict):
        self.redis_config = redis_config
        self.kafka_config = kafka_config
        self.ws_client = None

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def reload_ws_subscription(self):
        """
        Redis에서 최신 심볼 목록 로드 + 웹소켓 구독 갱신
        """
        ws_symbols = get_upbit_ws_symbols(**self.redis_config)

        if not ws_symbols:
            self.logger.warning("No symbols found to subscribe.")
            return

        self.logger.info(f"Reloading subscription with symbols: {ws_symbols}")

        if self.ws_client:
            self.logger.info("Disconnecting existing WebSocket client...")
            self.ws_client.disconnect()

        self.ws_client = UpbitWSClient(ws_symbols, self.kafka_config)
        self.logger.info("Connecting new WebSocket client...")
        self.ws_client.connect()


# if __name__ == "__main__":
#     redis_conf = {
#         "redis_host": "localhost",
#         "redis_port": 6379,
#         "redis_db": 0,
#         "redis_password": None
#     }

#     kafka_conf = {
#         "bootstrap_servers": "localhost:9092",
#         "topic": "upbit-stream"
#     }

#     producer = UpbitKafkaProducer(redis_conf, kafka_conf)
#     producer.reload_ws_subscription()
