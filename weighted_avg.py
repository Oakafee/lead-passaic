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

# Length of time with lead problem
lead_cities = lead_info.Muncode.unique()
lead_avgs = []

for m in lead_cities:
	weighted_conc = []
	total_years = 0
	for n in lead_info[lead_info.Muncode == m].itertuples():
		if math.isnan(n.Lead_in_mgL):
			continue
		years = data_format.time_delta_years(n.Start_dates, n.End_dates)
		total_years += years
		weighted = n.Lead_in_mgL * years
		weighted_conc.append(weighted)
	weighted_conc = np.array(weighted_conc)
	#lead_avgs.append(np.sum(weighted_conc))
	lead_avgs.append(np.mean(weighted_conc))

lead_avg_df = pd.DataFrame(data={
	'MUN_CODE': lead_cities,
	'lead_avg_conc': lead_avgs
})

# To incorporate regional systems that cover more than one MUN_CODE each:
new_cities = []
new_avgs = []

for i in regional_sys.sys:
	same_lead = lead_avg_df[lead_avg_df.MUN_CODE == i].iloc[0].lead_avg_conc
	for j in regional_sys.sys[i]:
		new_cities.append(j)
		new_avgs.append(same_lead)

new_avg_df = pd.DataFrame(data={
	'MUN_CODE': new_cities,
	'lead_avg_conc': new_avgs
})

lead_avg_df = lead_avg_df.append(new_avg_df)


# Join the two dfs
nj_w_lead = pd.merge(nj_muni, lead_avg_df, how="left", left_on='MUN_CODE', right_on='MUN_CODE')

# Filter to only display counties where I have data. There must be a prettier way to do this
nj_w_lead = nj_w_lead[(nj_w_lead.COUNTY == 'ESSEX')| (nj_w_lead.COUNTY == 'MORRIS') | (nj_w_lead.COUNTY == 'HUDSON') | (nj_w_lead.COUNTY == 'BERGEN') | (nj_w_lead.COUNTY == 'PASSAIC')]

nj_w_lead.plot(
	column='lead_avg_conc',
	cmap="OrRd",
	edgecolor="gray",
	linewidth=0.1,
	legend=True,
	legend_kwds=LEGEND_SETTINGS,
	scheme='user_defined',
	classification_kwds={'bins':[0.010, 0.0125, 0.015, 0.0175, 0.020]},
	missing_kwds={'color': 'white', 'edgecolor': 'gray', 'linewidth': 0.1, 'label': 'no data'},
)
#plt.show()
plt.savefig('plots/weighted_avg.jpg', bbox_inches='tight')