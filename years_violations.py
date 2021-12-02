import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import data_format
import regional_sys

NJ_MUNI = '/Users/Oakafee/Documents/cunymaps/nj-municipalities-age/Govt_admin_mun_coast_bnd/Govt_admin_mun_coast_bnd.shp'
PICKLE_PATH = '/Users/Oakafee/Documents/Grad_school/gisProgramming/project/ws_data/all_lead_as_one_3.pkl'

LEGEND_SETTINGS = {
	'loc': 'center left',
	'bbox_to_anchor':(1,0.5),
	'fmt':"{:.0f}"
}

nj_muni = gpd.read_file(NJ_MUNI)
lead_info = pd.read_pickle(PICKLE_PATH)


# Parsippany Issue, because of the dash character in the name
lead_info = lead_info.replace('HILLS', '1429')

# Number of violations broken down by year
lead_info['mcl'] = lead_info['Lead_in_mgL'] > 0.015
years = []
for row in lead_info.itertuples():
	years.append(row.Start_dates.year)
lead_info['year'] = years

lead_years = lead_info.groupby(by=['Muncode','City','year']).sum('mcl').reset_index()

# Number of years with violations
lead_years['mcl_bool'] = (lead_years['mcl'] > 0)
lead_years = lead_years.groupby(by=['Muncode']).sum('mcl_bool').reset_index()

# To incorporate regional systems that cover more than one MUN_CODE each:
new_cities = []
new_mcls = []

for i in regional_sys.sys:
	same_lead = lead_years[lead_years.Muncode == i].iloc[0].mcl_bool
	for j in regional_sys.sys[i]:
		new_cities.append(j)
		new_mcls.append(same_lead)

new_mcl_df = pd.DataFrame(data={
	'Muncode': new_cities,
	'mcl_bool': new_mcls
})

lead_years = lead_years.append(new_mcl_df)

# Join dfs
nj_w_lead = pd.merge(nj_muni, lead_years, how="left", left_on='MUN_CODE', right_on='Muncode')

# Filter to only display counties where I have data. There must be a prettier way to do this
nj_w_lead = nj_w_lead[(nj_w_lead.COUNTY == 'ESSEX')| (nj_w_lead.COUNTY == 'MORRIS') | (nj_w_lead.COUNTY == 'HUDSON') | (nj_w_lead.COUNTY == 'BERGEN') | (nj_w_lead.COUNTY == 'PASSAIC')]

nj_w_lead.plot(
	column='mcl_bool',
	cmap="OrRd",
	edgecolor="gray",
	linewidth=0.1,
	legend=True,
	legend_kwds=LEGEND_SETTINGS,
	scheme='user_defined',
	classification_kwds={'bins':[.999, 1.999, 2.999, 3.999, 4.999]},
	missing_kwds={'color': 'white', 'edgecolor': 'gray', 'linewidth': 0.1, 'label': 'no data'},
)
#plt.show()
plt.savefig('plots/years_violations.jpg', bbox_inches='tight')