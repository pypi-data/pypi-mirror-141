from fastapi import FastAPI
from notecoin.okex.server.const import account_account, market_tickers

app = FastAPI()
app.include_router(account_account)
app.include_router(market_tickers)

# uvicorn notecoin:app --host '0.0.0.0' --port 8444 --reload
