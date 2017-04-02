import pandas as pd
import numpy as np
from datetime import timedelta


def get_busiest_period(df, output_path, n=10):

	freq = df['Timestamp'].value_counts().sort_index(ascending=False) # group frequency of timestamp, sort index in ascending order; type: series

	lag = freq.index + timedelta(seconds=3600) #set 3600 second
	intervals = np.searchsorted(freq.index.astype(np.int64), lag.astype(np.int64)) #find the corresponding time point after 3600sec in the original frequency 
	cummulated_freq = freq.cumsum() # calculate the cummulated sum at each second

	cummulated_freq_by_interval = pd.Series([cummulated_freq[idx] if idx in cummulated_freq.index else 0 for idx in intervals]) # if total is less than 3600 sec, the rest of index is set to zero
	freq_by_interval = pd.Series([freq[idx] if idx in freq.index else 0 for idx in intervals]) # if total time is less than 3600, the frequency larger than this specifc time is set to zero

	busiest_period = pd.Series(cummulated_freq.values - cummulated_freq_by_interval.values + freq_by_interval.values, index=freq.index).sort_values(ascending=False)[:n] # total = cumsum of the 3600th time-cumsum of the 1st time+ freq of 3600th time, sort in decending way   

	with open(output_path, 'wb') as results:
		for time_stamp, count in busiest_period.iteritems():
			results.write('%s -0400,%s\n' % (time_stamp.strftime("%d/%b/%Y:%H:%M:%S"), int(count)))