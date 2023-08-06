from fastapi import FastAPI
from notecoin.server.market_coins import MarketCoins
from notecoin.server.account_server import AccountCoins
app = FastAPI()
app.include_router(MarketCoins(prefix='/market'))
app.include_router(AccountCoins())

# uvicorn job:app --host '0.0.0.0' --port 8446 --reload
