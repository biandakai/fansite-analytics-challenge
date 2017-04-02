import pandas as pd


def get_blocked_requests(df, output_path):

	blocked_hosts = {}
	blocked_starts = {}
	blocked_results = []

	for _, row in df.iterrows():

		http_code = row['HttpCode']
		host = row['Host']
		time_stamp = row['Timestamp']

		blocked_start = blocked_starts.get(host, None)
		blocked = False

		if pd.to_numeric(http_code, errors='ignore') in [304, 401]:
			if blocked_start is None:
				blocked_starts[host] = time_stamp
				blocked_hosts[host] = 1
			else:
				time_delta =  (time_stamp - blocked_start).total_seconds()
				if time_delta <= 20:
					blocked_hosts[host] += 1
				else:
					blocked_starts[host] = time_stamp
					blocked_hosts[host] = 1

			if blocked_hosts.get(host, 0) > 3:
				blocked = True
		else:
			if blocked_start is not None and (time_stamp - blocked_start).total_seconds() > 5 * 60:
				blocked_starts.pop(host)
				blocked_hosts.pop(host)

			if blocked_hosts.get(host, 0) >= 3:
				blocked = True


		if blocked:
			blocked_results.append('%s - - [%s %s %s %s %s\n' % (host, time_stamp.strftime("%d/%b/%Y:%H:%M:%S"), row['Timezone'], row['Request'], row['HttpCode'], row['Bytes']))

	with open(output_path, 'wb') as results:
		results.writelines(blocked_results)
