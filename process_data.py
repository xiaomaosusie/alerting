import pandas as pd 
import functools
import json
from pp_data import pp_data

class process_data(object):
	"""docstring for process_data"""
	def __init__(self, df):
		super(process_data, self).__init__()
		self.df = df 

	def get_dropper(self, segmentKey, pctCutoff, absoluteCutoff, acctCutoff):
		df = self.df.set_index(segmentKey)
		#apply account threshold, eliminating alerting on small accounts
		df = df[df['7davgrevenue'] >= acctCutoff]
		#apply alerting criteria 
		Crit1 = df.revenue_change_agst_pd_pct <= -pctCutoff * 100
		Crit2 = df.revenue_change_agst_4davg_pct <= -pctCutoff * 100
		Crit3 = df.revenue_change_agst_7davg_pct <= -pctCutoff * 100
		Crit4 = df.rev_diff_agst_pd_cur <= -absoluteCutoff
		CritList = [Crit1, Crit2, Crit3, Crit4]
		AllCrit = functools.reduce(lambda x, y: x | y, CritList)
		result = df[AllCrit]
		result['is_daily'] = result.apply(lambda row: 1 if row['revenue_change_agst_pd_pct'] <= -pctCutoff else 0, axis = 1) 
		sorted_res = result.sort_values(by = ['is_daily', 'revenue_cur'], ascending = [False, False])
		return sorted_res

	def get_jumper(self, segmentKey, pctCutoff, absoluteCutoff, acctCutoff):
		df = self.df.set_index(segmentKey)
		#apply account threshold, eliminating alerting on small accounts
		df = df[df['7davgrevenue'] >= acctCutoff]
		#apply alerting criteria 
		Crit1 = df.revenue_change_agst_pd_pct >= pctCutoff * 100
		Crit2 = df.rev_diff_agst_pd_cur >= absoluteCutoff * 100
		CritList = [Crit1, Crit2]
		AllCrit = functools.reduce(lambda x, y: x | y, CritList)
		result = df[AllCrit]
		return result

	def format_data(self, df):
		int_col = df[[col for col in df.columns if (('revenue' in col) | ('difference' in col))]]
		for col in int_col:
			df[col] = df[col].apply(lambda x: int(x))
		mm_col = df[[col for col in df.columns if ('mm' in col)]]
		for col in mm_col:
			df[col] = df[col].apply(lambda x: '{:,.0f}M'.format(x/1000000))
		currency_col = df[[col for col in df.columns if ('cur' in col)]]
		for col in currency_col:
			df[col] = df[col].apply(lambda x: '&#36;' + '{:,}'.format(x) if x >= 0 else '-&#36;' + '{:,}'.format(abs(x)))
		pct_col = df[[col for col in df.columns if ('pct' in col)]]
		for col in pct_col:
			df[col] = df[col].apply(lambda x: '{:.1f}%'.format(x)) 
		return df 

	def single_dsp_table(self, df):
		file_date = df['day'][0] 
		prior_day = df[['revenue_cur' , 'offer_mm' , 'offerrate_pct' , 'offermatchrate_pct' , 'bidrate_pct' , 'blockrate_pct' , 
				'winrate_pct' , 'revcpm_cur', 'costcpm_cur' , 'margin_pct' , 'timeoutrate_pct']]
		change_agst_ppd = df[['revenue_change_agst_pd_pct' , 'offer_change_agst_pd_pct' , 'offerrate_change_agst_pd_pct' , 'offermatchrate_change_agst_pd_pct' , 
							'bidrate_change_agst_pd_pct' , 'blockrate_change_agst_pd_pct' , 'winrate_change_agst_pd_pct' , 'revcpm_change_agst_pd_pct', 
							'costcpm_change_agst_pd_pct' , 'margin_change_agst_pd_pct' , 'timeoutrate_change_agst_pd_pct']]
		change_agst_4d = df[['revenue_change_agst_4davg_pct' , 'offer_change_agst_4davg_pct' , 'offerrate_change_agst_4davg_pct' , 'offermatchrate_change_agst_4davg_pct' , 
							'bidrate_change_agst_4davg_pct' , 'blockrate_change_agst_4davg_pct' , 'winrate_change_agst_4davg_pct' , 'revcpm_change_agst_4davg_pct', 
							'costcpm_change_agst_4davg_pct' , 'margin_change_agst_4davg_pct' , 'timeoutrate_change_agst_4davg_pct']]
		change_agst_7d = df[['revenue_change_agst_7davg_pct' , 'offer_change_agst_7davg_pct' , 'offerrate_change_agst_7davg_pct' , 'offermatchrate_change_agst_7davg_pct' , 
							'bidrate_change_agst_7davg_pct' , 'blockrate_change_agst_7davg_pct' , 'winrate_change_agst_7davg_pct' , 'revcpm_change_agst_7davg_pct', 
							'costcpm_change_agst_7davg_pct' , 'margin_change_agst_7davg_pct' , 'timeoutrate_change_agst_7davg_pct']]

		Col0 = pd.DataFrame({'metric': ['revenue', 'offer', 'offer rate', 'offermatch rate', 'bid rate', 'block rate', 
							'win rate', 'revcpm', 'costcpm', 'margin', 'timeout rate']})
		Col1 = prior_day.T.reset_index(drop=True)
		Col2 = change_agst_ppd.T.reset_index(drop=True)
		Col3 = change_agst_4d.T.reset_index(drop=True)
		Col4 = change_agst_7d.T.reset_index(drop=True)
		table_df = pd.concat([Col0, Col1, Col2, Col3, Col4], axis=1)
		table_df.columns = ['metric', file_date, 'change agst prior day', 'change agst 4-day avg', 'change agst 7-day avg']
		table_df.set_index('metric', drop=True)

		table_json = self.df_json(table_df)
		table_header = table_json['columns']
		table_val = table_json['data']
		return table_header, table_val	

	def multiple_tables(self, df):
		table_headers = []
		table_value = []
		accountnames = pd.Series(df.index)
		accountids = df['accountid'].iloc[:, 0]
		acctids_str = ", ".join([str(id) for id in accountids])
		deep_dive_acct = df[df['is_daily'] == 1]
		deep_dive_accountids = deep_dive_acct['accountid'].iloc[:, 0]
		deep_dive_acctids_str = ", ".join([str(id) for id in deep_dive_accountids])
		df = self.format_data(df)
		for name in accountnames:
			acct_data = df[df.index == name]
			table_header, table_val = self.single_dsp_table(acct_data)
			table_headers.append(table_header)
			table_value.append(table_val)
		return acctids_str, deep_dive_acctids_str, accountnames, table_headers, table_value	

	def df_json(self, df):
		json_str = df.to_json(orient='split')
		data = json.loads(json_str)
		return data 

	def changes(self, df, positive=True):
		df['flag'] = df['difference_cur'].apply(lambda x: 'increase' if x >=0 else 'drop')
		if positive is True:
			res = df[df['flag'] == 'increase']
			sorted_res = res.sort_values(by = ['difference_cur'], ascending = False)
		else:
			res = df[df['flag'] == 'drop']
			sorted_res = res.sort_values(by = ['difference_cur'], ascending = True)
		return sorted_res

	def top_by_pct(self, df, pct, positive=True):
		df = self.changes(df, positive)
		df["cum_pct"] = df['difference_cur'].cumsum()/df['difference_cur'].sum() * 100
		res = df[df['cum_pct'] <= pct * 100]
		res['num_of_others'] = len(res) - 5
		if len(res) == 0:
			res = df[:1]
		elif len(res) >= 5:
			res = df[:5]
		res['cutoff'] = int(pct * 100)
		return res

	def top_by_pct_multi_accts(self, pct, positive=True):
		accts = self.df['accountid'].unique()
		result = pd.concat([self.top_by_pct(self.df[self.df['accountid'] == acct], pct, positive) for acct in accts], ignore_index=True)
		result = self.format_data(result)
		return result


