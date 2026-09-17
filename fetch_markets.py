import requests
import json
import os

# payload = {'vs_currency':'usd', 'order':'market_cap_desc', 'per_page':50, 'page':1}


def fetch_markets(vs_currency='usd', per_page=50):
    """Запрашивает данные у CoinGecko. Бросает исключение, если что-то пошло не так."""
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
            save_json(result)
            print(f'Сохранено {len(result)} монет')
        except OSError as e:
            print(f'Не удалось записать файл: {e}')
            return
        except TypeError as e:
            print(f'Данные нельзя сохранить в JSON: {e}')
            return

if __name__ == "__main__":
    main('usd', 10)

