#!/usr/bin/env python3

CATEGORY_DICT = {
	1022390097: 'car ornament', 
	1136058119:'wind chime',
	1142310315:'wind chime',
	1057888513:'planter',
	1102771997:'accessories',
	1105618585:'accessories',
	953074300: 'chair protector',
	1150682097:'towel',
	1021830721:'bag', 
	1142723497:'bracelet',
	1190196483:'coaster',
	}

DROP_ID = [1036136177,1031877031,1156104972] 


# Weight of each item in kg
WEIGHT = {
	'bracelet':0.02, 
	'accessories':0.006,
	'car ornament':0.015,
	'chair protector':0.025,
	'pin':0.005,
	'figure':0.1,
	'bag':0.06,
	'planter':1,
	'sock':0.06,
	'towel':0.283,
	'wind chime':0.45,
	'coaster':0.02,
}

DATA_FIELDS = [
	'Sale Date', 'Ship State', 'Variations',
	'Order ID', 'Listing ID', 'Category',
	'Price','Quantity','Number of Items',  
	'Item Total', 'Gross Revenue',
	'Order Value','Order Revenue','Order Net', 
	]
	
DROP_ID = [1036136177,1031877031,1156104972] 

USPS_RATE = {'planter':10,'towel':5}
USDCHN = 6.3