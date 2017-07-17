import os, sys, datetime, datetime
import glob
import pandas as pd
from sqlalchemy import create_engine

database = "impala://impala.pulse.prod" 
directory = "C:/Users/ssu/Documents/github/alerting/"
prior_day = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")
current_day = datetime.datetime.now().strftime("%Y%m%d")

class PPData(object):
	"""docstring for data"""

	def __init__(self, sql_template):
		super(PPData, self).__init__()
		self.sql_template = sql_template

	def custom_sql(self, param=None):
		with open(directory + self.sql_template) as f:
			if param is None:
				query = f.read().strip()  
			else: 
				query = f.read().strip().format(param)
		return query 

	def get_data(self, fname, param=None):
		filename = os.path.join(directory, "{}_{}.pkl".format(fname, current_day))
		if os.path.exists(filename) is False:
			df = pd.read_sql(self.custom_sql(param), create_engine(database))
			df.to_pickle(filename)
		else:
			df = pd.read_pickle(filename)
		return df

	def remove_data(self):
		files = glob.glob(directory + "*" + prior_day + "*")
		if len(files) > 0:
			for f in files:
				os.remove(f)
		else:
			print("No files removed: no files as of the day requested")
			pass 