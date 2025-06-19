# external/upbit_symbol_collector.py

import requests
import redis
import json
import logging
from typing import List, Set, Tuple

class UpbitSymbolCollector:
    """업비트에서 KRW, USDT 마켓의 base 심볼을 수집하고, Redis에 저장"""
    def __init__(
        self,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
        redis_password: str = None,
    ):
        self.api_url = "https://api.upbit.com/v1/market/all"
        self.redis_client = redis.Redis(
            host=redis_host, port=redis_port, db=redis_db, password=redis_password
        )
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def fetch_market_data(self) -> List[dict]:
        """REST API로 업비트 거래쌍 목록 수집"""
        headers = {"Accept": "application/json"}
        response = requests.get(self.api_url, headers=headers)
        response.raise_for_status()
        return response.json()

    def filter_base_symbols(self, market_data: List[dict]) -> Tuple[Set[str], Set[str], Set[str]]:
        """
        KRW, USDT 마켓의 base 심볼 추출
        교집합 추출 부분은 삭제함
        """
        krw_bases, usdt_bases = set(), set()

        for item in market_data:
            market = item.get("market", "")
            if market.startswith("KRW-"):
                krw_bases.add(market.split("-")[1])
            elif market.startswith("USDT-"):
                usdt_bases.add(market.split("-")[1])

        return krw_bases, usdt_bases

    def save_to_redis(self, krw_bases: Set[str], usdt_bases: Set[str]) -> None:
        """
        Redis에 결과 저장
        symbol:upbit:krw -> 업비트의 KRW 거래쌍의 심볼들
        symbol:upbit:usdt -> 업비트의 USDT 거래쌍의 심볼들
        없어짐: symbol:upbit:base -> 위 2개 심볼 교집합 (웹소켓 구독 대상)
        """
        self.redis_client.set("symbol:upbit:krw", json.dumps(sorted(krw_bases)))
        self.redis_client.set("symbol:upbit:usdt", json.dumps(sorted(usdt_bases)))

    def run(self):
        """전체 실행 흐름"""
        market_data = self.fetch_market_data()
        krw_bases, usdt_bases = self.filter_base_symbols(market_data)

        self.save_to_redis(krw_bases, usdt_bases)
        self.logger.info(f"Saved: {len(krw_bases)} KRW bases, {len(usdt_bases)} USDT bases")


if __name__ == "__main__":
    """
    개발 중 단독 실행 테스트 용도
    운영 환경에서는 collect_upbit_symbols.py를 사용하쇼
    """
    # collector = UpbitSymbolCollector(redis_host="redis-data")
    collector = UpbitSymbolCollector(redis_host="localhost")
    collector.run()
