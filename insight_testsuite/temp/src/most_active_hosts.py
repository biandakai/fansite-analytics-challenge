def get_most_active_hosts(df, output_path, n=10):
	active_hosts = df['Host'].value_counts()[:n]

	with open(output_path, 'wb') as results:
		for index, count in active_hosts.iteritems():
			results.write('%s,%s\n' % (index, count))
