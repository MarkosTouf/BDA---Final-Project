
    import csv
    from pathlib import Path
    import requests
    from datetime import datetime, timezone, timedelta
    import time
    import os

    from concurrent.futures import ThreadPoolExecutor
    import threading


    url = "https://data-api.binance.vision/api/v3/klines"
    limit_num = 1000

    interval = "1h"

    concurrent_request_lock = threading.Semaphore(4) # Add rate limit of 4 threads
    write_log_file_lock = threading.Lock() # Add mutex lock for writing log file
    write_csv_file_lock = threading.Lock() # Add mutex lock for writing csv file
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

    def write_to_csv_file(csv_file_path,row):

        # file_path.parent.mkdir(parents=True, exist_ok=True) # I have it in main

        with write_csv_file_lock:
            
            with open(csv_file_path, "a", newline="", encoding="utf-8") as csv_file:
                file_is_empty = not os.path.exists(csv_file_path) or os.path.getsize(csv_file_path) == 0
                dict_writer = csv.DictWriter(csv_file, fieldnames = row.keys())

                if file_is_empty:
                    dict_writer.writeheader()

                dict_writer.writerow(row)

    def write_to_log_file(log_file_path, message):

        with write_log_file_lock:

            with open(log_file_path, "a", newline="", encoding="utf-8") as log_file:
                now_time = datetime.now(timezone.utc)
                log_row = f"{now_time}| {message}\n"
                
                log_file.write(log_row)   

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


    def get_request_for_symbol(url, symbol, interval, limit_num, time_out, minute_window_requests, requests_minute_limit, csv_file_path, log_file_path):
        
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

                        

                    try:

                        request_start_log_message = f"START request symbol= {symbol} interval= {interval} limit= {limit_num}"
                        
                        write_to_log_file(log_file_path, request_start_log_message)

                        num_records = 0

                        request_start_time = time.perf_counter()

                        response_from_server = requests.get(url, params=params,timeout=time_out )
                        response_from_server.raise_for_status()

                        request_end_time = time.perf_counter()

                        for record in response_from_server.json():

                            row = {
                                    "symbol": f"{symbol}",
                                    "interval": f"{interval}",
                                    "open_time": datetime.fromtimestamp(record[0]/1000, tz=timezone.utc),
                                    "open": record[1],
                                    "high": record[2],
                                    "low": record[3],
                                    "close": record[4],
                                    "volume": record[5],
                                    "close_time": datetime.fromtimestamp(record[6]/1000, tz=timezone.utc),
                                    "quote_volume": record[7],
                                    "trade_count": record[8],
                                    "taker_buy_base_volume":record[9],
                                    "taker_buy_quote_volume":record[10]
                            }

                            num_records += 1

                            write_to_csv_file(csv_file_path, row)                        
                    
                        request_end_log_message = f"END request symbol= {symbol} records= {num_records}"
                        
                        write_to_log_file(log_file_path, request_end_log_message)

        
                    except requests.exceptions.RequestException as err:
                        print(f"CRITICAL: A network connection error occurred: {err}. CSV was not updated.")

                        request_end_error_message = f"ERROR request symbol= {symbol} records= {num_records} error_message: {err}"

                        write_to_log_file(log_file_path, request_end_error_message)
                        
                
                    break
                
                else:
                    time.sleep(3)
                    continue

        return (request_start_time, request_end_time, symbol)

    def create_csv_comparison_row(method, time_duration, num_records, note):
        
        row_csv_comparison = {

            "method": f"{method}",
            "seconds": f"{time_duration}",
            "records": f"{num_records}",
            "note":  f"{note}"
        }

        return row_csv_comparison

    def take_total_row_records(file_path):
        
        line_count = 0
        
        with open(file_path, "r", encoding="utf-8") as file:

            for line in file:
                line_count += 1

        total_records_count = line_count - 1 #To remove the header from count

        return total_records_count
        

    if __name__ == "__main__":

        minute_window_requests_multithreaded = []
        minute_window_requests_serial = []
        requests_minute_limit = 100
        time_out = 30
        csv_file_path = Path("data/clean/clean_market_data.csv")
        csv_file_path_serial = Path("data/clean/clean_market_data_serial.csv")
        log_file_path = Path("results/api_download.log")
        log_file_path_serial = Path("results/api_download_serial.log")
        run_comparison_file_path = Path("results/runtime_comparison.csv")

        csv_file_path.parent.mkdir(parents=True, exist_ok=True)
        open(csv_file_path,"w").close() # Clear the clean data file if it exists

        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        open(log_file_path,"w").close() # Clear the clean data file if it exists

        csv_file_path_serial.parent.mkdir(parents=True, exist_ok=True)
        open(csv_file_path_serial, "w").close()
        
        # ---- For multithreading run: ---

        start_time_run_multithread = time.perf_counter()

        with ThreadPoolExecutor(max_workers = 10) as Executor:

            for crypto_symbol in crypto_symbols:

                Executor.submit(get_request_for_symbol, url, crypto_symbol, interval, limit_num, time_out, minute_window_requests_multithreaded, requests_minute_limit, csv_file_path, log_file_path)

        end_time_run_multithread = time.perf_counter()

        # time taken by csv and log write is considered very small relative to the API IO and download step and kept and
        # time comparison to serial verifies serial is 2.15 or so slower than multithreaded with 4 threads

        run_execution_duration_multithread =  end_time_run_multithread - start_time_run_multithread

        # --- For serial run: ---

        start_time_run_serial = time.perf_counter()

        for crypto_symbol in crypto_symbols:
            get_request_for_symbol(url, crypto_symbol, interval, limit_num, time_out, minute_window_requests_serial, requests_minute_limit, csv_file_path_serial, log_file_path_serial)
        
        end_time_run_serial = time.perf_counter()

        run_execution_duration_serial = end_time_run_serial - start_time_run_serial


        multithread_records_count = take_total_row_records(csv_file_path)

        print(f"Total records: {multithread_records_count}")
        record_count_check = "passed" if multithread_records_count == 10000 else "failed"
        print(f"Record count check: {record_count_check}")

        serial_records_count = take_total_row_records(csv_file_path_serial)

        csv_write_log_message = f"WROTE csv={csv_file_path} records = {multithread_records_count}"

        write_to_log_file(log_file_path, csv_write_log_message)  

        multithread_comparison_note = "downloaded several symbols at the same time"
        serial_comparison_note = "downloaded the ten symbols one after another"

        run_comparison_row_multithreading = create_csv_comparison_row("multithreading", run_execution_duration_multithread, multithread_records_count, multithread_comparison_note)
        run_comparison_row_serial = create_csv_comparison_row("serial", run_execution_duration_serial, serial_records_count, serial_comparison_note)

        write_to_csv_file(run_comparison_file_path, run_comparison_row_multithreading)
        write_to_csv_file(run_comparison_file_path, run_comparison_row_serial)
















