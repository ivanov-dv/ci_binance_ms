import asyncio

from engine import app, monitoring


@app.on_event("startup")
async def on_startup():
    asyncio.create_task(monitoring.reset_weight())
    asyncio.create_task(monitoring.get_list_tickers())
    asyncio.create_task(monitoring.check_all_changes())


@app.get('/prices/{ticker}')
async def get_current_price(ticker: str):
    return await monitoring.get_ticker_price(ticker.upper())


@app.get('/tickers')
async def get_tickers():
    return monitoring.list_tickers


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
