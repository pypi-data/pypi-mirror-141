import pandas as pd
from notebuild.tool.fastapi import add_api_routes, api_route
from notecoin.database.connect import RedisConnect
from notecoin.strategy.utils import market_api


class MarketCoins(RedisConnect):
    def __init__(self, *args, **kwargs):
        super(MarketCoins, self).__init__(*args, **kwargs)
        add_api_routes(self)

    @api_route('/update', description="update market tickers")
    def update_value(self, suffix=""):
        data = pd.DataFrame(market_api.get_tickers(instType='SPOT').data)
        self.put_value(self.get_key(suffix=suffix), data)
        return {"success": len(data)}

    @api_route('/read', description="read market tickers")
    def get_value(self, suffix=""):
        return super(MarketCoins, self).get_value(suffix=suffix)
