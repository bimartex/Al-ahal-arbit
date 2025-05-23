from utils.bitget_api import BitgetClient
import json

def handler(request, response):
    client = BitgetClient()
    prices = client.get_prices(["BTCUSDT", "ETHUSDT", "ETHBTC"])

    usdt_to_btc = 1 / prices["BTCUSDT"]
    btc_to_eth = 1 / prices["ETHBTC"]
    eth_to_usdt = prices["ETHUSDT"]

    final_amount = usdt_to_btc * btc_to_eth * eth_to_usdt
    profit = (final_amount - 1) * 100

    return response.json({
        "profit_percentage": profit,
        "final_amount": final_amount,
        "opportunity": profit > 0.2
    })
