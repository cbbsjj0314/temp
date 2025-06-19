# DEQ-45

# external/upbit_symbol_utils.py

import json
import redis
import logging
from typing import Set

def detect_symbol_change(
    redis_client: redis.Redis,
    new_symbols: Set[str],
    redis_key: str,
) -> bool:
    """
    Redis에 저장된 거래쌍과 새로운 거래쌍을 비교하여 변화 여부 반환
    """
    logger = logging.getLogger(__name__)

    prev_raw = redis_client.get(redis_key)
    if prev_raw is None:
        logger.info(f"No previous value for {redis_key} → Considering it as a change")
        return True

    try:
        prev_symbols = set(json.loads(prev_raw))
    except json.JSONDecodeError:
        logger.warning(f"Could not decode {redis_key} → Considering it as a change")
        return True

    if prev_symbols != new_symbols:
        logger.info(f"Change detected in {redis_key}")
        return True
    else:
        logger.info(f"No change in {redis_key}")
        return False
