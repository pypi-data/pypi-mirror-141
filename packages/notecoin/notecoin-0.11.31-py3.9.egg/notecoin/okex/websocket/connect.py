import base64
import hmac
import json
import logging
import time
import zlib

from websocket import WebSocket, WebSocketException, create_connection


def get_local_timestamp():
    return int(time.time())


def partial(res):
    data_obj = res['data'][0]
    bids = data_obj['bids']
    asks = data_obj['asks']
    instrument_id = res['arg']['instId']
    # print('全量数据bids为:' + str(bids))
    # print('档数为:' + str(len(bids)))
    # print('全量数据asks为:' + str(asks))
    # print('档数为:' + str(len(asks)))
    return bids, asks, instrument_id


def update_bids(res, bids_p):
    # 获取增量bids数据
    bids_u = res['data'][0]['bids']
    # print('增量数据bids为:' + str(bids_u))
    # print('档数为:' + str(len(bids_u)))
    # bids合并
    for i in bids_u:
        bid_price = i[0]
        for j in bids_p:
            if bid_price == j[0]:
                if i[1] == '0':
                    bids_p.remove(j)
                    break
                else:
                    del j[1]
                    j.insert(1, i[1])
                    break
        else:
            if i[1] != "0":
                bids_p.append(i)
    else:
        bids_p.sort(key=lambda price: sort_num(price[0]), reverse=True)
        # print('合并后的bids为:' + str(bids_p) + '，档数为:' + str(len(bids_p)))
    return bids_p


def update_asks(res, asks_p):
    # 获取增量asks数据
    asks_u = res['data'][0]['asks']
    # print('增量数据asks为:' + str(asks_u))
    # print('档数为:' + str(len(asks_u)))
    # asks合并
    for i in asks_u:
        ask_price = i[0]
        for j in asks_p:
            if ask_price == j[0]:
                if i[1] == '0':
                    asks_p.remove(j)
                    break
                else:
                    del j[1]
                    j.insert(1, i[1])
                    break
        else:
            if i[1] != "0":
                asks_p.append(i)
    else:
        asks_p.sort(key=lambda price: sort_num(price[0]))
        # print('合并后的asks为:' + str(asks_p) + '，档数为:' + str(len(asks_p)))
    return asks_p


def sort_num(n):
    if n.isdigit():
        return int(n)
    else:
        return float(n)


def check(bids, asks):
    # 获取bid档str
    bids_l = []
    bid_l = []
    count_bid = 1
    while count_bid <= 25:
        if count_bid > len(bids):
            break
        bids_l.append(bids[count_bid - 1])
        count_bid += 1
    for j in bids_l:
        str_bid = ':'.join(j[0: 2])
        bid_l.append(str_bid)
    # 获取ask档str
    asks_l = []
    ask_l = []
    count_ask = 1
    while count_ask <= 25:
        if count_ask > len(asks):
            break
        asks_l.append(asks[count_ask - 1])
        count_ask += 1
    for k in asks_l:
        str_ask = ':'.join(k[0: 2])
        ask_l.append(str_ask)
    # 拼接str
    num = ''
    if len(bid_l) == len(ask_l):
        for m in range(len(bid_l)):
            num += bid_l[m] + ':' + ask_l[m] + ':'
    elif len(bid_l) > len(ask_l):
        # bid档比ask档多
        for n in range(len(ask_l)):
            num += bid_l[n] + ':' + ask_l[n] + ':'
        for l in range(len(ask_l), len(bid_l)):
            num += bid_l[l] + ':'
    elif len(bid_l) < len(ask_l):
        # ask档比bid档多
        for n in range(len(bid_l)):
            num += bid_l[n] + ':' + ask_l[n] + ':'
        for l in range(len(bid_l), len(ask_l)):
            num += ask_l[l] + ':'

    new_num = num[:-1]
    int_checksum = zlib.crc32(new_num.encode())
    fina = change(int_checksum)
    return fina


def change(num_old):
    num = pow(2, 31) - 1
    if num_old > num:
        out = num_old - num * 2 - 2
    else:
        out = num_old
    return out


class BaseConnect:
    def __init__(self, url, channels, api_key=None, secret_key=None, passphrase=None):
        self.url = url
        self.channels = channels
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

        self.ws: WebSocket = create_connection(self.url)
        self.subscribe_start()

    def run(self):
        while True:
            try:
                res = self.ws.recv()
            except (TimeoutError, WebSocketException):
                try:
                    self.ping()
                except Exception as e:
                    logging.warning(f"连接关闭，正在重连:{e}")
                    self.subscribe_restart()
                continue
            self.handle_data(res)

    def handle_data(self, res):
        pass

    def ping(self):
        self.ws.send('ping')
        res = self.ws.recv()
        print(res)
        assert res == 'pong'

    def subscribe_restart(self):
        self.subscribe_stop()
        self.subscribe_start()

    def subscribe_start(self):
        self.ws: WebSocket = create_connection(self.url)
        sub_param = {"op": "subscribe", "args": self.channels}
        sub_str = json.dumps(sub_param)
        self.ws.send(sub_str)
        print(f"send: {sub_str}")
        res = self.ws.recv()
        print(f"recv: {res}")
        time.sleep(1)

    def subscribe_stop(self):
        self.ws: WebSocket = create_connection(self.url)
        sub_param = {"op": "unsubscribe", "args": self.channels}
        sub_str = json.dumps(sub_param)
        self.ws.send(sub_str)
        print(f"send: {sub_str}")
        res = self.ws.recv()
        print(f"recv: {res}")


class PublicConnect(BaseConnect):
    def __init__(self, channels, *args, **kwargs):
        super(PublicConnect, self).__init__(url="wss://ws.okx.com:8443/ws/v5/public",
                                            channels=channels, *args, **kwargs)

    def handle_data(self, res):
        res = eval(res)
        print(f"{get_local_timestamp()}\t{res}")
        if 'event' in res:
            return
        l = []
        for i in res['arg']:
            if 'books' in res['arg'][i] and 'books5' not in res['arg'][i]:
                # 订阅频道是深度频道
                if res['action'] == 'snapshot':
                    for m in l:
                        if res['arg']['instId'] == m['instrument_id']:
                            l.remove(m)
                    # 获取首次全量深度数据
                    bids_p, asks_p, instrument_id = partial(res)
                    d = {}
                    d['instrument_id'] = instrument_id
                    d['bids_p'] = bids_p
                    d['asks_p'] = asks_p
                    l.append(d)

                    # 校验checksum
                    checksum = res['data'][0]['checksum']
                    # print('推送数据的checksum为:' + str(checksum))
                    check_num = check(bids_p, asks_p)
                    # print('校验后的checksum为:' + str(check_num))
                    if check_num == checksum:
                        print("校验结果为:True")
                    else:
                        print("校验结果为:False，正在重新订阅……")
                        self.subscribe_stop()
                        self.subscribe_start()

                elif res['action'] == 'update':
                    for j in l:
                        if res['arg']['instId'] == j['instrument_id']:
                            # 获取全量数据
                            bids_p = j['bids_p']
                            asks_p = j['asks_p']
                            # 获取合并后数据
                            bids_p = update_bids(res, bids_p)
                            asks_p = update_asks(res, asks_p)

                            # 校验checksum
                            checksum = res['data'][0]['checksum']
                            # print('推送数据的checksum为:' + str(checksum))
                            check_num = check(bids_p, asks_p)
                            # print('校验后的checksum为:' + str(check_num))
                            if check_num == checksum:
                                print("校验结果为:True")
                            else:
                                print("校验结果为:False，正在重新订阅……")
                                self.subscribe_stop()
                                self.subscribe_start()


class PrivateConnect(BaseConnect):

    def __init__(self, channels, *args, **kwargs):
        super(PrivateConnect, self).__init__(url='wss://ws.okx.com:8443/ws/v5/private',
                                             channels=channels, *args, **kwargs)

    def handle_data(self, res):
        print(res)

    def subscribe_start(self):
        self.ws = create_connection(self.url)
        timestamp = str(get_local_timestamp())
        message = timestamp + 'GET' + '/users/self/verify'
        mac = hmac.new(bytes(self.secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        sign = base64.b64encode(mac.digest()).decode("utf-8")
        login_param = {"op": "login", "args": [{"apiKey": self.api_key,
                                                "passphrase": self.passphrase,
                                                "timestamp": timestamp,
                                                "sign": sign}]}
        login_str = json.dumps(login_param)
        self.ws.send(login_str)
        print(f"send: {login_str}")


class TradeConnect(PrivateConnect):
    def __init__(self, *args, **kwargs):
        super(TradeConnect, self).__init__(*args, **kwargs)

    def handle_data(self, res):
        print(res)
