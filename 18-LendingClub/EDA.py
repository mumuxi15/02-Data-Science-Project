from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm 
import seaborn as sns
import itertools
import random
import os, sys
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 1000)
cmap = plt.colormaps["tab20"]
DATA_PATH = os.getcwd()+'/18-LendingClub/data' if 'LendingClub' not in os.getcwd() else os.getcwd()+'/data'




def extract_loan_sample(p):
	''' p % of the lines  '''
	
	meta_cols = pd.read_csv(DATA_PATH+'/LCDataDictionary.csv',
					index_col=['LoanStatNew']).index.to_list()
	
	df = pd.read_csv(DATA_PATH+'/Loan_status_2007-2020Q3.gzip', 
					skiprows=lambda i: i>0 and random.random() > p, 
					usecols = meta_cols,
					low_memory=False)
				
	df['fico_score']  =  (df['fico_range_high']+df['fico_range_low'])/2.0
	df['issue_d'] = pd.to_datetime(df['issue_d'], format='%b-%Y')
	df = df.drop(columns=['fico_range_high','fico_range_low','emp_title'])
	
	#############  Cleaning    #####################
	df = df.loc[df['loan_status'].isin(['Fully Paid','Charged Off'])]
	
	#########  Preprossing     ############
	df['emp_length'] = df['emp_length'].replace('< 1 year','0').str.extract('(\d+)'
	).astype(float)
	df['int_rate'] = df['int_rate'].str.rstrip('%').astype('float') / 100.0
	df['earliest_cr_line'] = pd.to_datetime(df['earliest_cr_line'], format="%b-%Y")
	df['earliest_cr_line'] = df['earliest_cr_line'].dt.year
	
	print ('sample size :', len(df))
	loan_status = df['loan_status'].value_counts(normalize=True)
	print (loan_status)
	return df


def corr_heatmap(data):
	df = data.copy()
	col = list(df)
	col[0], col[1] = col[1], col[0] #swap column orders
	df['loan_status'] = df['loan_status'].map(dict({'Fully Paid':1, 'Charged Off':0}))
	corr = df[col].corr(numeric_only=True)
	err = corr[(corr>0.8)&(corr<1)].dropna(how="all").dropna(axis="columns",how="all")
	if len(err)>0:
		print('Multicollinearity Exists')
		print (err)
		
	f, ax = plt.subplots(figsize=(11, 9))
	cmap = sns.diverging_palette(220, 10, as_cmap=True)
	# Draw the heatmap with the mask and correct aspect ratio
	sns.heatmap(corr.round(2), cmap=cmap, vmax=0.2, vmin=-0.2, center=0,square=True, 
				linewidths=.5, cbar_kws={"shrink": .5}, annot=True)


def analysis_on_grade(data):
		col = ['loan_status','term','grade','sub_grade','int_rate']
		df = data[col].copy()
	
		fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))
	
		# -------    Grade    ----------
		factor = 'grade'
		status = df.groupby([factor,'loan_status']).agg({factor:  'count','int_rate':'mean'}
							)[factor].unstack(level=1)
		status['Count'] = status.sum(axis=1)
		status['Default Rate'] = status['Charged Off']/status['Count']*100        
		status['Paid Rate']    = status['Fully Paid']/status['Count']*100 
		status['Count pct'] = 100*status['Count']/status['Count'].sum(axis=0)
	
		status.plot(y='Default Rate',ax=ax[0,0], color='r', linestyle='dashed')
		status[['Default Rate','Paid Rate']].plot.bar(rot=0, ax=ax[0,0], color=cmap([7,1]))    
		ax[0,0].legend(loc='upper right')
		ax[0,0].set_ylabel('%')
		ax[0,0].set_title('Default Rate of Different Loan Grade')
	
		#pie chart: outer ring 
		cm = plt.get_cmap("tab20c")
		status.plot(
				y     ='Count pct',
				kind  ='pie',
				legend=False,
				autopct=lambda v: f'{v:.1f}%', pctdistance=1.3,
				radius=1, wedgeprops=dict(width=0.3, edgecolor='w'),
				colors=cm(np.arange(3)*4),
				ax=ax[0,1]
		)
		ax[0, 1].set_title('Loan Class Distribution')
	
#     display(status)
		# -------   Sub Grade   ----------
		factor = 'sub_grade'
		status = df.groupby([factor,'loan_status']
											).agg({factor:  'count','int_rate':'mean'}
											)[factor].unstack(level=1)
		status['Count'] = status.sum(axis=1)
		status['Default Rate'] = status['Charged Off']/status['Count']*100        
		status['Paid Rate']    = status['Fully Paid']/status['Count']*100 
		status['Count pct'] = 100*status['Count']/status['Count'].sum(axis=0)
	
		status.plot(y='Default Rate',ax=ax[1,0], color='r', linestyle='dashed')
		status[['Default Rate','Paid Rate']].plot.bar(rot=90, ax=ax[1,0], color=cmap([7,1]))    
		ax[1,0].legend(loc='upper right')
		ax[1,0].set_ylabel('%')
		ax[1,0].set_title('Default Rate of Different Loan Grade')
	
		status.plot.bar(y=['Charged Off', 'Fully Paid'], 
								color=cmap([7,1]),
								rot=90, ax=ax[1,1], stacked=True
							) 
	
		#pie chart: inner ring 
#     display(status)
		label     = status.index.values
		label = list(label[0:20])+[' ']*(len(label)-20) 
		status.plot(
				y = 'Count pct',
				kind='pie',
				radius=0.7, wedgeprops=dict(width=0.3, edgecolor='w'),
				colors=cm([i//5*4+x for i, x in enumerate(list([0,1,2,3,3])*6)]),
				labels=label, legend=False,
				ax=ax[0,1]
		)
		ax[0,0].legend(loc='upper right') 
		ax[0,0].set_ylabel('%')
		ax[0,0].set_title('Default Rate of Different Grades')
		ax[0,1].set_ylabel('')
		ax[1,0].legend(loc='upper right') 
		ax[1,0].set_ylabel('%')
		ax[1,0].set_title('Default Rate of Different Sub Grades')
		ax[1,1].legend(loc='upper right') 
		ax[1,1].set_title('Sub Grade Distribution ')
		ax[1,1].set_ylabel('Counts')
	
	
	
def analysis_on_application(data):
		cols = ['loan_status','application_type','term','verification_status','purpose']
		df = data[cols].copy()
		gp = df.set_index('loan_status'
						).stack().groupby('loan_status'
						).value_counts().unstack(fill_value=0)
		
		fig, ax = plt.subplots(nrows=4, ncols=2, figsize=(12, 15))
		
		p = list(itertools.product(range(0,2), range(0,2)))
		cmap = plt.colormaps["tab20c"]
		for idx, col in enumerate(cols[1::]):
			status = gp[list(df[col].unique())].T
			status['Count'] = status.sum(axis=1)
			status['Default Rate'] = status['Charged Off']/status['Count']*100
			status['Count pct'] = status['Count']/status['Count'].sum(axis=0)*100
			status = status.sort_values(by='Default Rate', ascending=False)   #sort
			status['Label'] = status.index
			
			if len(status.index)>5:
				status['Label'] = status.apply(lambda x: x.name if x['Count pct'] >5 else ' ', axis=1)
				
			status.plot(
				kind='pie', 
				y   ='Count',
				autopct=lambda v: f'{v:.1f}%' if v>2 else '', 
				labels=status['Label'],
				legend=False,
				ax=ax[idx,1],
				colors=cmap(np.linspace(0.3, 1, status['Charged Off'].nunique())),
				fontsize=7)
			status.plot.bar(y='Default Rate',
								color=cmap(np.linspace(0.3, 1, status['Charged Off'].nunique())),
												legend=False, 
												ax=ax[idx,0], 
												rot=0) 
			ax[idx,1].set_ylabel('')
			ax[idx,1].set_title(col)
			ax[idx,0].set_ylabel('Default Rate %')
		ax[0,1].set_title('application type composition')
		ax[0,0].set_title('Charged Off Rate')
		ax[3,0].tick_params(axis='x', rotation=90)
		
		

loans = extract_loan_sample(p=0.03)
#corr_heatmap(loans)
#analysis_on_grade(loans)
#analysis_on_application(loans)
#plt.show()