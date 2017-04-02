def get_most_active_hosts(df, output_path, n=10):
	active_hosts = df['Host'].value_counts()[:n] #count index IP frequency

	with open(output_path, 'wb') as results: #open and write a file
		for index, count in active_hosts.iteritems(): 
			results.write('%s,%s\n' % (index, count))
