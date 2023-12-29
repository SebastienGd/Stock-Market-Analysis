from polygon import RESTClient
import csv

client = RESTClient(api_key="d2YVvfDXc7194T3DfmkehnCAT57IUFV7")


class Data:
    def __init__(
        self, ticker, timespan, start_date, end_date, multiplier, sort, limit
    ) -> None:
        self.ticker = ticker
        self.timespan = timespan
        self.start_date = start_date
        self.end_date = end_date
        self.multiplier = multiplier
        self.sort = sort
        self.limit = limit

    def get_data(self):
        candles = client.get_aggs(
            ticker=self.ticker,
            timespan=self.timespan,
            from_=self.start_date,
            to=self.end_date,
            multiplier=self.multiplier,
            sort=self.sort,
            limit=self.limit,
        )
        return [candle for candle in candles]


data = Data(
    ticker="NIO",
    timespan="minute",
    start_date="2022-01-01",
    end_date="2022-02-01",
    multiplier=5,
    sort="asc",
    limit=50000,
).get_data()


with open("data.csv", "a") as f:
    writer = csv.writer(f, delimiter=",")
