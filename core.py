import os, sys, datetime, datetime
import _pickle as cPickle
#import cPickle as pickle

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import functools
import json
 
from email_alert import EmailAlert
from pp_data import PPData
from process_data import ProcessData
from insights import Insights


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

alert_params = {
	'account_rev_threshold': 1000,
	'pct_cutoff': 0.15,
	'absolute_cutoff': 5000,
	'dsp_pub_top_changers_by_pct': 0.5,
	'dsp_campaign_top_changers_by_pct': 0.5,
	'tvalue_color': 0.2
}

emails = {
	'from': 'ssu@pulsepoint.com',
	'to': ['ssu@pulsepoint.com', 'VXavier@pulsepoint.com'] #['analysts@pulsepoint.com', 'VXavier@pulsepoint.com'] 
}

def run_app(acct_type, change_type, sql_obj, link_obj, alert_param_obj, email_obj, jumper=False):
	data = PPData(sql_obj[acct_type])
	#removed dated data
	data.remove_data()
	#email subject & email htmal filename
	email_subject = acct_type + " daily " + change_type
	html_name = acct_type + "_" + change_type
	#generate new data	
	alertee_df = data.get_data(html_name)
	processed = ProcessData(alertee_df)
	alertee = processed.get_alertee(acct_type, alert_param_obj['pct_cutoff'], alert_param_obj['absolute_cutoff'], alert_param_obj['account_rev_threshold'], jumper)
	#if no alertees the app will generate a default html 
	if len(alertee) == 0:
		print("no alertee for today.")
		html_name = 'default'
		no_alertee = EmailAlert(html_name)
		no_alertee.send_email(email_subject, email_obj['from'], email_obj['to'] )
	else: 
		#get top-line
		top_line = Insights(alertee).topline(jumper)

		#get table headers and values 
		ids, deep_dive_ids, accountnames, table_headers, table_value = processed.multiple_tables(alertee, alert_param_obj['tvalue_color'])

		#when there's no prior day changers, the app doesn't need to run/process pub/campaign/channel queries 
		if len(deep_dive_ids) == 0:
			default_msg = ['' for acct in accountnames]
		    #construct email content
			email_content = {
			"accountname": accountnames,
			"message0": top_line,
			"message1": default_msg,
			"message2": default_msg,
			"message3": default_msg,
			"theader": table_headers,
			"tvalue": table_value
			}
		else:	
			#get pub data
			pub = PPData(sql_obj['pub'])
			pub_df = pub.get_data('pub_' + change_type, deep_dive_ids)
			pub_processed = ProcessData(pub_df)
			pub_tops = pub_processed.top_by_pct_multi_accts(alert_param_obj['dsp_pub_top_changers_by_pct'], jumper)
			insight1 = Insights(pub_tops)
			pub_res = insight1.top_changers(ids, 'publisher', link_obj['Tableau_dsp_pub'])

			#get campaign data
			lan = PPData(sql_obj['campaign'])
			lan_df = lan.get_data("campaign_" + change_type, deep_dive_ids)
			lan_processed = ProcessData(lan_df)
			lan_tops = lan_processed.top_by_pct_multi_accts(alert_param_obj['dsp_campaign_top_changers_by_pct'], jumper)
			insight2 = Insights(lan_tops)
			cam_res = insight2.top_changers(ids, 'campaign')

			#get channel data
			cn = PPData(sql_obj['channel'])
			cn_df = cn.get_data("channel_" + change_type, deep_dive_ids)
			insight3 = Insights(cn_df)
			cn_res = insight3.facts(ids, 'channel')

			#construct email content
			email_content = {
			"accountname": accountnames,
			"message0": top_line,
			"message1": pub_res,
			"message2": cam_res,
			"message3": cn_res,
			"theader": table_headers,
			"tvalue": table_value
			}

		#build html & send email
		email = EmailAlert(html_name)
		email.render_template(data_directory + 'input.mjml', email_content)
		email.send_email(email_subject, email_obj['from'], email_obj['to'])


run_app(account_types['dsp'], change_types['droppers'], dsp_queries, links, alert_params, emails, jumper=False)
run_app(account_types['dsp'], change_types['jumpers'], dsp_queries, links, alert_params, emails, jumper=True)