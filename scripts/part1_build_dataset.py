import csv
from pathlib import Path
import requests
from datetime import datetime, timezone, timedelta
import time

from concurrent.futures import ThreadPoolExecutor
import threading


url = "https://data-api.binance.vision/api/v3/klines"
limit_num = 1000

interval = "1h"

concurrent_request_lock = threading.Semaphore(4) # Add rate limit of 4 threads
write_log_file_lock = threading.Lock() # Add mutex lock for writing file
rate_request_limit_lock = threading.Lock() # Add mutex lock for writing file


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

def write_to_file(filename):

    with write_lock:

def track_requests_for_rate_limit(minute_window_requests, requests_minute_limit):
    now = datetime.now(timezone.utc)
    one_minute_ago = now - timedelta(minutes=1)
    cutoff_timestamp = one_minute_ago.timestamp()

    while len(minute_window_requests)>=100:
        oldest_timestamp = minute_window_requests[0]
        if oldest_timestamp < cutoff_timestamp:
            minute_window_requests.pop(0)
        else:
            break

    active_count = len(minute_window_requests)

    rate_limit_check = active_count < requests_minute_limit

    return rate_limit_check


def get_request_for_symbol(url, symbol, interval, limit_num, time_out, minute_window_requests, requests_minute_limit):
    
    params = {
    "symbol": f"{symbol}",
    "interval": interval,
    "limit": limit_num,
}
    
    with concurrent_request_lock:
        
        now = datetime.now(timezone.utc)

        while True:

            rate_limit_check = track_requests_for_rate_limit(minute_window_requests, requests_minute_limit)     

            if rate_limit_check:

                with rate_request_limit_lock:
                    minute_window_requests.append(now)

                    response_from_server = requests.get(url, params=params,timeout=time_out )
                    response_from_server.raise_for_status()
            
                break
            
            else:
                time.sleep(3)
                continue  
      

if __name__ == "__main__":

    minute_window_requests = []
    requests_minute_limit = 100
    left_index = 0
    time_out = 30

    with ThreadPoolExecutor(max_workers = 10) as Executor:

        for crypto_symbol in crypto_symbols:

            Executor.submit(get_request_for_symbol, url, crypto_symbol, interval, limit_num, time_out, minute_window_requests, requests_minute_limit)











