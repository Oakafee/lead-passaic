import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import data_format

NJ_MUNI = '/Users/Oakafee/Documents/cunymaps/nj-municipalities-age/Govt_admin_mun_coast_bnd/Govt_admin_mun_coast_bnd.shp'
PICKLE_PATH = '/Users/Oakafee/Documents/Grad_school/gisProgramming/project/ws_data/all_lead_as_one_3.pkl'

nj_muni = gpd.read_file(NJ_MUNI)
lead_info = pd.read_pickle(PICKLE_PATH)


# Harrison Twp in Gloucester County problem:
lead_info = lead_info[lead_info.Muncode != '0808']

'''
maxlead = lead_info.groupby(by='Muncode').max()
# or .max()
'''
'''
lead_info['mcl'] = lead_info['Lead in mgL'] > 0.015
lead2003 = lead_info[(lead_info.date > '2009-01-01') & (lead_info.date < '2010-01-01')]
'''

lead_mcls = lead_info[lead_info['Lead_in_mgL'] > 0.015]

# Length of time with lead problem
lead_cities = lead_info.Muncode.unique()
lead_times = []

for m in lead_cities:
	time = 0
	for n in lead_mcls[lead_mcls.Muncode == m].itertuples():
		time += data_format.time_delta_years(n.Start_dates, n.End_dates)
	lead_times.append(time)

lead_times_df = pd.DataFrame(data={
	'MUN_CODE': lead_cities,
	'lead_years': lead_times
})

'''
lead_violations = lead_info.groupby(by='Muncode').sum()

years = []
for row in lead_info.itertuples():
	years.append(row.date.year)
lead_info['year'] = years

lead_years = lead_info.groupby(by=['Muncode','City','year']).sum('mcl').reset_index()
print(lead_years.head())

lead_years['mcl_bool'] = (lead_years['mcl'] > 0)
#lead2019 = lead_years[lead_years.year==2019]

'''

nj_w_lead = pd.merge(nj_muni, lead_times_df, how="inner", left_on='MUN_CODE', right_on='MUN_CODE')

print(nj_w_lead[nj_w_lead.lead_years > 0])

nj_w_lead.plot(column='lead_years', cmap="OrRd")
plt.show()

'''
for i in range(2002,2021):
	filename = 'yearplots/lead' + str(i) + '.jpg'
	leadyr = nj_w_lead[nj_w_lead.year == i]
	leadyr.plot(column="mcl_bool", cmap="OrRd", edgecolor='black')
	plt.savefig(filename)	

'''