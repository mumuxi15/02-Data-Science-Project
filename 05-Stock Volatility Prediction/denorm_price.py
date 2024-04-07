#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib as mpl
import pyarrow.parquet as pq
import pandas as pd
import random
import os


files = []
for dirname, _, filenames in os.walk('input'):
    for filename in filenames:
        files.append(os.path.join(dirname, filename))
print (' ---  loading %d   files --- '%(len(files)))


def get_price(stock_id, book_trade, train_test='train'):
    return [f for f in files if f'stock_id={stock_id}/' in f and book_trade in f and train_test in f]

def plot_price(stock_id,time_id,price_name):
    " minimum difference in stock ticks are typically 0.01, so if we do 0.01/Pr_real ~ min_pr_norm/Pr_norm "
    df = pq.read_table(get_price(stock_id, 'book')[0]).to_pandas()
    df = df.query(f'time_id == {time_id}').drop(columns='time_id').set_index('seconds_in_bucket').reindex(np.arange(600), method='ffill')
    min_diff = np.nanmin(abs(df[price_name].diff().where(lambda x: x > 0))) #non null min of price in this period
    
    fig, ax = plt.subplots(nrows=3, ncols=1,  figsize=(15, 8),sharex=True,squeeze=True)
    
    df[price_name].plot.line(legend=False, ax=ax[0])
    ax[0].set_title(f'stock_id={stock_id}, time_id={time_id}: {price_name} normalized')
    
    df2 = df[price_name].diff().reset_index()
    df2.plot.bar(x='seconds_in_bucket', y=price_name, color=np.where(df2[price_name] > 0, 'g', 'r'), legend=False, edgecolor='none', width=1, ax=ax[1]).grid(axis='y',linestyle='--')
    ax[1].set_title(f'stock_id={stock_id}, time_id={time_id}: {price_name} change')
    ax[1].yaxis.set_major_locator(mpl.ticker.MultipleLocator(1))
    ax[1].set_xticks([])
    
    
    df[price_name+'_org'] = 0.01 / min_diff * df[price_name]
    df[price_name+'_org'].plot.line(legend=False, ax=ax[2])
    ax[2].set_title(f'stock_id={stock_id}, time_id={time_id}: {price_name} original')
    
    plt.show()
    

#def calc_price(df):
#   diff = abs(df.filter(like='price').diff())
#   min_diff = np.nanmin(diff.where(lambda x: x > 0))
#   n_ticks = (diff / min_diff).round()
#   return 0.01 / np.nanmean(diff / n_ticks)
#
#
#df_prices = df_book.groupby(['stock_id', 'time_id']) \
#   .progress_apply(calc_price).to_frame('price').reset_index()
#   
#sns.stripplot(data=df_prices, x='price', y='stock_id', orient='h')

plot_price(stock_id=1,time_id=16,price_name='ask_price1')