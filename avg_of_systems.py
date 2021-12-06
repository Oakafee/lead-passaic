lead_cities = lead_info.Muncode.unique()

sys_lead = []

for m in lead_cities:
	for n in lead_info[lead_info.Muncode == m].itertuples():
		for year in range(2002,2022):
			sys_yr = n.Start_dates.date.year
				if ((sys_yr == year) or (sys_year == year - 1)):
					sys_lead.append(n.Lead_in_mgL)
				elif n.Start_dates.year == year - 1:
					
		
		
		
for row in lead_info.itertuples():
	# iterate through years
	for year in range(2002,2022):
		
			
for year in range(2002,2022):
	sys_lead = []
	for row in lead_info.itertuples():
		candidate = row[row.Start_dates.date.year]
		if candidate
		if row[row.Start_dates.date.year] == year:
			