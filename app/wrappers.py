import requests
from datetime import datetime

class StockTicker:
    def __init__(self, ticker, tradeDate, expirDate, strikePrice, stockPrice, callVolume, putVolume):
        self.ticker = ticker
        self.tradeDate = tradeDate
        self.expirDate = expirDate
        self.strikePrice = strikePrice
        self.stockPrice = stockPrice
        self.callVolume = callVolume
        self.putVolume = putVolume

    def __str__(self):
        return f"Stock Ticker: {self.ticker}"

    def __repr__(self):
        return f"<Stock Ticker | {self.ticker}>"

    def to_dict(self):
        return {'ticker': self.ticker, 'tradeDate': self.tradeDate, 'expirDate': self.expirDate}


class Orats:
    def __init__(self):
        self.base_path = "https://api.orats.io/datav2/strikes/options"
        self.api_key = "df2bf29a-22cb-4567-8750-8ad2a2938525"

    def get_ticker_info(self, ticker, expirDate, strike):
        url = self.base_path + "?token=" + self.api_key + "&ticker=" + ticker + "&expirDate=" + expirDate + "&strike=" + strike
        r = requests.get(url)
        response = r.json()
        response = response['data'][0]
        ticker = response['ticker']
        tradeDate = response['tradeDate']
        expirDate = response['expirDate']
        strikePrice = response['strike']
        stockPrice = response['stockPrice']
        callVolume = response['callVolume']
        putVolume = response['putVolume']
        data = StockTicker(ticker, tradeDate, expirDate, strikePrice, stockPrice, callVolume, putVolume)
        return data