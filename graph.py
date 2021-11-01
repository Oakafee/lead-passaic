import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



PICKLE_PATH = '/Users/Oakafee/Documents/Grad_school/gisProgramming/project/ws_data/all_lead_dfs.pkl'

pickle_off = open(PICKLE_PATH, "rb")
tables = pickle.load(pickle_off)

for table in tables:
	print(type(table))
	try:
		start = table.loc[:,['Start dates','Lead in mg/L']]
		end = table.loc[:,['End dates','Lead in mg/L']]

		start.rename(columns = {'Start dates':'date'}, inplace = True)
		end.rename(columns = {'End dates':'date'}, inplace = True)

		alldates = pd.concat([start,end], ignore_index=True, sort=True)
		alldates.sort_values(by='date', inplace=True)

		plt.plot(alldates['date'],alldates['Lead in mg/L'])
	except:
		print('oops')
plt.show()

