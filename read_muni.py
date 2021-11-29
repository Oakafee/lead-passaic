import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

NJ_MUNI = '/Users/Oakafee/Documents/cunymaps/nj-municipalities-age/Govt_admin_mun_coast_bnd/Govt_admin_mun_coast_bnd.shp'
PICKLE_PATH = '/Users/Oakafee/Documents/Grad_school/gisProgramming/project/ws_data/all_lead_as_one.pkl'

nj_muni = gpd.read_file(NJ_MUNI)
lead_info = pd.read_pickle(PICKLE_PATH)

lead_info['mcl'] = lead_info['Lead in mg/L'] > 0.015
lead2003 = lead_info[(lead_info.date > '2009-01-01') & (lead_info.date < '2010-01-01')]

nj_w_lead = pd.merge(nj_muni, lead2003, how="inner", left_on='MUN_CODE', right_on='Muncode')

#print(nj_w_lead.head())

nj_w_lead.plot(column="mcl", cmap="OrRd")
plt.show()