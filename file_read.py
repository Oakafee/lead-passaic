import os
import pickle
import numpy
import pandas as pd
import date_format

BASE_PATH = '/Users/Oakafee/Documents/Grad_school/gisProgramming/project/web_lead'
cwd = os.getcwd()

def read_file(path):
	if path[-4:] != 'html':
		print('skipping because not an html file:', path)
		return
	lead_page = open(path)
	ws_table = pd.read_html(lead_page, attrs = {'style': 'background:#99CCFF;'})
	lead_page.close()
	
	lead_page = open(path)
	lead_table = pd.read_html(lead_page, header=4, attrs = {'id': 'PB'})
	lead_page.close()
	
	return format_lead_df(lead_table)
	
	'''
	if not formatted_df.empty:
		formatted_df.to_pickle(cwd + '/ws_data/' + format_filename(ws_table))
	'''


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

	try:
		lead_df = pd.DataFrame(lead_df)
	except:
		print('problem formatting DF:', lead_df)
		lead_df = pd.DataFrame({})

	return lead_df

def format_filename(ws_table):
	print(ws_table[0][0][1])
	pwsid = ws_table[0][1][0]
	wsname = ws_table[0][1][1]
	wsname = wsname.lower()
	wsname = wsname.replace(" ","-")
	return(pwsid + '-' + wsname + '.pkl')
	
def go_through_files(base_path):
	pickle_path = cwd + '/ws_data/all_lead_dfs.pkl'
	all_lead_dfs = []
	
	for name in os.listdir(base_path):
		path = os.path.join(base_path, name)
		all_lead_dfs.append(read_file(path))
	
	with open(pickle_path, 'wb') as fil:
		pickle.dump(all_lead_dfs, fil)
	

go_through_files(BASE_PATH)