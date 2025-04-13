import asyncio
import logging

import sentry_sdk
import uvicorn
from fastapi import HTTPException

from config import SENTRY_DSN
from engine import app, monitoring


@app.on_event("startup")
async def on_startup():
    asyncio.create_task(monitoring.reset_weight())
    asyncio.create_task(monitoring.get_list_tickers())
    asyncio.create_task(monitoring.check_all_changes())


@app.get('/prices/{ticker}')
async def get_current_price(ticker: str):
    try:
        return await monitoring.get_ticker_price(ticker.upper())
    except Exception as e:
        logging.error(f'get_current_price error: {e}')
        raise HTTPException(status_code=500, detail=f'get_current_price error: {e}')


@app.get('/tickers')
async def get_tickers():
    return monitoring.list_tickers


@app.get('/metrics')
async def get_metrics():
    return await monitoring.get_metrics()


if __name__ == "__main__":
    if SENTRY_DSN:
        sentry_sdk.init(SENTRY_DSN)
    uvicorn.run(app, host="0.0.0.0", port=8002)
