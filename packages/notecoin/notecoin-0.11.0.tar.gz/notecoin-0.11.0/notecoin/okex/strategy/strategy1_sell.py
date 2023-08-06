import time

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

    @property
    def current_price(self):
        return float(market.get_ticker(self.coin_id).data[0]['last'])

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
        price = self.current_price
        if price > self.price_in * 1.01:
            self.sell()

    def __str__(self):
        price = self.current_price
        return f"{self.coin_id}\t{self.count}\t{self.price_in}\t{price}\t{self.count * price}"


class CoinList:
    def __init__(self):
        self.usdt = 0
        self.coin_map = {}

    def load(self):
        data = account.get_account().data[0]

        for detail in data['details']:
            if detail['ccy'] == 'USDT':
                self.usdt = detail['availBal']
                continue
            coin = OkexCoin.instance_by_account(detail)
            if coin.coin_id not in self.coin_map.keys():
                self.coin_map[coin.coin_id] = coin

    def print(self):
        print("****************************************************")
        print(self.usdt)
        for coin in self.coin_map.values():
            print(coin)

    def watch(self):
        while True:
            self.load()
            self.print()
            time.sleep(1)
            for coin in self.coin_map.values():
                coin.watch()


col = CoinList()
col.watch()
