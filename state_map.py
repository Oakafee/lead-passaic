import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import data_format
import math

NJ_MUNI = '/Users/Oakafee/Documents/cunymaps/nj-municipalities-age/Govt_admin_mun_coast_bnd/Govt_admin_mun_coast_bnd.shp'

LEGEND_SETTINGS = {
	'loc': 'center left',
	'bbox_to_anchor':(1,0.5),
	'fmt':"{:.0f}"
}

nj_muni = gpd.read_file(NJ_MUNI)

nj_muni.plot()
plt.savefig('plots/state.jpg')