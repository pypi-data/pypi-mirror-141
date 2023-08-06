from notecoin.okex.websocket.channel import PublicChannel
from notecoin.okex.websocket.connect import PublicConnect

connect = PublicConnect(channels=[PublicChannel.public_tickers("SHIB-USDT").to_json()])
connect.run()
