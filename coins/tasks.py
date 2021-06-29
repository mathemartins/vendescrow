import requests
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.forms import model_to_dict

from coins.models import CoinGecko, CoinCMC

channel_layer = get_channel_layer()


@shared_task
def get_coins_data_from_coingecko():
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    data = requests.get(url=url).json()
    print(data)

    coins = []

    for coin in data:
        obj, created = CoinGecko.objects.get_or_create(symbol=coin['symbol'])
        obj.name = coin['name']
        obj.symbol = coin['symbol']

        if obj.price > coin['current_price']:
            state = 'fail'
        elif obj.price == coin['current_price']:
            state = 'same'
        elif obj.price < coin['current_price']:
            state = 'raise'

        obj.price = coin['current_price']
        obj.rank = coin['market_cap_rank']
        obj.image = coin['image']

        obj.save()
        new_data = model_to_dict(obj)
        new_data.update({'state': state})

        coins.append(new_data)

    async_to_sync(channel_layer.group_send)('coins', {'type': 'send_new_data', 'text': coins})


def get_coins_data_from_coinmarket_cap():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {"X-CMC_PRO_API_KEY": "b9bce1cc-01ad-44d0-bc4e-e1421245ec0f", "Content-Type": "application/json"}
    data = requests.request("GET", url, headers=headers).json()

    for coin in data:
        obj, created = CoinCMC.objects.get_or_create(symbol=coin['symbol'])
        obj.name = coin['name']
        obj.symbol = coin['symbol']
        obj.quote.usd.price = coin['quote']['USD']['price']
        obj.quote.usd.volume_24h = coin['quote']['USD']['volume_24h']
        obj.quote.usd.percent_change1h = coin['quote']['USD']['percent_change_1h']
        obj.quote.usd.percent_change24h = coin['quote']['USD']['percent_change_24h']
        obj.quote.usd.percent_change7d = coin['quote']['USD']['percent_change_7d']
        obj.quote.usd.percent_change30d = coin['quote']['USD']['percent_change30d']
        obj.quote.usd.percent_change60d = coin['quote']['USD']['percent_change60d']
        obj.quote.usd.percent_change90d = coin['quote']['USD']['percent_change90d']
        obj.quote.usd.market_cap = coin['quote']['usd']['market_cap']
        obj.quote.usd.last_updated = coin['quote']['usd']['last_updated']
        obj.number_of_market_pairs = coin['num_market_pairs']
        obj.date_added = coin['date_added']
        obj.max_supply = coin['max_supply']
        obj.circulating_supply = coin['circulating_supply']
        obj.total_supply = coin['total_supply']
        obj.platform = coin['platform']
        obj.cmc_rank = coin['cmc_rank']
        obj.last_updated = coin['last_updated']

        obj.save()
