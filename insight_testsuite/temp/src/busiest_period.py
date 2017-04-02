import pandas as pd
import numpy as np
from datetime import timedelta


def get_busiest_period(df, output_path, n=10):

	freq = df['Timestamp'].value_counts().sort_index(ascending=False)

	lag = freq.index + timedelta(seconds=3600)
	intervals = np.searchsorted(freq.index.astype(np.int64), lag.astype(np.int64))
	cummulated_freq = freq.cumsum()

	cummulated_freq_by_interval = pd.Series([cummulated_freq[idx] if idx in cummulated_freq.index else 0 for idx in intervals])
	freq_by_interval = pd.Series([freq[idx] if idx in freq.index else 0 for idx in intervals])

	busiest_period = pd.Series(cummulated_freq.values - cummulated_freq_by_interval.values + freq_by_interval.values, index=freq.index).sort_values(ascending=False)[:n]

	with open(output_path, 'wb') as results:
		for time_stamp, count in busiest_period.iteritems():
			results.write('%s -0400,%s\n' % (time_stamp.strftime("%d/%b/%Y:%H:%M:%S"), int(count)))