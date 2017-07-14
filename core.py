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

account_types = {
	"dsp" : 'dsp',
	"pub" : 'pub'
}

change_types = {
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

alert_params = {
	'account_rev_threshold': 1000,
	'pct_cutoff': 0.15,
	'absolute_cutoff': 5000,
	'dsp_pub_top_changers_by_pct': 0.5,
	'dsp_campaign_top_changers_by_pct': 0.5
}

emails = {
	'from': 'ssu@pulsepoint.com',
	'to': ['ssu@pulsepoint.com', 'ssu@pulsepoint.com'] #['analysts@pulsepoint.com', 'VXavier@pulsepoint.com'] 
}





def run_app(acct_type, change_type, sql_obj, link_obj, default_msg_obj, alert_param_obj, email_obj, jumper=False):
	data = pp_data(sql_obj[acct_type])
	#removed dated data
	data.remove_data()
	#email subject & email htmal filename
	email_subject = acct_type + " daily " + change_type
	filename = acct_type + "_" + change_type
	#generate new data	
	alertee_df = data.get_data(filename)
	processed = process_data(alertee_df)
	alertee = processed.get_alertee(acct_type, alert_param_obj['pct_cutoff'], alert_param_obj['absolute_cutoff'], alert_param_obj['account_rev_threshold'], jumper)
	if len(alertee) == 0:
		filename = 'default'
		no_alertee = email_alert.EmailAlert(filename)
		no_alertee.send_email(email_subject, email_obj['from'], email_obj['to'] )
	else: 
		ids, deep_dive_ids, accountnames, table_headers, table_value = processed.multiple_tables(alertee)

		#get pub data
		pub = pp_data(sql_obj['pub'])
		pub_df = pub.get_data('pub_' + change_type, deep_dive_ids)
		pub_processed = process_data(pub_df)
		pub_tops = pub_processed.top_by_pct_multi_accts(alert_param_obj['dsp_pub_top_changers_by_pct'], jumper)
		insight = insights(pub_tops)
		pub_res = insight.top_changers(ids, 'publisher', default_msg_obj['pub'], link_obj['Tableau_dsp_pub'])

		#get campaign data
		lan = pp_data(sql_obj['campaign'])
		lan_df = lan.get_data("campaign_" + change_type, deep_dive_ids)
		lan_processed = process_data(lan_df)
		lan_tops = lan_processed.top_by_pct_multi_accts(alert_param_obj['dsp_campaign_top_changers_by_pct'], jumper)
		insight2 = insights(lan_tops)
		cam_res = insight2.top_changers(ids, 'campaign', default_msg_obj['campaign'])

		#get channel data
		cn = pp_data(sql_obj['channel'])
		cn_df = cn.get_data("channel_" + change_type, deep_dive_ids)
		insight3 = insights(cn_df)
		cn_res = insight3.facts(ids, 'channel', default_msg_obj['channel'])

		#construct email content
		email_content = {
		"accountname": accountnames,
		"message1": pub_res,
		"message2": cam_res,
		"message3": cn_res,
		"theader": table_headers,
		"tvalue": table_value
		}

		#build email html & send email
		email = EmailAlert(filename)
		email.render_template(data_directory + 'input.mjml', email_content)
		email.send_email(email_subject, email_obj['from'], email_obj['to'])


run_app(account_types['dsp'], change_types['droppers'], dsp_queries, links, default_message, alert_params, emails, jumper=False)
run_app(account_types['dsp'], change_types['jumpers'], dsp_queries, links, default_message, alert_params, emails, jumper=True)