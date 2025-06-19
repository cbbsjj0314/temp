import redis, json

r = redis.Redis(host="localhost", port=6379, db=0)
krw = json.loads(r.get("upbit:market_pairs:krw"))
usdt = json.loads(r.get("upbit:market_pairs:usdt"))
common = json.loads(r.get("upbit:common_symbols"))

print("KRW Pairs:", krw)
print("USDT Pairs:", usdt)
print("Base Symbols:", common)