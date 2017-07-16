import pandas as pd 
from process_data import ProcessData

class Insights(object):
	"""docstring for insights"""
	def __init__(self, df):
		super(Insights, self).__init__()
		self.df = df 

	def topline(self, jumper=False):
		df = self.df[['rev_diff_agst_pd_cur', 'is_deep_dive']]
		process = ProcessData(df).format_data(df)
		if jumper is False:
			change = 'dropped'
		else: 
			change = 'increased'
		process['topline'] = process.apply(lambda row: ('Account ' + change + ' <b>' + row['rev_diff_agst_pd_cur'] + '</b> agst prior day.') if row['is_deep_dive'] == 1 else ('The account ' + change + ' aganst 4(7)-day average. If expected, ignore the alert. O/w, please take a look.'), axis = 1)
		return process['topline']

	def top_changers(self, accountids_str, dimension, link=None):
		accountids = accountids_str.split(",")
		result = []
		for acct in accountids:
			acct_df = self.df[self.df['accountid'] == int(acct)]
			if len(acct_df) == 0:
				string = ''
			else:
				string = "* " + dimension + "s account for " + str(self.df['cutoff'][0]) + "% of " + str(self.df['flag'][0]) + ": "
				if link is None:
					selectedCols = acct_df[[dimension, 'difference_cur', 'delta_pct']]	
				else:
					selectedCols_ext = acct_df[[dimension, 'difference_cur', 'delta_pct', 'dsp']]
					selectedCols_ext[dimension] = "<a href='" + link + "dsp=" + selectedCols_ext['dsp'] + "&publisher=" + selectedCols_ext[dimension] + "' >" + selectedCols_ext[dimension] + '</a>'	
					selectedCols = selectedCols_ext[[dimension, 'difference_cur', 'delta_pct']]
				for i in range(len(selectedCols)):
					val = ', '.join([str(i) for i in selectedCols.iloc[i]])
					string = string + val + ";  "
			if acct_df['num_of_others'].mean() > 0:
				string = string + "and " + str(int(acct_df['num_of_others'].mean()))  + " more " + dimension + "(s). "
			result.append(string)
		return result

	def facts(self, accountids_str, dimension):
		accountids = accountids_str.split(",")
		result = []
		formatted = ProcessData(self.df)
		df = formatted.format_data(self.df)
		for acct in accountids:
			acct_df = df[df['accountid'] == int(acct)]
			if len(acct_df) == 0:
				string = ''
			else:
				string = "* Changes by " + dimension + ": "
				selectedCols = acct_df[[dimension, 'difference_cur', 'delta_pct']]	
				for i in range(len(selectedCols)):
					val = ', '.join([str(i) for i in selectedCols.iloc[i]])
					string = string + val + ";  "
			result.append(string)
		return result