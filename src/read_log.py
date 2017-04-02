import pandas as pd
import csv

def read_log_txt(file_path):
	df = pd.read_csv(file_path, delimiter=' ', quoting=csv.QUOTE_NONE, error_bad_lines=False, header=None, usecols=[0, 3, 4, 5, 6, 7, 8, 9]) #read txt file, divide with space not with quote since there are two types of quotes in the log txt file, generate a dataframe with desired parameters
	df[5] = df[5] + ' ' + df[6] + ' ' + df[7] #conbine [5][6][7] into Request [5]
	df.drop(6, axis=1, inplace=True) #delete [6][7] 
	df.drop(7, axis=1, inplace=True)
	df.columns = ['Host', 'Timestamp', 'Timezone', 'Request', 'HttpCode', 'Bytes'] #reassign the name to columns
	df['Timestamp'] = pd.to_datetime(df['Timestamp'].str.replace('[', ''), format='%d/%b/%Y:%H:%M:%S') #change str type into timestamp, thus we can use math operation on time

	return df