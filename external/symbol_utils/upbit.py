# external/symbol_utils/upbit.py

def map_base_to_market_pair(symbol: str, quote_currency: str = "USDT") -> str:
    """
    업비트용 거래쌍 포맷으로 변환 (e.g., BTC → USDT-BTC)
    """
    return f"{quote_currency}-{symbol}"