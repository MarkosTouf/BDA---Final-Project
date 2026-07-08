# Report to Stelios

### How your API downloader works

Requests are mainly handled by get_request_for_symbol function. Installed and imported external requests package which makes http requests to Binance API to get data from url. In multithreaded option get_request function is called by a multithreaded executor of maximum 10 thread workers for 10 calls and 10 symbols to use capacity of threads while other threads have IO waits from http API. But for call of function have placed concurrency and synchronization controls (semaphore 4 threads etc) which will explain below. 
Requests.get gets parameters for url, interval, and timeout and returns json formatted text and through .json() function turning it into python list of lists. Then iterating over it and getting for its list record the elements to populate row dictionary. Rows are then placed in csv file through dict writer, and similarly for log_file, with files protected from concurrency through mutex locks.
response raises status and captures try_exception errors for log.


### How you limited concurrent API requests

Have placed both max server concurrency via *semaphore* - at 4 threads out of total 10 max thread workers initially set in executor - and request rate limit to concurrency. As note request rate limit uses a list or requests which is also a shared resource and critical code section and was protected *via mutex lock*.
4 threads were chosen lower than 10 because on one hand wanted to display the use of semaphore vs the threadpoolexecutor max workers available and on other hand to not be heavy for the url server. But were chosen high enough to have some meaningful speed up compared to serial run.
For rate limit, via rate_limit_function, minute_window_requests holds the requests between now and 1 minute prior and if its *length is greater than 100 program waits and retries*.



### Why the log file needed protection from simultaneous writes
As a note both csv files and log file required protection from simultaneous writes *via mutex locks* to protect from concurrent multithread writes.
Log file is shared resource and read_update_write with file is sensitive with 4 multi_threads hence mutex lock ensures critical update has log_file reliably updated.
Without this protection, two threads writing to the log at the exact same moment could update their file simultaneously, producing a corrupted or unreadable log entry.


### What Dara did to the data and how you cleaned it
Dara used mess_my_data.py to create "dirty" symbol names, missing values, incorrect timestamp or float datatype values, negative trades and volumes as well as negative impossible price ranges (high-low). Duplicates were added.
For cleaning detected and standardized symbol names with stripping from spaces, turning uppercase, removing backslashes. Removed records with missing values. Changed string datatypes to float or timestamp datatypes and errors were turned to null and removed. Impossible negative trades, volumes or price ranges ( high lower than low) led to corrupted rows removed.
As examples the cleaning captured step by step the data_quality issue_specific marked records via the masks. And were removed sequentially while counting per data quality issue category with examples of 213 duplicate rows, 770 invalid numeric rows, 496 missing values for rough total of roughly 1500 corrupted records cleaned.


### Why pandas was used only on a small sample
Pandas is very good structured data analytics tool, and clear one, but does not have inherent Big Data Analytics capability.

It does not have inherent distributed parallel processing, or embedded concurrency and synchronisation management. It is also not as efficient or scalable for big data that is volatile and its analysis is time critical since it is crypto market data.

It also does not have inherent RAM optimisation use for data processing capabilities or resilient data structures if wanting to use it via multithreading.
Hence the use case would add complexity and not embed safety and be slower and riskier.



### Why Zehra asked you to use Spark for the full analytics
Spark is inherently as engine using distributed storage and processing - RAM based - which is efficient and scalable while also providing inherent concurrency protection and fault tolerance.

Spark also allows for both its own coding model for data pipeline easy and logical programming and the use of SQL Queries for clear data retrival and transformation hence has 2 parallel useful ways providing flexibility.

Spark also provides safety with RDDs and forces creation of new dataframes for each step and reference of prior step dataframes for checking.

Its speed, scalability, concurrency protection, flexibility with sql or its methods, clear programming methodology, fault tolerance with backups, and broad application for modern use cases, and its relevance to crypto market data analytics which is time critical analysis with volatile values, which has scalable data price amounts are all relevant to Dara requiring Spark.


### What your final analytics showed

Final analytics via spark showed BTCUSDT as the most active symbol and the most absolutely volative since the proxy for absolute volatility was on price_range and it is the highest price one. Relative volatility could use percentages.
Busiest hour was 14:00 which can be expected due to US market participants being more active while European at peak activity, while June 5th was busiest date which upon research coincided with nonfarm employment data publish.
Quote volume in USDT is more reliable than crypto volume since latter is dependent on unit crypto value and highest quote_volume could have lowest absolute volume.





