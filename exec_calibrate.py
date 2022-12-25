from yahoo_fin.stock_info import get_data
import yahoo_fin.stock_info as si
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from backtest.py import calibrator

############ assign parameters #################

dow_list = si.tickers_dow()
dow_historical_data = get_stock_data_historical(dow_list,"12/04/2017","12/04/2022", "1wk", "spy")

def gen_key(lb_window,lf_window,lb_threshold):
	return str(lb_window) + str(lf_window) + str(lb_threshold)

def get_loc(lb_window,lf_window,lb_threshold):
	x = (lb_window - 5)*(lf_window)*(lb_threshold-1)

def get_sampling_window(df): ### this function returns the sampling window which best predicts fwd performance
	list_ = [1.0]*50
	for i in range(50):  #### or len(df). 50 is a placeholder
		x = df[['pct_gain']].copy()
		x['rolling_avg'] = x['pct_gain'].rolling(i+1).mean()
		woo = x.assign(diff=abs(x['pct_gain'].shift(-1)-x['rolling_avg'])).dropna()['diff'].mean()
		list_[i] = woo
	# print(list_)
	return list_.index(min(list_)) + 1 ## this is the appropriate sampling window




lookback_windows = list(range(6,13))
lookfwd_windows = list(range(1,7))
lookback_thresholds = list(range(1,7))

baseline_stock = 'spy'

problem_size = len(lookback_windows)*len(lookfwd_windows)*len(lookback_thresholds)
keys = []*problem_size

winning_stocks = calibrator(dow_historical_data, 8,2,2.0,'spy')

################################ Need a function which stores dataframes in a list ###################################

df_dictionary = {}

for i in lookback_windows:
	for j in lookfwd_windows:
		for k in lookback_thresholds:
			key = gen_key(i,j,k)
			print(i,j,k)
			winning_stocks_temp = calibrator(dow_historical_data, i, j, float(k), 'spy')
			sampling_window = get_sampling_window(winning_stocks_temp)
			df_dictionary[key] = [winning_stocks_temp, sampling_window] ## 17 is a placeholder, will replace with the proper sampling window


################################ Need a function which calculates the right sampling window ###################################

# for i in len












