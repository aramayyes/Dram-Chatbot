class ExchangeRate:
    """Represents AMD exchange rate for both buy and sell types."""

    def __init__(self, cur: str, buy: str = None, sell: str = None):
        self.cur = cur
        self.buy = buy
        self.sell = sell
