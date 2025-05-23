import time, hmac, hashlib, requests, json, os

class BitgetClient:
    def __init__(self):
        self.api_key = os.getenv("BITGET_API_KEY")
        self.api_secret = os.getenv("BITGET_API_SECRET")
        self.passphrase = os.getenv("BITGET_API_PASSPHRASE")
        self.base_url = "https://api.bitget.com"

    def _get_headers(self, method, path, body=""):
        timestamp = str(int(time.time() * 1000))
        prehash = timestamp + method.upper() + path + body
        sign = hmac.new(self.api_secret.encode(), prehash.encode(), hashlib.sha256).hexdigest()

        return {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": sign,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json"
        }

    def place_order(self, symbol, side, size, price):
        path = "/api/spot/v1/trade/orders"
        url = self.base_url + path
        body = json.dumps({
            "symbol": symbol,
            "side": side,
            "orderType": "limit",
            "price": str(price),
            "size": str(size),
        })
        headers = self._get_headers("POST", path, body)
        res = requests.post(url, headers=headers, data=body)
        return res.json()

    def get_prices(self, symbols):
        prices = {}
        for symbol in symbols:
            res = requests.get(f"{self.base_url}/api/spot/v1/market/ticker?symbol={symbol}")
            prices[symbol] = float(res.json()["data"]["close"])
        return prices
