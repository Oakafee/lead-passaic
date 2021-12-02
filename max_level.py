import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from regional_sys import sys

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

# Only one line of data manipulation in this one, incredibly
maxlead = lead_info.groupby(by='Muncode').max('Lead_in_mgL').reset_index()

# To incorporate regional systems that cover more than one MUN_CODE each:
new_cities = []
new_maxes = []

for i in sys:
	same_lead = maxlead[maxlead.Muncode == i].iloc[0].Lead_in_mgL
	for j in sys[i]:
		new_cities.append(j)
		new_maxes.append(same_lead)

new_maxes_df = pd.DataFrame(data={
	'Muncode': new_cities,
	'Lead_in_mgL': new_maxes
})

maxlead = maxlead.append(new_maxes_df)

# Join dfs
nj_w_lead = pd.merge(nj_muni, maxlead, how="left", left_on='MUN_CODE', right_on='Muncode')

# Filter to only display counties where I have data. There must be a prettier way to do this
nj_w_lead = nj_w_lead[(nj_w_lead.COUNTY == 'ESSEX')| (nj_w_lead.COUNTY == 'MORRIS') | (nj_w_lead.COUNTY == 'HUDSON') | (nj_w_lead.COUNTY == 'BERGEN') | (nj_w_lead.COUNTY == 'PASSAIC')]

nj_w_lead.plot(
	column='Lead_in_mgL',
	cmap="OrRd",
	edgecolor="gray",
	linewidth=0.1,
	legend=True,
	legend_kwds=LEGEND_SETTINGS,
	scheme='user_defined',
	classification_kwds={'bins':[0.010, 0.015, 0.025, 0.04, 0.06]},
	missing_kwds={'color': 'white', 'edgecolor': 'gray', 'linewidth': 0.1, 'label': 'no data'},
)
#plt.show()
plt.savefig('plots/max_levels.jpg', bbox_inches='tight')