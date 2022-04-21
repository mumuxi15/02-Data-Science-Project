#!/usr/bin/env python3
import pandas as pd
import numpy as np
from config import *

def csv_reader(name, begin, end):
	files = ['%s%d.csv'%(name,i) for i in range(begin,end+1)]
	return pd.concat([pd.read_csv('data/'+csv, parse_dates=['Sale Date']) for  csv in files])

def assign_category(df):
	df = df.apply(lambda x: x.str.lower() if(x.dtype == 'object') else x) 
	mapper = df.sort_values('Sale Date').drop_duplicates(['Listing ID'], keep='last')[['Item Name','Listing ID']]
	mapper['Category'] = mapper['Listing ID'].map(CATEGORY_DICT)
	mask = lambda x: (mapper['Category'].isnull())&(mapper['Item Name'].str.contains(x))
	mapper.loc[mask('sock'),'Category'] = 'sock'
	mapper.loc[mask('figure'),'Category'] = 'figure'
	mapper.loc[mask('enamel pin'),'Category'] = 'pin'    
	return pd.Series(mapper['Category'].values,index=mapper['Listing ID']).to_dict()

def load_orders(begin=2021, end=2022):
	orders = csv_reader(name='EtsySoldOrders', begin=begin, end=end) 
	# redefine order net n order total
	orders['Order Net'] = orders.apply(lambda x: x['Adjusted Net Order Amount'] if x['Adjusted Net Order Amount']!=0 else x['Order Net'], axis=1)
	orders['Order Revenue'] = orders['Order Value'] + orders['Shipping']
	orders['Order Net']     = orders['Order Net'] - orders['Order Total']*0.05
	orders = orders[list(set(orders.columns) & set(DATA_FIELDS))]
	
	items = csv_reader(name='EtsySoldOrderItems', begin=begin, end=end)
	items = items.loc[~items['Listing ID'].isin(DROP_ID)]         #drop unwanted listing id
	items['Category'] = items['Listing ID'].map(assign_category(items))
	items = items[list(set(items.columns) & set(DATA_FIELDS))]
	assert len(items[items['Category'].isnull()])== 0, 'Undefined listing, Edit mapper'
	
	cols_to_use = orders.columns.difference(items.columns).to_list()+['Order ID']
	df = pd.merge(
		items, orders[cols_to_use],
		how="left", on='Order ID',
		sort=True,indicator=False,
	)
	
	df['Shipping'] = (df['Category'].map(USPS_RATE).fillna(4))/df['Number of Items']*df['Quantity']+(df['Number of Items']-1)*0.25
	df['Listing Fee'] = 0.2
	df['Item Gross Revenue'] = df['Order Revenue']/df['Order Value']*(df['Item Total'])
	df['Item Net Revenue']   = df['Order Net']/df['Order Value']*(df['Item Total'])
	
	
	df['Year']   = df['Sale Date'].dt.year
	df['Month']  = df['Sale Date'].dt.month
	df['Quarter']= 'Q'+df['Sale Date'].dt.quarter.astype(str)
	
	return df