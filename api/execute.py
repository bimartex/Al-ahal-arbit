from utils.bitget_api import BitgetClient
import json

def handler(request, response):
    client = BitgetClient()

    if request.method == "POST":
        prices = client.get_prices(["BTCUSDT", "ETHUSDT", "ETHBTC"])

        usdt_to_btc = 1 / prices["BTCUSDT"]
        btc_to_eth = 1 / prices["ETHBTC"]
        eth_to_usdt = prices["ETHUSDT"]

        final_amount = usdt_to_btc * btc_to_eth * eth_to_usdt
        profit = (final_amount - 1) * 100
        executed = False

        if profit > 0.2:
            client.place_order("BTCUSDT", "buy", 0.001, prices["BTCUSDT"])
            client.place_order("ETHBTC", "buy", 0.015, prices["ETHBTC"])
            client.place_order("ETHUSDT", "sell", 0.015, prices["ETHUSDT"])
            executed = True

        return response.json({
            "profit_percentage": profit,
            "final_amount": final_amount,
            "opportunity": profit > 0.2,
            "executed": executed
        })

    return response.status(405).json({"error": "Method Not Allowed"})
