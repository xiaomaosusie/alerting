import pandas as pd 
from process_data import process_data

class insights(object):
	"""docstring for insights"""
	def __init__(self, df):
		super(insights, self).__init__()
		self.df = df 

	def top_changers(self, accountids_str, dimension, default_message, link=None):
		accountids = accountids_str.split(",")
		result = []
		for acct in accountids:
			acct_df = self.df[self.df['accountid'] == int(acct)]
			if len(acct_df) == 0:
				string = default_message
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

	def facts(self, accountids_str, dimension, default_message):
		accountids = accountids_str.split(",")
		result = []
		formatted = process_data(self.df)
		df = formatted.format_data(self.df)
		for acct in accountids:
			acct_df = df[df['accountid'] == int(acct)]
			if len(acct_df) == 0:
				string = default_message
			else:
				string = "* Changes by " + dimension + ": "
				selectedCols = acct_df[[dimension, 'difference_cur', 'delta_pct']]	
				for i in range(len(selectedCols)):
					val = ', '.join([str(i) for i in selectedCols.iloc[i]])
					string = string + val + ";  "
			result.append(string)
		return result