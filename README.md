# Fansite-analytics-challenge

This project is to perform basic analytics on a server log file, provide useful metrics and implement basic security measures

## Installation

Required packages:
1. numpy==1.11.3
2. pandas==0.19.2

## Usage


1. list the top 10 most active IP with visit counts and write into hosts.txt

2. Identify the top 10 resources on the site 
   
3. List the top 10 busiest 60-min periods

4. Detect patterns of the failed login attempts from the same IP over 20 sec so that all further attempts to the site can be blocked for 5 min.


## Method

-- read the log.txt file and convert it into a dataframe (read_log.py)

-- feature 1: count index frequency and write into an output file with descending order (most_active_hosts.py)

-- feature 2: convert "bytes" into int, fill the null bytes, "-", into 0
              group and sum the "Request", sort in a descending order and show the first 10 
              (most_bandwidth_resources.py)

-- feature 3: group frequency of timestamp, sort index in descending order; calculate the cummulated sum at each second;
              if total time in the log file is less than 3600, the frequency of the time between 3600sec and max time is set to zero;
              total = cumsum of the 3600th time-cumsum of the 1st time+ freq of 3600th time, sort in decending way  
              (busiest_period.py)

-- feature 4: detect potential blocked host by detecting the first 304, 401 httpcodes;
              check the number of failue counts in the next 20 sec
              if blocked, blocked all attempts in the next 5min
              if not blocked, reset to initial state
