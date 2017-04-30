import os, sys, datetime, datetime
import _pickle as cPickle
#import cPickle as pickle

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import functools
import json
 
from email_alert import EmailAlert
#from insights import Insights 

pd.set_option('max_colwidth',180)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

np.random.seed(42)

data_directory = ""

query = {
	'DSP': "dsp_query_new.sql",
	'DSP-PUB': "dsp-pub.sql",
	'LANDINGPAGE': "dsp-landingpage.sql",
	'DC': "dsp-dc.sql",
	'CHANNEL': "dsp-channel.sql"
}

dsps = []

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
	email(processed_data)

def load_data(sql, fname, param=None, param_num=None):
	with open(sql) as f:
		if param is None:
			query = f.read().strip()
		elif param_num == 1:
			query = f.read().strip() % (param)
		elif param_num == 2:
			query = f.read().strip() % (param, param)
		else: 
			print("incorrect param_number")
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

def transform_data(df):
	day = df['day'][0]
	accts = pd.Series(df.index)
	headers = []
	value = []

	acctid = df['buyerid'].T.drop_duplicates().T
	acctid_array = np.array(acctid['buyerid'])
	acctids = ', '.join([str(i) for i in acctid_array])

	yesterday_cols = ['revenue' , 'offer' , 'offerrate' , 'offermatchrate' , 'bidrate' , 'blockrate' , 'winrate' , 'revcpm'
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
		acct_data = pd.concat([acct_yesterday, pday, avg4d, avg7d], axis = 1, keys=[day, 'change agst prior day', 'change agst 4-day avg', 'change agst 7-day avg'])
		acct_data= acct_data.reset_index()
		#formatting metric names 
		acct_data['metric'] = acct_data['metric'].apply(lambda x: x.replace('rate', ' rate')) 
		data = df_json(acct_data)
		header = data['columns']
		val = data['data']
		headers.append(header)
		value.append(val)
	return acctid_array, accts, headers, value


def email(df):
	acctid_array, accts, headers, value = transform_data(df)

	pub = get_topdrop(acctid_array, query['DSP-PUB'], 'dsp-pub', 2, 'publisher','rev_difference', 'rev_delta', '* Top drop pubs: ')
	landingpages = get_topdrop(acctid_array, query['LANDINGPAGE'], 'dsp_landingpage', 1, 'landingpagedomain', 'difference', 'delta', '* Top drop campaigns: ')
	datacenters = get_topdrop(acctid_array, query['DC'], 'dsp_dc', 1, 'dc', 'difference', 'delta', '* Change by DataCenter: ')
	channels = get_topdrop(acctid_array, query['CHANNEL'], 'dsp_channel', 1, 'channel', 'difference', 'delta', '* Change by Channel: ')

	html = EmailAlert('dsp', 'input.mjml', accts, pub, landingpages, datacenters, channels, headers, value)	
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


def get_topdrop(acctid, sql, fname, param_num, dimension, difference, delta, strheader):
	acctids = ', '.join([str(i) for i in acctid])
	df = load_data(sql, fname, acctids, param_num)
	res = []
	for acct in acctid:
		top = df[df['buyerid'] == acct]
		top = top.sort_values(by = [difference], ascending = [True])
		top['difference_str'] = top[difference].apply(lambda x: int(round(x))).apply(str)
		top['num_sign'] = top['difference_str'].apply(lambda x: '-' if x.startswith( '-' ) else '')
		top["difference_abs"] = top[difference].abs()
		top['difference_abs_formatted'] = top['difference_abs'].apply(lambda x: '&#36;' + '{:,}'.format(int(round(x))))
		top[difference] = top['num_sign'] + top['difference_abs_formatted']
		selectedCols = top[[dimension, difference, delta]]
		selectedCols[delta] = np.vectorize(percent)(selectedCols[delta])
		if len(top)>= 3:
			top3 = selectedCols[:3]
		else:
			top3 = selectedCols
		string = strheader
		for i in range(len(top3)):
			val = ', '.join([str(i) for i in top3.iloc[i]])
			string = string + val + "; "
		res.append(string)
	return res 

