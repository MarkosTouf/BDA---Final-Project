import csv
from pathlib import Path
import requests

from concurrent.futures import ThreadPoolExecutor
import threading


domain = "https://data-api.binance.vision/api/v3/klines"
limit_num = 1000

rate_limit_lock = threading.Semaphore(10) # Add rate limit of 10 threads
write_lock = threading.lock() # Add mutex lock for writing file

crypto_symbols = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "ADAUSDT",
    "DOGEUSDT",
    "AVAXUSDT",
    "LINKUSDT",
    "DOTUSDT"
]

def get_for_symbol(url, symbol, limit_num):
    
    params = {
    "symbol": f"{symbol}",
    "interval": "1h",
    "limit": limit_num,
}
    
    response_from_server = requests.get(url, params=params,time_out=30 )
    response_from_server.raise_for_status()


if __name__ = "main":

    with ThreadPoolExecutor(max_workers = 10) as Executor:

        for crypto_symbol in crypto_symbols:











