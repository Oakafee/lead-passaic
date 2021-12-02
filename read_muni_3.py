import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from datetime import timedelta

NJ_MUNI = '/Users/Oakafee/Documents/cunymaps/nj-municipalities-age/Govt_admin_mun_coast_bnd/Govt_admin_mun_coast_bnd.shp'
PICKLE_PATH = '/Users/Oakafee/Documents/Grad_school/gisProgramming/project/ws_data/all_lead_as_one_3.pkl'

nj_muni = gpd.read_file(NJ_MUNI)
lead_info = pd.read_pickle(PICKLE_PATH)


# TODO: Harrison Twp in Gloucester County problem:
lead_info = lead_info[lead_info.Muncode != '0808']

maxlead = lead_info.groupby(by='Muncode').max()

nj_w_lead = pd.merge(nj_muni, maxlead, how="inner", left_on='MUN_CODE', right_on='Muncode')

nj_muni.plot()
nj_w_lead.plot(column='Lead_in_mg/L', cmap="OrRd", legend=True)
plt.show()

'''
for i in range(2002,2021):
	filename = 'yearplots/lead' + str(i) + '.jpg'
	leadyr = nj_w_lead[nj_w_lead.year == i]
	leadyr.plot(column="mcl_bool", cmap="OrRd", edgecolor='black')
	plt.savefig(filename)	

'''