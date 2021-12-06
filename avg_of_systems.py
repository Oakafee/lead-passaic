import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

PICKLE_PATH = '/Users/Oakafee/Documents/Grad_school/gisProgramming/project/ws_data/all_lead_as_one_3.pkl'
AVG_VALUE = 0.01

lead_info = pd.read_pickle(PICKLE_PATH)
lead_cities = lead_info.PWSID.unique()

pwsids = []
dates = []
leadcs = []

for m in lead_cities:
	for year in range(2002,2022):
		for month in [1, 7]:
			ordered = lead_info[lead_info.PWSID == m].sort_values(by='Start_dates')
			for n in ordered.itertuples():
				leadval = -9999
				if ((n.Start_dates.year == year) and (n.Start_dates.month == month)):
					leadval = n.Lead_in_mgL
					break
			# If you can't find a lead concentration for the date, just assume the previous value is still valid
			if (leadval == -9999):
				if len(leadcs):
					leadval = leadcs[-1]
				else:
					# if we are just starting out then just estimate the global average value TODO calculate global average value
					leadval = AVG_VALUE
			leadcs.append(leadval)
			pwsids.append(m)
			isodate = date.fromisoformat(str(year)+'-'+str(month).zfill(2)+'-01')		
			dates.append(isodate)
						
print('pwsids length', len(pwsids))
print('dates length', len(dates))
print('leadcs length', len(leadcs))
						
monthly_est_df = pd.DataFrame(data={
	'PWSID': pwsids,
	'date': dates,
	'Lead_in_mgL': leadcs
})

print(monthly_est_df[monthly_est_df.PWSID=='NJ0714001'])

global_avg_lead = monthly_est_df.groupby(by='date').mean('Lead_in_mgL').reset_index()
plt.plot(global_avg_lead.date, global_avg_lead.Lead_in_mgL)
plt.show()