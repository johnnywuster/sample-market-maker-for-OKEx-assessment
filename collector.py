import csv
import sys
from datetime import datetime
from market_maker import bitmex
import settings

connector = bitmex.BitMEX(base_url=settings.BASE_URL, symbol=settings.SYMBOL, apiKey=settings.API_KEY, apiSecret=settings.API_SECRET, shouldWSAuth=False)

count = 1  # max API will allow
query = {
    'reverse': 'true',
    'start': 0,
    'count': count
}

query['symbol'] = settings.SYMBOL

csvwriter = None
preData = None

while True:
    data = connector.ticker_data(symbol=settings.SYMBOL)
    data['timestamp'] = datetime.now()
    data['symbol'] = settings.SYMBOL
    if csvwriter is None:
        csvwriter = csv.DictWriter(sys.stdout, data.keys())
        csvwriter.writeheader()

    if preData is None:
        csvwriter.writerow(data)
        preData = data
    else:
        if preData['last'] != data['last'] or preData['buy'] != data['buy'] or preData['sell'] != data['sell'] or preData['mid'] != data['mid']:
            csvwriter.writerow(data)
            preData = data