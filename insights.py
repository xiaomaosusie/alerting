class Insights(object):
	"""docstring for insights"""
	def __init__(self, acctid, df):
		super(Insights, self).__init__()
		self.acctid = acctid
		self.df = df

	def process_topdrop(self, dimension, difference, delta, strheader):
		res = []
		for acct in self.acctid:
			top = self.df[self.df['buyerid'] == acct]
			top = top.sort_values(by = [difference], ascending = [True])
			selectedCols = top[[dimension,difference, delta]]
			selectedCols[difference] = np.vectorize(currency)(selectedCols[difference])
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


		