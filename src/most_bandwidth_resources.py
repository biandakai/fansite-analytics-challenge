import pandas as pd


def get_most_bandwidth_resources(df, output_path, n=10):
	df['Bytes'] = pd.to_numeric(df['Bytes'], errors='coerce', downcast='integer').fillna(0) # convert str to int, if byte is '-',change to 0
	most_bandwidth = df[['Request', 'Bytes']].groupby('Request').sum().sort_values(by='Bytes', ascending=False).head(n)#group and sum the request, return a data frame with the largest 10 bandwidth 

	with open(output_path, 'wb') as results:
		for request, _ in most_bandwidth.iterrows():
			url = request.split(' ')[1] if ' ' in request else request
			results.write('%s\n' % url)