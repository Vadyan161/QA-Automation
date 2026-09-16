import requests
import json
import os

payload = {'vs_currency':'usd', 'order':'market_cap_desc', 'per_page':50, 'page':1}

try:
    r = requests.get('https://api.coingecko.com/api/v3/coins/markets', params=payload, timeout=3)
    r.raise_for_status()
    markets =r.json()
    print('Данные получены успешно!')
    os.makedirs("data", exist_ok=True)  #делается проверка, если такой папки нет, то создает, если есть, то без ошибок продолжает в ней работу
    with open("data/markets.json", "w", encoding="utf-8") as f:
        json.dump(markets, f, ensure_ascii=False, indent=2)
    print(f'Сохранено {len(markets)} монет, ниже три самых популярных:{[ids["id"] for ids in markets[0:3]]}')

except requests.exceptions.HTTPError as http_err:
    # Перехватываем ошибки сервера или неверных URL (4xx, 5xx)
    print(f"Произошла HTTP ошибка: {http_err}")
    print(f"Статус-код: {r.status_code}")

except requests.exceptions.ConnectionError as conn_err:
    # Перехватываем проблемы с сетью (например, пропал интернет)
    print(f"Ошибка соединения: {conn_err}")

except requests.exceptions.Timeout as timeout_err:
    # Перехватываем ошибку превышения времени ожидания
    print(f"Истекло время ожидания: {timeout_err}")

except requests.exceptions.RequestException as err:
    # Базовое исключение для любых других непредвиденных ошибок requests
    print(f"Что-то пошло не так: {err}")



