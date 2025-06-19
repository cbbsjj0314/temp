# external/collect_upbit_symbols.py

import os
import logging
from upbit_symbol_collector import UpbitSymbolCollector

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    try:
        collector = UpbitSymbolCollector(
            redis_host=os.getenv("REDIS_HOST", "redis-data"),
            redis_port=int(os.getenv("REDIS_PORT", 6379)),
            redis_db=int(os.getenv("REDIS_DB", 0)),
            redis_password=os.getenv("REDIS_PASSWORD", None) or None,
        )
        collector.run()
    except Exception as e:
        logger.error(f"Exception occurred during collection: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
