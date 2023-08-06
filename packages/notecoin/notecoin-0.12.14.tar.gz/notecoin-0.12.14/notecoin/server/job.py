from fastapi import FastAPI
from notecoin.server.account_server import AccountAccount
from notecoin.server.market_server import MarketTickers

app = FastAPI()
app.include_router(MarketTickers())
app.include_router(AccountAccount())

# uvicorn job:app --host '0.0.0.0' --port 8446 --reload
