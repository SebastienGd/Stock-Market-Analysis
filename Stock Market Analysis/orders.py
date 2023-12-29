class Order:
    def __init__(self) -> None:
        self.buy_price = None
        self.sell_price = None

    def buy(self, price):
        self.buy_price = price

    def sell(self, price):
        self.sell_price = price
        return self.sell_price - self.buy_price
