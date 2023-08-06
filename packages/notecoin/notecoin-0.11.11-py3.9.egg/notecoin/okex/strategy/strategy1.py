from flask_classful import FlaskView
from notecoin.okex.strategy.domain import OkexCoin
from notecoin.okex.strategy.utils import account_api, market_api


class Strategy1(FlaskView):
    def __init__(self):
        self.usdt = 0
        self.coin_map = {}

    def load_account(self):
        data = account_api.get_account().data[0]
        self.coin_map = {}
        for detail in data['details']:
            if detail['ccy'] == 'USDT':
                self.usdt = detail['availBal']
                continue
            coin = OkexCoin.instance_by_account(detail)
            if coin.money > 1:
                self.coin_map[coin.coin_id] = coin

    def update_price(self):
        data = market_api.get_ticker().data
        data_map = dict([(cin['instId'], cin['last']) for cin in data])
        for coin in self.coin_map.values():
            coin.price = data_map[coin.coin_id]

    def to_json(self):
        return {
            "res": self.usdt,
            "coins": [coin.to_json() for coin in self.coin_map.values()]
        }

    def update(self):
        self.load_account()
        self.update_price()
        for coin in self.coin_map.values():
            coin.watch()
        return self.to_json()
