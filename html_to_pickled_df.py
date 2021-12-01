# This is the up-to-date way to load in data

import os
import pickle
import numpy
import pandas as pd
import data_format

BASE_PATH = '/Users/Oakafee/Documents/Grad_school/gisProgramming/project/'
HTML_FOLDER = 'web_lead'
PICKLE_PATH = 'ws_data/all_lead_as_one_3.pkl'
# Combines start and end dates into one
STACK_DATES = False

cwd = os.getcwd()

def go_through_files(base_path):
	pickle_path = cwd + '/ws_data/all_lead_dfs.pkl'
	all_lead = []
	
	for name in os.listdir(base_path):
		path = os.path.join(base_path, name)
		ws_df = read_file(path)
		if not type(ws_df) == bool:
			all_lead.append(ws_df)
	
	all_lead_df = pd.concat(all_lead, ignore_index=True)
	all_lead_df.to_pickle(BASE_PATH + PICKLE_PATH)

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
	
	return format_lead_df(lead_table, ws_table)


def format_lead_df(lead_table, ws_table):

	dates = lead_table[0]['Compliance Period']
	freq = lead_table[0]['SampleFrequency']
	conc = lead_table[0]['90th Percentile*']
	pwsid = ws_table[0][1][0]
	ws_name = ws_table[0][1][1]
	muni = ws_table[0][1][3]

	start_dates, end_dates = data_format.find_dates(dates)
	county, city, muncode = data_format.muni_info(muni)
			
	lead_df = {
		'Start_dates': start_dates,
		'End_dates': end_dates,
	#	freq.name: freq,
		'Lead_in_mg/L': data_format.conc_numeric(conc),
		# PWSID
		'PWSID': pwsid,
		# Water System Name
		'Water_system_name': ws_name,
		# Principal County and City
		'City': city,
		'County': county,
		'Muncode': muncode
		# TODO: consider population
	}
	try:
		lead_df = pd.DataFrame(lead_df)
		#print(lead_df.head())
	except:
		print('problem formatting DF:', lead_df)
		lead_df = False
	else:
		if STACK_DATES:
			lead_df = stack_dates(lead_df)
		else:
			lead_df.sort_values(by='Start_dates', inplace=True)

	return lead_df

def stack_dates(table):
	try:
		start = table.loc[:, table.columns != 'End dates',]
		end = table.loc[:, table.columns != 'Start dates']
	except:
		print('This data frame is empty or invalid for some reason')
		return False
		
	start.rename(columns = {'Start dates':'date'}, inplace = True)
	end.rename(columns = {'End dates':'date'}, inplace = True)

	alldates = pd.concat([start,end], ignore_index=True, sort=True)
	alldates.sort_values(by='date', inplace=True)
	return alldates
	

go_through_files(BASE_PATH + HTML_FOLDER)