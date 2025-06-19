# external/symbol_utils/upbit_ws.py

import redis
import json
from .upbit import map_base_to_market_pair

def get_upbit_ws_symbols(
    redis_host: str = "localhost",
    redis_port: int = 6379,
    redis_db: int = 0,
    redis_password: str = None,
    quote_currencies: list[str] = ["KRW", "USDT"],
) -> list[str]:
    """
    Redis에서 KRW와 USDT 마켓 base 심볼을 불러옴
    각각의 거래쌍 포맷으로 변환 후 합침
    """
    client = redis.Redis(
        host=redis_host, port=redis_port, db=redis_db, password=redis_password
    )
    
    all_symbols = []

    for quote in quote_currencies:
        raw_data = client.get(f"symbol:upbit:{quote.lower()}")
        if not raw_data:
            continue
        base_symbols = json.loads(raw_data)
        all_symbols.extend([f"{quote}-{sym}" for sym in base_symbols])
    
    return all_symbols
