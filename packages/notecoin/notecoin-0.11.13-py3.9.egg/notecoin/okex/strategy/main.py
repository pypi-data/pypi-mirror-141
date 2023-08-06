from waitress import serve
from flask import Flask
from notecoin.okex.strategy.strategy1 import Strategy1

app = Flask(__name__)


@app.route('/')
def index():
    return 'success'


Strategy1.register(app, route_base='/')


#serve(app, host="0.0.0.0", port=8884)
app.run(host='0.0.0.0', port=8444)
