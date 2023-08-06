import pickle
from typing import Any

import pandas as pd
import redis
import six
from fastapi import APIRouter
from notebuild.tool.fastapi import add_api_routes, api_route
from notecoin.database.connect import RedisConnect
from notecoin.strategy.utils import market_api


class RedisStrategy(APIRouter):
    def __init__(self, cache_prefix='cache', host='localhost', port=6379, *args, **kwargs):
        self.cache_prefix = cache_prefix
        self.redis_client = redis.Redis(host=host, port=port, decode_responses=False)
        super(RedisStrategy, self).__init__(*args, **kwargs)

    def update(self, suffix=""):
        raise Exception("not implements")

    def read(self, suffix=""):
        data = self.redis_client.get(self.key(suffix=suffix))
        return pickle.loads(six.ensure_binary(data, encoding='latin1'))

    def key(self, suffix=""):
        return f"{self.cache_prefix}_{suffix}"

    def put(self, key, value: Any):
        self.redis_client.set(key, pickle.dumps(value))


class MarketCoins(RedisConnect):
    def __init__(self, *args, **kwargs):
        super(MarketCoins, self).__init__(*args, **kwargs)
        add_api_routes(self)

    @api_route('/update', description="update market tickers")
    def update_value(self, suffix=""):
        data = pd.DataFrame(market_api.get_tickers(instType='SPOT').data)
        self.put(self.get_key(suffix=suffix), data)
        return {"success": len(data)}

    @api_route('/read', description="read market tickers")
    def get_value(self, suffix=""):
        return super(MarketCoins, self).get_value(suffix=suffix)


coin = MarketCoins()
print(len(coin.get_value()))
print(type(coin.get_value()))
