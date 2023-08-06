from notecoin.okex.strategy.utils import account_api, market_api, trade_api


class OkexCoin:
    def __init__(self, coin_id='METIS-USDT', count=0.):
        self.coin_id = coin_id
        self.count = count
        self.price_in = self.current_price
        self.price = self.price_in

    @property
    def current_price(self):
        self.price = float(market_api.get_ticker(self.coin_id).data[0]['last'])
        return self.price

    @property
    def money(self):
        return self.price * self.count

    def buy(self):
        print("sell")
        return trade_api.place_order(instId=self.coin_id, tdMode='cash', side='buy', ordType='market', sz='50')

    def sell(self):
        coin_dict = dict([(line['ccy'], line['availBal']) for line in account_api.get_account().data[0]['details']])
        count = coin_dict[self.coin_id.split('-')[0]]
        return trade_api.place_order(instId=self.coin_id, tdMode='cash', side='sell', ordType='market', sz=count)

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
        money = self.money
        if money > 52 or money < 48:
            self.sell()

    def __str__(self):
        return f"{self.coin_id}\t{self.count}\t{self.price_in}\t{self.price}\t{self.money}"

    def to_json(self):
        return {
            "coin_id": self.coin_id,
            # "count": self.count,
            # "price_in": self.price_in,
            # "price": price,
            "usdt": self.count * self.price
        }
