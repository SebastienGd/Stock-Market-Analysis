from data import *
from strategy import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
import csv


class Simulation:
    def __init__(self, strategy) -> None:
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
        return f"Profits: {total_profits}, Winrate: {win_rate}, Number of trades: {len(results)}"

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


# with open("data.csv", "a") as f:
#     writer = csv.writer(f, delimiter=",")
#     dates = Simulation.change_dates_by_a_month("2022-05-01", "2022-09-01")
#     i = 0
#     while i < len(dates) - 1:
#         start_date = dates[i]
#         end_date = dates[i + 1]
#         data = Data(
#             ticker="NIO",
#             timespan="minute",
#             start_date=start_date,
#             end_date=end_date,
#             multiplier=5,
#             sort="asc",
#             limit=50000,
#         )
#         print(dates[i])
#         writer.writerow([f"De {start_date} à {end_date}", data])
#         i += 1
