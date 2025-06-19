# api/main.py

from fastapi import FastAPI, Request
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/reload")
async def reload_symbols(req: Request):
    body = await req.json()
    changed = body.get("changed")
    logger.info(f"/reload endpoint called — source: {changed}")
    return {"status": "ok", "source": changed}
