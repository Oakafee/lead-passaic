import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import monthly_avg

PICKLE_PATH = '/Users/Oakafee/Documents/Grad_school/gisProgramming/project/ws_data/all_lead_as_one_3.pkl'
lead_info = pd.read_pickle(PICKLE_PATH)

# All systems:
all_systems = lead_info.PWSID.unique()
global_avg_lead = monthly_avg.monthly_est(all_systems, lead_info)

# Systems with lead MCL violations:
mcl_systems = lead_info[lead_info['Lead_in_mgL'] >= 0.015].PWSID.unique()
mcl_avg_lead = monthly_avg.monthly_est(mcl_systems, lead_info)

# Systems without MCL violations:
other_systems = all_systems.tolist()
for x in mcl_systems:
	other_systems.remove(x)	
other_avg_lead = monthly_avg.monthly_est(other_systems, lead_info)

plt.plot(
	global_avg_lead.date,
	global_avg_lead.Lead_in_mgL,
	label='all systems (' + str(len(all_systems)) + ')'
)
plt.plot(
	mcl_avg_lead.date,
	mcl_avg_lead.Lead_in_mgL,
	label='systems with violations (' + str(len(mcl_systems)) + ')'
)
plt.plot(
	other_avg_lead.date,
	other_avg_lead.Lead_in_mgL,
	label='systems w/o violations (' + str(len(other_systems)) + ')'
)
plt.axhline(y=0.015, color='red', linestyle='--')
plt.legend(title='Average lead concentration by year')
#plt.show()
plt.savefig('plots/monthly_avgs.jpg')