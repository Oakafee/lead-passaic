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

# Filter to only display counties where I have data. There must be a prettier way to do this
nj_muni = nj_muni[(nj_muni.COUNTY == 'ESSEX')| (nj_muni.COUNTY == 'MORRIS') | (nj_muni.COUNTY == 'HUDSON') | (nj_muni.COUNTY == 'BERGEN') | (nj_muni.COUNTY == 'PASSAIC')]

nj_muni.plot(
	column='POP2010',
	cmap="Blues",
	edgecolor="gray",
	linewidth=0.1,
	legend=True,
	legend_kwds=LEGEND_SETTINGS,
	scheme="NaturalBreaks"
)
#plt.show()
plt.savefig('plots/pop.jpg', bbox_inches='tight')