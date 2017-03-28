import os, sys, datetime, datetime
import _pickle as cPickle
#import cPickle as pickle

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import functools
import json
 
from email_alert import EmailAlert

pd.set_option('max_colwidth',180)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

np.random.seed(42)

data_directory = ""

query = {
	'DSP': "dsp_query_new.sql"
}

me = 'ssu@pulsepoint.com'

you = 'ssu@pulsepoint.com'

neg_alert_threshold = -10
#pos_alert_threshold = 10
alert_rev_cutoff = 500

def currency(data):
	d = '{:,}'.format(data)
	formatted_d = '&#36;' + d
	return formatted_d

def percent(data):
	return '{:.1f}%'.format(data)

def unit_mm(data):
	return '{:,.0f}M'.format(data/1000000)

def run_app(sql, fname):
	df = load_data(sql, fname)
	processed_data = run_data(df)
	output_email(processed_data)

def load_data(sql, fname):
	with open(sql) as f:
		query = f.read().strip()
	filename = os.path.join(data_directory, "{}_{}.pkl".format(fname, datetime.datetime.now().strftime("%Y%m%d")))
	if os.path.exists(filename) is False:
		df = pd.read_sql(query, create_engine("impala://impala.pulse.prod"))
		df.to_pickle(filename)
	else:
		df = pd.read_pickle(filename)
	return df

def run_data(df):
	df = df.sort_values(by = ['revenue'], ascending = [False])

	df['weights'] = 1 + ((df['rev_diff_agst_pd'].abs() - df['rev_diff_agst_pd'].abs().min()) / (df['rev_diff_agst_pd'].abs().max() - df['rev_diff_agst_pd'].abs().min()))
	df['weighted_pd_change'] = df['weights'] * df['revenue_change_agst_pd']
	df['weighted_4d_change'] = df['weights'] * df['revenue_change_agst_4davg']
	df['weighted_7d_change'] = df['weights'] * df['revenue_change_agst_7davg']		

	df = df.set_index('advertiser')

	#only focus on accts that have avg daily rev >= X cutoff
	df = df[df['7davgrevenue'] >= alert_rev_cutoff]
	#cutom criteria 
	Crit1 = df.weighted_pd_change <= neg_alert_threshold
	Crit2 = df.weighted_4d_change <= neg_alert_threshold
	Crit3 = df.weighted_7d_change <= neg_alert_threshold
	#Crit4 = df.rev_change_agst_pd >= pos_alert_threshold
	#Crit5 = df.rev_change_agst_4davg >= pos_alert_threshold
	#Crit6 = df.rev_change_agst_7davg >= pos_alert_threshold

	CritList = [Crit1,Crit2,Crit3]
	AllCrit = functools.reduce(lambda x,y: x | y, CritList)

	new_df = format_data(df[AllCrit])
	return new_df

def output_email(df):
	day = df['day'][0]
	accts = pd.Series(df.index)
	headers = []
	value = []
	yesterday_cols = ['revenue' , 'offer' , 'offerrate' , 'offermatchrate' , 'bidrate' , 'matchbidrate' , 'blockrate' , 'winrate' , 'revcpm'
	                     , 'costcpm' , 'margin' , 'timeoutrate']
	yesterday = df[yesterday_cols]
	yesterday_T = yesterday.T
	delta_col = list(df.loc[:, 'revenue_change_agst_pd':'timeoutrate_change_agst_7davg'])
	delta = df[delta_col]

	for acct in accts:
		acct_yesterday = yesterday_T[acct]
		pday = slice_data('pd', delta, acct)
		avg4d = slice_data('4davg', delta, acct) 
		avg7d = slice_data('7davg', delta, acct) 
		acct_data = pd.concat([acct_yesterday, pday, avg4d, avg7d], axis = 1, keys=[day, 'change agst Prior Day', 'change agst 4-day avg', 'change agst 7-day avg'])
		acct_data= acct_data.reset_index()
		data = df_json(acct_data)
		header = data['columns']
		val = data['data']
		headers.append(header)
		value.append(val)
	html = EmailAlert('dsp', 'input.mjml', accts, headers, value)	
	html.render_template()
	html.send_email('Testing', me, you)


def format_data(df):
	mm_col = df[[col for col in df.columns if ('bidsoffered' in col) | (col == 'offer')]]
	for col in mm_col:
		df[col] = np.vectorize(unit_mm)(df[col])
	currency_col = df[[col for col in df.columns if  (('rev' in col) & ('_' not in col)) | (('cost' in col) & ('_' not in col))| (col == 'rev_diff_agst_pd') ]]
	for col in currency_col:
		df[col] = np.vectorize(currency)(df[col])
	pct_col = df[[col for col in df.columns if ('rate' in col) | ('change' in col) | ('margin' in col)]]
	for col in pct_col:
		df[col] = np.vectorize(percent)(df[col])
	return df 

def slice_data(timewindow, data, dsp):
	timewindow_delta = data.T[[timewindow in n for n in data.T.index]]
	acct_data = timewindow_delta[dsp]
	acct_data.index = acct_data.index.str.split('_').str.get(0)
	acct_data.index.name = 'metric'
	return acct_data

def df_json(df):
	json_str = df.to_json(orient='split')
	data = json.loads(json_str)
	return data 