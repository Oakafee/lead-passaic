import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import data_format
import regional_sys
import math


NJ_MUNI = '/Users/Oakafee/Documents/cunymaps/nj-municipalities-age/Govt_admin_mun_coast_bnd/Govt_admin_mun_coast_bnd.shp'
PICKLE_PATH = '/Users/Oakafee/Documents/Grad_school/gisProgramming/project/ws_data/all_lead_as_one_3.pkl'
LEGEND_SETTINGS = {
	'loc': 'center left',
	'bbox_to_anchor':(1,0.5),
	'fmt':"{:.4f}"
}



nj_muni = gpd.read_file(NJ_MUNI)
lead_info = pd.read_pickle(PICKLE_PATH)


# Parsippany Issue, because of the dash character in the name
lead_info = lead_info.replace('HILLS', '1429')

# Belleville data cleaning: very low value was messing up log scale
lead_info.replace(0.00017, 0, inplace=True)


# Length of time with lead problem...using PWSID instead of Muncode
lead_systems = lead_info.PWSID.unique()
lead_avgs = []
sys_names = []

for m in lead_systems:
	weighted_conc = []
	total_years = 0
	sys_name = ''
	for n in lead_info[lead_info.PWSID == m].itertuples():
		if math.isnan(n.Lead_in_mgL):
			continue
		years = data_format.time_delta_years(n.Start_dates, n.End_dates)
		total_years += years
		weighted = n.Lead_in_mgL * years
		weighted_conc.append(weighted)
		sys_name = n.Water_system_name
	weighted_conc = np.array(weighted_conc)
	lead_avgs.append(np.sum(weighted_conc)/total_years)
	# And the water system names (could also be city names)
	sys_names.append(sys_name)

lead_avg_df = pd.DataFrame(data={
	'PWSID': lead_systems,
	'water_system_name': sys_names,
	'lead_avg_conc': lead_avgs
})

# Top ten lead contaminated water systems:
top_contam = lead_avg_df.sort_values(by='lead_avg_conc', ascending=False)[0:8].PWSID

# Make line graph of top ten: need to spread out dates
start = lead_info.loc[:,['Start_dates', 'PWSID', 'Water_system_name', 'Lead_in_mgL']]
end = lead_info.loc[:,['End_dates', 'PWSID', 'Water_system_name', 'Lead_in_mgL']]
start.rename(columns = {'Start_dates':'date'}, inplace = True)
end.rename(columns = {'End_dates':'date'}, inplace = True)
alldates = pd.concat([start,end], ignore_index=True, sort=True)
alldates.sort_values(by='date', inplace=True)

for m in top_contam:
	sys = alldates[alldates.PWSID == m]
	label = sys.iloc[0].Water_system_name
	plt.plot(sys.date, sys.Lead_in_mgL, label=label, linewidth=2.5)
# a horizontal line
plt.axhline(y=0.015, color='red', linestyle='--')
plt.semilogy()
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
#plt.show()
plt.savefig('plots/top_ten.jpg', bbox_inches='tight')