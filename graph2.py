import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


PICKLE_PATH = '/Users/Oakafee/Documents/Grad_school/gisProgramming/project/ws_data/all_lead_as_one.pkl'

df = pd.read_pickle(PICKLE_PATH)
print(df.columns)

'''
plt.plot(df['date'],df['Lead in mg/L'])
plt.show()


highlead = df[df['Lead in mg/L'] > 0.015]
print(highlead.to_string())

'/Users/Oakafee/Documents/nj-gis-data/County_Boundaries_of_NJ-shp'

import geopandas as gpd

nj =  gpd.read_file('/Users/Oakafee/Documents/nj-gis-data/County_Boundaries_of_NJ-shp')
'''