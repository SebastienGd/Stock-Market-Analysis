from data import *
from strategy import *
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Simulation:
    def __init__(self, strategy=Hammer) -> None:
        self.strategy = strategy

    def run_simulation(self):
        results = self.strategy.strategy()
        total_profits = 0

        positive_trades_count = 0
        for result in results:
            total_profits += result
            if result >= 0:
                positive_trades_count += 1

        win_rate = positive_trades_count / len(results) * 100
        return total_profits, win_rate, len(results)

    @staticmethod
    def change_dates_by_a_month(start_date_str, end_date_str):
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        current_date = start_date
        all_dates = []

        while current_date <= end_date:
            all_dates.append(current_date.strftime("%Y-%m-%d"))
            current_date += relativedelta(months=1)

        return all_dates


aui = Simulation(
    Hammer(
        Data(
            ticker="NIO",
            timespan="minute",
            start_date="2022-01-01",
            end_date="2022-02-28",
            multiplier=5,
            sort="asc",
            limit=50000,
        ),
        0.5 / 100,
        2,
    ),
)


print(aui.run_simulation())
