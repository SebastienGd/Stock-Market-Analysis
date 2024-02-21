from data import *
from orders import *


class Hammer:
    def __init__(self, data: Data, target: int, p_l_ratio: int):
        self.data = data.get_data()
        self.target = target
        self.p_l_ratio = p_l_ratio
        self.trend = None
        self.candles = []
        self.order = Order()
        self.holding = False

    def find_trend(self):
        highest_or_lowest = []
        for candle in self.data:
            if not highest_or_lowest:
                highest_or_lowest.append(candle)
            else:
                if candle.close > highest_or_lowest[0].open:
                    highest_or_lowest[0] = candle
                    self.trend = "Ascending"
                elif candle.close < highest_or_lowest[0].open:
                    highest_or_lowest[0] = candle
                    self.trend = "Descending"

    def execute_orders(self, candle):
        sell_price = (candle.high - candle.low) / 2 + candle.low
        if (
            self.order.buy_price * self.target + self.order.buy_price < candle.high
            and self.order.buy_price * self.target + self.order.buy_price > candle.low
        ):
            self.holding = False
            return self.order.sell(sell_price)

        elif (
            self.order.buy_price - self.order.buy_price * self.target / 2 < candle.high
            and self.order.buy_price - self.order.buy_price * self.target / 2
            > candle.low
        ):
            self.holding = False
            return self.order.sell(sell_price)

    def strategy(self):
        orders = []
        highest_or_lowest = []
        for candle in self.data:
            # Finding the trend
            if not highest_or_lowest:
                highest_or_lowest.append(candle)
            else:
                if candle.close > highest_or_lowest[0].open:
                    highest_or_lowest[0] = candle
                    self.trend = "Ascending"
                elif candle.close < highest_or_lowest[0].open:
                    highest_or_lowest[0] = candle
                    self.trend = "Descending"
            # Finding upwards hammer candles
            if not self.holding:
                if not self.candles:
                    self.candles.append(candle)
                else:
                    if candle.open > candle.close:
                        self.candles.append(candle)
                        if (
                            len(self.candles) > 3
                            and self.trend == "Descending"
                            and (candle.high - candle.low)
                            / (candle.open - candle.close)
                            >= 4
                        ):
                            self.order.buy(candle.close)
                            self.holding = True
                    else:
                        self.candles = []
            else:
                if self.execute_orders(candle) != None:
                    orders.append(self.execute_orders(candle))

        return orders


class MovingAverageCrossover:
    def __init__(self, data=None, short_window=20, long_window=50):
        self.data = data.get_data()
        self.short_window = short_window
        self.long_window = long_window
        self.order = Order()
        self.holding = False

    def strategy(self):
        orders = []
        starting_short = self.data[
            self.long_window - self.short_window : self.long_window
        ]
        starting_long = self.data[: self.long_window]

        for candle in self.data[self.long_window :]:
            starting_short.append(candle)
            starting_short = starting_short[1:]
            starting_long.append(candle)
            starting_long = starting_long[1:]
            m_a_short = (
                sum(candle_close.close for candle_close in starting_short)
                / self.short_window
            )
            m_a_long = (
                sum(candle_close.close for candle_close in starting_long)
                / self.long_window
            )
            if m_a_short > m_a_long and not self.holding:
                self.order.buy(candle.close)
                self.holding = True
            elif m_a_short < m_a_long and self.holding:
                orders.append(self.order.sell(candle.close))
                self.holding = False
        return orders
