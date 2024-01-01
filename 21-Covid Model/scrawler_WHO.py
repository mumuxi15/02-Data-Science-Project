import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import json
import requests as re

country_code = {'CHN':['wpro','cn'],'USA':['amro','us']} 


def predict(country):
	post_url = "https://covid19.who.int/page-data/region/%s/country/%s/page-data.json"%(country_code[country][0],country_code[country][1])
	
	print (post_url)
	try:
		res = re.get(post_url, timeout=10)
		status_code = res.status_code
	except re.exceptions.ConnectionError:
		status_code = 'CONNECTION ERROR'
	if status_code != 200:
		print ('___'*20, status_code)
		return 'STATUS ERROR'
	
	json_data = json.loads(res.json()['result']['data']['countryGroup']['data'])
	cols = ['date','_']+[x['name'] for x in json_data['metrics']]
	df = pd.DataFrame(data=json_data['rows'], columns=cols)
	df['date'] = pd.to_datetime(df['date'],utc=True,unit='ms').dt.date
	df.drop(columns=['_'],inplace=True)	
#	print (df.describe().T) 
#	print (df.loc[df['Deaths']<0]) # abnormal data neg daily death 
	df = df.loc[df['Deaths']>0]
	print (df)
#	print (df.describe().T)

	
#	df.to_csv('data/covid_cn.csv')
#	print (df.dtypes)
#	df = pd.read_csv('data/covid_countries.csv',parse_dates=['date'],index_col=['date'])
#	df = df.loc[df.index<'2023-01-11']
#	plt.plot(df['active_china'])
#	print (df)
##	print (df)
#	
#	
#	
#	confirm = np.array(data['total'])
#	scaler = np.max(confirm)
#	confirm = confirm/(scaler)
#
#
#	x = np.arange(len(confirm))
#	# curve fit
#	popt, pcov = curve_fit(logistic_function, x, confirm,maxfev=2000)
#	#predit future
#	predict_x = list(x) + [x[-1] + i for i in range(1, 1 + predict_days)]
#	predict_x = np.array(predict_x)
#	predict_y = logistic_function(predict_x, popt[0], popt[1], popt[2])
#	plt.figure(figsize=(15, 8))
#	plt.plot(x, confirm, 's',label="confimed infected number")
#	plt.plot(predict_x, predict_y, '--',label="predicted infected number")
#	plt.xticks(rotation=90)
#	plt.yticks(rotation=90)
#	
#	plt.suptitle("Coronavirus cases prediction in %s for the next %d days (Pred = %d,  r=%.2f)"%(c.capitalize(),predict_days,scaler*predict_y[-1], popt[2]), fontsize=12, fontweight="bold")
#	plt.title("Predict time:{}".format(time.strftime("%Y-%m-%d", time.localtime())), fontsize=16)
#	plt.xlabel('date', fontsize=14)
#	plt.ylabel('infected number', fontsize=14)
	plt.show()
 
predict(country='USA')
#predict(country='CHN')