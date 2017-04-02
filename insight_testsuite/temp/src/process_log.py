import sys
import os
from read_log import read_log_txt
from most_active_hosts import get_most_active_hosts
from most_bandwidth_resources import get_most_bandwidth_resources
from busiest_period import get_busiest_period
from block_requests import get_blocked_requests


def main():
	input_path, hosts_path, hours_path, resources_path, blocked_path = sys.argv[1:]
	cwd = os.getcwd()

	df = read_log_txt(file_path=os.path.join(cwd, input_path.replace('./', '')))

	get_most_active_hosts(df, output_path=os.path.join(cwd, hosts_path.replace('./', '')), n=10)

	get_most_bandwidth_resources(df, output_path=os.path.join(cwd, resources_path.replace('./', '')), n=10)

	get_busiest_period(df, output_path=os.path.join(cwd, hours_path.replace('./', '')), n=10)

	get_blocked_requests(df, output_path=os.path.join(cwd, blocked_path.replace('./', '')))



if __name__ == "__main__":
    main()