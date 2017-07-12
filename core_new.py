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
from pp_data import pp_data
from process_data import process_data
from insights import insights


data_directory = "C:/Users/ssu/Documents/github/alerting/"

dsp_queries = {
	'dsp': "dsp_kpi.sql",
	'pub': "dsp-pub.sql",
	'campaign': "dsp-landingpage.sql",
	'datacenter': "dsp-dc.sql",
	'channel': "dsp-channel.sql",
	'bidloss': "dsp-bidloss.sql",
	"test": "master.sql"
}

account_type = {
	"dsp" : 'dsp',
	"pub" : 'pub'
}

change_type = {
	'jumpers': 'jumpers',
	'droppers': 'droppers'
}

links = {
	'Tableau_dsp_pub': 'http://tableau:8000/#/views/DSPTrendsDashboard/DSPPublisherTrends7D?'
}

default_message = {
	'pub': "The account dropped aganst 4(7)-day average. If expected, ignore the alert. O/w, please take a look.",
	'campaign': "",
	'channel': ""
}

alert_param = {
	'alertee_account_rev_threshold': 1000,
	'jumper_pct_cutoff': 15,
	'jumper_absolute_cutoff': 5000,
	'dropper_pct_cutoff': 15,
	'dropper_absolute_cutoff': 5000,
	'dsp_pub_top_changers_by_pct': 0.5,
	'dsp_campaign_top_changers_by_pct': 0.5
}

emails = {
	'from': 'ssu@pulsepoint.com',
	'to': 'ssu@pulsepoint.com' #['analysts@pulsepoint.com', 'VXavier@pulsepoint.com'] #'VXavier@pulsepoint.com'/ analysts mwojcik@pulsepoint.com
}





def run_app(acct_type, change_type, queries, ):
	df = load_data(sql, fname)
	processed_data = run_data(df)
	formatted_data = format_data(processed_data)
	email(formatted_data)




def email(df):
	acctid_array, accts, headers, value = transform_data(df)
	pub = get_topdrop(acctid_array, query['DSP-PUB'], 'dsp_pub', 2, 'publisher','rev_difference', 'rev_delta', '* Top drop pubs: ', add_link=True)
	landingpages = get_topdrop(acctid_array, query['LANDINGPAGE'], 'dsp_landingpage', 1, 'landingpagedomain', 'difference', 'delta', '* Top drop campaigns: ', add_link=False)
	datacenters = get_topdrop(acctid_array, query['DC'], 'dsp_dc', 1, 'dc', 'difference', 'delta', '* Change by DataCenter: ', add_link=False)
	channels = get_topdrop(acctid_array, query['CHANNEL'], 'dsp_channel', 1, 'channel', 'difference', 'delta', '* Change by Channel: ', add_link=False)
	html = EmailAlert(data_directory+'dsp', data_directory+'input.mjml', accts, pub, landingpages, datacenters, channels, headers, value)	
	html.render_template()
	html.send_email('DSP Daily Droppers', me, you)




# #run_app(query['DSP'], "dsp_kpi")