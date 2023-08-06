from fastapi import FastAPI
from notecoin.server.market_coins import MarketCoins

app = FastAPI()
app.include_router(MarketCoins(prefix='/market'))

#uvicorn job:app --host '0.0.0.0' --port 8446 --reload
