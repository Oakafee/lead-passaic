import datetime

def find_dates(dates):
	start_dates = []
	end_dates = []
	
	for d in dates:
		try:
			int(d[0])
		except(ValueError):
			pass
		else:
			start, end = date_format(d)
			start_dates.append(start)
			end_dates.append(end)
	
	return(start_dates, end_dates)


def date_format(dr):
	start = []
	end = []

	dr = dr.split("--")
	dr[0] = dr[0].split("/")
	dr[1] = dr[1].split("/")

	for i in dr[0]:
		start.append(int(i))

	for i in dr[1]:
		end.append(int(i))

	start = datetime.datetime(start[2], start[0], start[1])
	end = datetime.datetime(end[2], end[0], end[1])
		
	return(start, end)
	
	
def conc_numeric(conc):
	conc_numeric = []
	for obs in conc:
		if obs == 'A 90th percentile value was not calculated':
			conc_numeric.append(float('nan'))
		else:
			obs = obs.split(" ")
			try:
				obs = float(obs[0])
			except(ValueError):
				pass	
			else:
				conc_numeric.append(obs)
	
	return conc_numeric
	
def muni_info(muni):
	muni = muni.split(", ")
	muni[1] = muni[1].split("-")
	return(muni[0], muni[1][0], muni[1][1])

# Takes two time delta objects
def time_delta_years(start, end):
	delta = end - start
	# TODO; round to nearest 0.5 years
	delta = delta.days / 365
	return delta	