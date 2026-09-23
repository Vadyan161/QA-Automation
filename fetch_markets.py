import requests
import json
import os


class MarketDataClient:
    def __init__(self, base_url= 'https://api.coingecko.com/api/v3', timeout=10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "MyCustomApp/1.0"
        })


    def _get(self, path, params= None):
        url = self.base_url+path
        r = self.session.get(url, params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()


    def fetch_markets(self, vs_currency='usd', per_page=50):
        payload = {'vs_currency':vs_currency, 'per_page':per_page}
        return self._get(path=f'/coins/markets', params = payload)


    def fetch_prices(self, coin_ids):
        # # os.makedirs(os.path.dirname(path:="data/prices.json"), exist_ok=True)
        # # with open(path, "w", encoding="utf-8") as f:
        # #         json.dump(result, f, ensure_ascii=False, indent=2)
        payload = {'ids':",".join(coin_ids)  ,'vs_currencies':'usd'}
        return self._get(f'/simple/price', params = payload)


    def get_coins(self):
        coins_raw = [Coin(item) for item in self.fetch_markets()]
        return coins_raw

class Coin:
    def __init__ (self, raw: dict):
        self.id = raw.get('id')
        self.symbol = raw.get('symbol')
        self.name = raw.get('name')
        self.price = raw.get('current_price')
        self.market_cap = raw.get('market_cap')


    def is_valid (self):
        flag = False
        if all(v is not  None for v in (self.id, self.symbol, self.name, self.price)):
            if self.price > 0:
                flag = True
        return flag
            

        

def save_json(data, path="data/markets.json"):
    """Сохраняет данные в JSON. Бросает исключение при сбое."""
    os.makedirs(os.path.dirname(path), exist_ok=True) #делается проверка, если такой папки нет, то создает, если есть, то без ошибок продолжает в ней работу
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def top_by_field(markets, field, n):
    """Отсортировывает список словарей по заданному полю и возвращет список словарей"""
    sorted_data = sorted(markets, key=lambda x: x[field], reverse=True)
    print(f'\nТоп {n} монет по полю {field}:')
    d = list()
    for i in sorted_data[:n]:
        # print(i.get('id'), i.get(field))
        temp_dict= {i.get('id'): i.get(field)}
        d.append(temp_dict)
    return d


def find_missing_field(markets, field):
    """Возвращает монеты у которых нехватает поля или оно не заполнено"""
    d = []
    print(f'\nМонеты у которых нет поля {field}:')
    for i in markets:
        if field not in i:
            # print(f'{i[id]} - нет поля {field}')
            temp_dict={'id': i['id']}
            d.append(temp_dict)
        else:
            if i[field] is None:
                temp_dict={'id': i['id'], field:i[field]}
                d.append(temp_dict)
    return d


def main(vs_currency='usd', per_page=10):
    client = MarketDataClient()
    try:
        markets = client.fetch_markets(vs_currency, per_page)
    except requests.exceptions.JSONDecodeError:
        print('Не удалось разобрать ответ сервера как JSON')
        return
    except requests.exceptions.HTTPError as e:
        print(f'Сервер вернул ошибку: {e}')
        return
    except requests.exceptions.ConnectionError:
        print('Нет соединения с сервером — проверь интернет или путь до сервера')
        return
    except requests.exceptions.Timeout:
        print('Сервер не ответил вовремя')
        return
    except requests.exceptions.RequestException as e:
        print(f'Непредвиденная ошибка запроса: {e}')
        return

    if not markets:
        print('API вернул пустой список данных')
        return
    else:
        try:
            save_json(markets)
            print(f'Сохранено {len(markets)} монет')
            for i in top_by_field(markets, "market_cap", 5):
                print(i)
            for i in top_by_field(markets, "total_volume", 5):
                print(i)
        except OSError as e:
            print(f'Не удалось записать файл: {e}')
            return
        except TypeError as e:
            print(f'Данные нельзя сохранить в JSON: {e}')
            return

    try:
        prices=client.fetch_prices(coin_ids=['bitcoin', 'ethereum', 'tether'])
        for  k, v in prices.items():
            print(f'{k}:{v}')
    except requests.exceptions.JSONDecodeError:
        print('Не удалось разобрать ответ сервера как JSON')
        return
    except requests.exceptions.HTTPError as e:
        print(f'Сервер вернул ошибку: {e}')
        return
    except requests.exceptions.ConnectionError:
        print('Нет соединения с сервером — проверь интернет или путь до сервера')
        return
    except requests.exceptions.Timeout:
        print('Сервер не ответил вовремя')
        return
    except requests.exceptions.RequestException as e:
        print(f'Непредвиденная ошибка запроса: {e}')
        return

    # coins = client.get_coins()
    coins = [Coin(item) for item in markets]
    count = 0
    for c in coins:
        if not c.is_valid():
            count += 1
    print(f'Невалидных монет: {count}')
    

if __name__ == "__main__":
    main('usd', 50)

