import pandas as pd


def get_blocked_requests(df, output_path):

	blocked_hosts = {} #record failure time of  a potential blocked host in a time period
	blocked_starts = {} #record start time of ip 
	blocked_results = [] #output --> into the output  file

	for _, row in df.iterrows():

		http_code = row['HttpCode']
		host = row['Host']
		time_stamp = row['Timestamp']

		blocked_start = blocked_starts.get(host, None) # get block start time by host
		blocked = False 

		if pd.to_numeric(http_code, errors='ignore') in [304, 401]: #convert str into int if it is 304 or 401
			if blocked_start is None: # if not fails before
				blocked_starts[host] = time_stamp #record initial failure
				blocked_hosts[host] = 1 # failure counts =1
			else:
				time_delta =  (time_stamp - blocked_start).total_seconds() #calculate the time interval between next failure
				if time_delta <= 20: # if time interval is less than 20 sec
					blocked_hosts[host] += 1 # failure counts+1
				else:
					blocked_starts[host] = time_stamp # if time is larger than 20sec, record as initial faulre
					blocked_hosts[host] = 1

			if blocked_hosts.get(host, 0) > 3: # if failure time >3, this host is blocked
				blocked = True
		else: # normal login but..
			if blocked_start is not None and (time_stamp - blocked_start).total_seconds() > 5 * 60: # if this host has failure login but the interval is larger than 5 min, delete the host from the potential blocked list
				blocked_starts.pop(host)
				blocked_hosts.pop(host)

			if blocked_hosts.get(host, 0) >= 3: # if the failure attempt of a host larger than 3 times, blocked
				blocked = True


		if blocked: # record the blocked information into the list
			blocked_results.append('%s - - [%s %s %s %s %s\n' % (host, time_stamp.strftime("%d/%b/%Y:%H:%M:%S"), row['Timezone'], row['Request'], row['HttpCode'], row['Bytes']))

	with open(output_path, 'wb') as results:
		results.writelines(blocked_results)
