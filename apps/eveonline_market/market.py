import numpy
import pandas
from huey import RedisHuey

huey = RedisHuey()


def filter_by(data, key, value):
    return list(filter(lambda d: d[key] == value, data))


def sort_by(data, key, reverse=False):
    return sorted(data, key=lambda i: i[key], reverse=reverse)


def five_percent(raw_data):
    # Ensure we are sorted
    data = sort_by(raw_data, 'price')
    # Total Volume on Market right now
    total_volume = sum(item['volume_remain'] for item in data)
    # 5% of that Market
    target_volume = total_volume * .05

    prices = []
    i = 1
    # Figure out how many orders would buy up 5% of the Market
    while target_volume > 0:
        prices.append(data[i]['price'])
        target_volume -= data[i]['volume_remain']
        i += 1

    # Total cost to buy 5% of the Market
    price_total = sum(item for item in prices)
    # Avg cost to buy 5% of the Market
    price_avg = price_total / len(prices)

    return price_avg


def pandas_stats(raw_data):
    sell = pandas.DataFrame(raw_data)
    sell['min'] = sell.groupby('type_id')['price'].transform('min')
    sell['volume'] = sell.apply(lambda x: 0 if x['price'] > x['min'] * 100 else x['volume_remain'], axis=1)
    sell['cumsum'] = sell.groupby('type_id')['volume'].apply(lambda x: x.cumsum())
    sell['fivepercent'] = sell.groupby('type_id')['volume'].transform('sum') / 20
    sell['lastsum'] = sell.groupby('type_id')['cumsum'].shift(1)
    sell.fillna(0, inplace=True)
    sell['applies'] = sell.apply(
        lambda x: x['volume'] if x['cumsum'] <= x['fivepercent'] else x['fivepercent'] - x['lastsum'], axis=1)

    sellagg = pandas.DataFrame()
    sellagg['weightedAverage'] = sell.groupby('type_id').apply(lambda x: numpy.average(x.price, weights=x.volume))
    sellagg['max'] = sell.groupby('type_id')['price'].max()
    sellagg['min'] = sell.groupby('type_id')['price'].min()
    sellagg['stddev'] = sell.groupby('type_id')['price'].std()
    sellagg['median'] = sell.groupby('type_id')['price'].median()
    sellagg.fillna(0.01, inplace=True)
    sellagg['volume'] = sell.groupby('type_id')['volume'].sum()
    sellagg['orderCount'] = sell.groupby('type_id')['price'].count()
    sellagg['percentile'] = sell.groupby('type_id').apply(lambda x: numpy.average(x.price, weights=x.applies))
    return sellagg.to_dict('records')[0]


def every_three_minutes():
    print('This task runs every three minutes')
