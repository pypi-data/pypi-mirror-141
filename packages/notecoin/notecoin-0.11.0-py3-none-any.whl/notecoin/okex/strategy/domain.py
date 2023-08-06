from notecoin.okex.strategy.utils import market_api, trade_api


class OkexCoin:
    def __init__(self, coin_id='METIS-USDT', count=0.):
        self.coin_id = coin_id
        self.count = count
        self.price_in = self.current_price

    @property
    def current_price(self):
        return float(market_api.get_ticker(self.coin_id).data[0]['last'])

    @property
    def money(self):
        return self.current_price * self.count

    def buy(self):
        print("sell")
        return trade_api.place_order(instId=self.coin_id, tdMode='cash', side='buy', ordType='market', sz='50')

    def sell(self):
        return trade_api.place_order(instId=self.coin_id, tdMode='cash', side='sell', ordType='market', sz=self.count)

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
