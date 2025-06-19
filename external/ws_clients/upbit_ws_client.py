# external/ws_clients/upbit_ws_client.py

import asyncio
import json
import logging
import websockets
from kafka import KafkaProducer


class UpbitWSClient:
    def __init__(self, symbols: list[str], kafka_config: dict):
        self.symbols = symbols
        self.kafka_config = kafka_config
        self.ws_url = "wss://api.upbit.com/websocket/v1"
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_config["bootstrap_servers"],
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        self.topic = kafka_config["topic"]
        self.logger = logging.getLogger(__name__)

    def build_payload(self) -> list[dict]:
        return [
            {"ticket": "test"},
            {"type": "trade", "codes": self.symbols},
            {"format": "DEFAULT"}
        ]

    async def connect_and_listen(self):
        self.logger.info("Connecting to Upbit WebSocket server...")
        try:
            async with websockets.connect(self.ws_url) as websocket:
                await websocket.send(json.dumps(self.build_payload()))
                self.logger.info("Subscribed to: %s", self.symbols)

                while True:
                    message = await websocket.recv()
                    parsed = json.loads(message)
                    self.producer.send(self.topic, parsed)
                    self.logger.info("Sent message to Kafka: %s", parsed)

        except Exception as e:
            self.logger.error("WebSocket error: %s", str(e))

    def connect(self):
        asyncio.get_event_loop().run_until_complete(self.connect_and_listen())

    def disconnect(self):
        # 실제 사용 시에는 websockets 객체를 외부에서 제어하도록 수정할 수 있음
        self.logger.info("Disconnect called — not implemented (use process-level kill)")