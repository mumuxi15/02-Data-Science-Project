#!/usr/bin/env python3

import itertools
import spacy
import calendar
import logging
# import parameters
from util import * 

def print_heading(x):
	return ('-'*20+x+'-'*20)

def calculate_cogs():
	df = pd.read_csv('data/COGS.csv').groupby(['Category']).sum().reset_index()
	df['USD']=df['RMB']/USDCHN
	df['w'] = df['Category'].map(WEIGHT)*df['Quantity']
	df['Weight'] = df['w']/(df['w']).sum()
	extra_cost = df.loc[df['w'].isnull(),'USD'].sum()
	df['COGS'] = df['USD']+extra_cost*df['Weight']	
	return (df.loc[df['w'].notnull(),['Category','COGS','Quantity']]).set_index("Category")


def calculate_revenue():
	logging.info(print_heading(' Calculate Revenue  '))     
	return (data.groupby(['Year']).agg({'Item Gross':'sum'}).rename(columns={'Item Gross':'Revenue'}))
	
	
def calculate_profit(df):
	print_heading(' PROFIT ')
	return pd.pivot_table(
						df.groupby(['Category']).sum(), 
						values = ['Item Gross Revenue','Item Net Revenue','Item Sold','Shipping','Listing Fee'], 
						index = 'Category', 
		).fillna(0)


def sale_summary(data):
#   ############  Item sold   #############    
	'per item:  pieces in each variation'
	print('\nITEM SOLD ')
	
	df = data.copy()
	mask = lambda x: (df['Category']== x )
	df['Per Item'] = df['Variations'].str.extract('(\d+)')
	df.loc[mask('figure'), 'Per Item']=(df.loc[mask('figure'), 'Price']/10).round(0)
	df.loc[mask('fold bag'), 'Per Item']=(df.loc[mask('fold bag'),'Price']/5).round(0)
	df.loc[mask('bracelet')&(df['Variations'].str.contains('pair')), 'Per Item'] = 2
	df['Per Item'] = df['Per Item'].fillna(1).astype(int)
	
	df['Item Sold'] = df['Quantity'].mul(df['Per Item'])
	df['Date'] = df['Sale Date'].dt.to_period('M')
	sold = pd.pivot_table(
						df.groupby(['Date','Category']).sum(), 
						values = 'Item Sold', 
						index='Date', 
						columns = 'Category', 
		).fillna(0)
	print(sold.astype(int).tail(4))
	
	
	############  Inventory Check   #############    
	print('\nInventory Check  (Have at least 3 Month supply) ')
	cost = calculate_cogs()
	inventory = cost['Quantity']
	inv = pd.concat([ inventory.rename('No. Purchased'),sold.sum().rename('No. Sold')],axis=1)
	inv['Minimum Line']= sold.tail(3).sum()
	inv['Inventory'] = inv['No. Purchased'] - inv['No. Sold']
	inv = inv.astype(int)
	inv['Status'] = (inv['Inventory'] <= inv['Minimum Line']).map({True:'Low',False:'-'})
	print(inv.T)




if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	orders = load_orders(begin=2021, end=2022)
	logging.info(print_heading(' Data Loaded  '))     
	logging.info(print_heading(' Generate Sale Report  '))     
	sale_summary(orders)
	