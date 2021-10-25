import numpy
import pandas as pd

import date_format

FILE_PATH = '/Users/Oakafee/Documents/Grad_school/gisProgramming/project/'

def read_file():
	lead_page = open(FILE_PATH + 'north-caldwell.html')
	ws_table = pd.read_html(lead_page, attrs = {'style': 'background:#99CCFF;'})
	lead_page.close()
	
	lead_page = open(FILE_PATH + 'north-caldwell.html')
	lead_table = pd.read_html(lead_page, header=4, attrs = {'id': 'PB'})
	lead_page.close()
	
	format_lead_df(lead_table).to_pickle(FILE_PATH + 'ws_data/' + format_filename(ws_table))


def format_lead_df(lead_table):
	dates = lead_table[0]['Compliance Period']
	freq = lead_table[0]['SampleFrequency']
	conc = lead_table[0]['90th Percentile*']

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

	start_dates = []
	end_dates = []

	for d in dates:
		try:
			int(d[0])
		except(ValueError):
			pass
		else:
			start, end = date_format.date_format(d)
			start_dates.append(start)
			end_dates.append(end)
			
	lead_df = {
		'Start dates': start_dates,
		'End dates': end_dates,
	#	freq.name: freq,
		'Lead in mg/L': conc_numeric
	}

	return pd.DataFrame(lead_df)

def format_filename(ws_table):
	'''
	pwsid = ws_table[1][0]
	wsname = ws_table[1][1]
	wsname = wsname.lower()
	wsname = wsname.replace(" ","-")
	return(pwsid + '-' + wsname + '.pkl')
	'''
	return('meowwolf.pkl')
	
read_file()