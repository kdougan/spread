import requests


class SymbolListException(Exception):
    pass


def get_symbol_list():
    uri = 'https://fapi.binance.com/fapi/v1/ticker/price'
    response = requests.get(uri)
    if response.status_code != 200:
        raise SymbolListException('get_symbol_list')
    data = response.json()
    return [x['symbol'].lower() for x in data if 'USDT' in x['symbol']]
