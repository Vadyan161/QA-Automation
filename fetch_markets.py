import requests
import json
import os


def fetch_markets(vs_currency='usd', per_page=50):
    """Запрашивает данные по рынкам у CoinGecko. Бросает исключение, если что-то пошло не так."""
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    payload = {'vs_currency': vs_currency, 'per_page': per_page}
    r = requests.get(url, params=payload, timeout=3)
    r.raise_for_status()
    return r.json()

    
def save_json(data, path="data/markets.json"):
    """Сохраняет данные в JSON. Бросает исключение при сбое."""
    os.makedirs(os.path.dirname(path), exist_ok=True) #делается проверка, если такой папки нет, то создает, если есть, то без ошибок продолжает в ней работу
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fetch_prices(coin_ids):
    """Запрашивает данные по монетам у CoinGecko. Бросает исключение, если что-то пошло не так."""
    url =  'https://api.coingecko.com/api/v3/simple/price'
    playload = {'ids':",".join(coin_ids)  ,'vs_currencies':'usd'}
    r=requests.get(url, params=playload, timeout=3)
    r.raise_for_status()
    return r.json()
    # os.makedirs(os.path.dirname(path:="data/prices.json"), exist_ok=True)
    # with open(path, "w", encoding="utf-8") as f:
    #         json.dump(result, f, ensure_ascii=False, indent=2)


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
    try:
        result = fetch_markets(vs_currency, per_page)
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

    if not result:
        print('API вернул пустой список данных')
        return
    else:
        try:
            test = [{'id':'usd', 'image': None}, {'id': 'bitcoin'}, {'id': 'eth', 'image': 1}]
            save_json(result)
            print(f'Сохранено {len(result)} монет')
            for i in top_by_field(result, "market_cap", 5):
                print(i)
            for i in top_by_field(result, "total_volume", 5):
                print(i)
            for i in find_missing_field(result, "image"):
                print(i)
            for i in find_missing_field(test, "image"):
                print(i)
        except OSError as e:
            print(f'Не удалось записать файл: {e}')
            return
        except TypeError as e:
            print(f'Данные нельзя сохранить в JSON: {e}')
            return

    try:
        print(fetch_prices(coin_ids=['bitcoin', 'ethereum', 'tether']))
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

    

if __name__ == "__main__":
    main('usd', 50)

