# Reflections

## 1. What was the hardest technical problem in this project and how did you overcome it?

My hardest technical problem was the use of semaphore for API requests and mutex locks for csv and log files as well as rate limit dynamic requests list.
One issue was that multi-processing was not working properly and upon observing downloads and log file during checks was observed that the real run executed was effectively sequential due to mutex lock being bottleneck in the multithreading.
After moving mutex the 4 threads were correctly running concurrently and the log verified their start and end API request runs to prove 4 are in progress at each time. 
Secondary difficulties were uses of Pandas masks, Pandas dataframe vs series, and in Spark usage of dataframe vs row for taking values.



## 2. Did multithreading make the API download faster or safer? Explain.

Multithreading was faster than serial with a rough 9.5 sec to 20.5 sec relative comparison.
Hence it made the API download function faster by allowing 4 threads to send requests and a thread sending or receiving while other thread is waiting for response or having some IO network wait.

Multithreading introduces risk due to being heavier for server and due to updating shared resources (files and list) but was risk managed through semaphore for server and mutex locks for files and list. Multithreading has the risk of race condition and of reading and writing on a file while in between other thread has updated after reading the file hence potentially introducing unreliable update. Mutex locks managed the risk via blocking multithreading from those critical section code steps.

## 3. What did pandas make easier?

Pandas makes it easier to see dataset in a tabular manner.
Also to filter by given single or composite conditions or masks.
Masks were very useful because they were dataframes or mostly series with boolen values which then either could be used to filter dataframe or to combine logically the masks to get records as was done in "invalid numeric conversion only" mask where "original missing mask" was logically removed ( mask a ~ mask b) from "all post conversion nulls mask" to get 
Similarly for impossible negative values masks, used logical OR expressions on the negative volumes or negative trades masks or negative ranges ( high - low negative which captured high lower than low) to get a total set mask of impossible values.
The dataframe to boolean dataframe to mask calculations were very useful.
Then masks could be used to get records via filter or record counts on the masks.
And new masks to be created from prior via logical expressions.
Pandas also allosed to easily update dataframe in place, for example to replace a null value with "missing label" or with any value.
It was easy to integrate with Jupyter notebook as well.

## 4. What did Spark make easier?
Spark makes it easier to have multistep data pipeline changes and analytics. 
In the data pipeline steps, It also provides flexibility on using its own data pipeline tools or embeding sql queries.
Introducing embedded sql queries allowed to leverage existing knowledge of querying data and getting case relevant sql results from the views.
Also, its code structure, using with_column, join, filter, select code structure allowed to work on a dataframe in kind of modular clear code format and hence was clear to both build and to update prior code to rebuild new dataframe and see refreshed results.
Overall, it forced to create new dataframes in each step which made easy to transparently see prior steps. And due to RDDs to have the safety of knowing that it is efficient but also the data transformations of each step are safely updated and reliable.
On Summary report steps, groupBy and aggregation logic was separate and clear to create new aggregated dataframes at the granularity required for aggregated analyses and summaries. Windows were very useful to allow application of functions and dense_rank for rankings without changing granularity.
Spark was a little faster compared to Pandas to "refresh all".
Via Google Collab, post setup, through "copy to Github" menu option it was a little faster to make commits with messages to git branch.

## 5. What would you improve if you had more time?

I would check that close price of one hour interval matches the open price of the next.
Would isolate time measured in team 1 to only count download step although in present time measurement noted that file writting is relatively small time wise to network API IO requests and downloads.
Would compare semaphore options of 4 or other allowed multithreading to set the semaphore parameter.
Could add more refactoring via functions and one function definition per one program function.
Would check if so many files updated and using disk could be improved through more RAM based data structures.
Would not remove roughly 1400 records and would replace values of records with volume and trade values from prior or following records which would locally at those busy-ness periods make sense without impacting the averages too much but also reflecting trade and volume counts of those periods.
Would create visual graphs to have a rapid reflection of activity, volatility and prices on the days and intervals being checked after replacing the missing values to have continuity of the intervals with the combined focus of logical locally values which dont impact averages too much.
Would create time comparisons of pandas vs spark analysis to show and prove the advantages of spark processing.
Would attempt to improve time and space complexity of code.
Would add relative volatility metrics on symbols to showcase percentage price changes instead of only absolute volatility of price change.
