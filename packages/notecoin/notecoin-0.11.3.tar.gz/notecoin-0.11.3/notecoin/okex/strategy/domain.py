from notecoin.okex.v5.client import (AccountClient, AssetClient, MarketClient,
                                     PublicClient, TradeClient)
from notetool.secret import read_secret

api_key = read_secret(cate1='coin', cate2='okex', cate3='api_key')
secret_key = read_secret(cate1='coin', cate2='okex', cate3='secret_key')
passphrase = read_secret(cate1='coin', cate2='okex', cate3='passphrase')

account = AccountClient(api_key, secret_key, passphrase)
fundingAPI = AssetClient(api_key, secret_key, passphrase)
market = MarketClient(api_key, secret_key, passphrase)
publicAPI = PublicClient(api_key, secret_key, passphrase)
tradeAPI = TradeClient(api_key, secret_key, passphrase)


class OkexCoin:
    def __init__(self, coin_id='METIS-USDT', count=0.):
        self.coin_id = coin_id
        self.count = count
        self.price_in = self.current_price
        self.price = self.price_in

    @property
    def current_price(self):
        self.price = float(market.get_ticker(self.coin_id).data[0]['last'])
        return self.price

    @property
    def money(self):
        return self.current_price * self.count

    def buy(self):
        print("sell")
        return tradeAPI.place_order(instId=self.coin_id, tdMode='cash', side='buy', ordType='market', sz='50')

    def sell(self):
        coin_dict = dict([(line['ccy'], line['availBal']) for line in account.get_account().data[0]['details']])
        count = coin_dict[self.coin_id.split('-')[0]]
        return tradeAPI.place_order(instId=self.coin_id, tdMode='cash', side='sell', ordType='market', sz=count)

    @staticmethod
    def instance_by_account(data):
        okex = OkexCoin(coin_id=f"{data['ccy']}-USDT", count=float(data['availBal']))
        return okex

    @staticmethod
    def instance_by_new(coin_id):
        okex = OkexCoin(coin_id=coin_id)
        okex.buy()
        return okex

    def watch(self):
        if self.money > 52:
            self.sell()

    def __str__(self):
        price = self.current_price
        return f"{self.coin_id}\t{self.count}\t{self.price_in}\t{price}\t{self.count * price}"

    def to_json(self):
        return {
            "coin_id": self.coin_id,
            # "count": self.count,
            # "price_in": self.price_in,
            # "price": price,
            "usdt": self.count * self.price
        }
