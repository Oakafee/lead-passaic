# TODO: delete this, it's outdated

import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_PATH = '/Users/Oakafee/Documents/Grad_school/gisProgramming/project/ws_data/'
INPUT_PICKLE_NAME = 'all_lead_dfs.pkl'
OUTPUT_PICKLE_NAME = 'all_lead_as_one.pkl'

pickle_off = open(BASE_PATH + INPUT_PICKLE_NAME, "rb")
tables = pickle.load(pickle_off)
as_one = pd.DataFrame()

for table in tables:
	#print(type(table))
	try:
		# TODO: make sure to include other fields
		start = table.loc[:, table.columns != 'End dates',]
		end = table.loc[:, table.columns != 'Start dates']

	except:
		print('This data frame is empty or invalid for some reason')
	else:
		start.rename(columns = {'Start dates':'date'}, inplace = True)
		end.rename(columns = {'End dates':'date'}, inplace = True)

		alldates = pd.concat([start,end], ignore_index=True, sort=True)
		alldates.sort_values(by='date', inplace=True)

		as_one = as_one.append(alldates)

print(as_one.head())

as_one.to_pickle(BASE_PATH + OUTPUT_PICKLE_NAME)