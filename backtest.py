from yahoo_fin.stock_info import get_data
import yahoo_fin.stock_info as si
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta



# current strategy:
# bkward function: returns % gains for entire universe
# fwd function: returns % gains for entire universe
# winner function: Mess/clusterF


#new strategy

# bkwd function: input(mkt data, lookback window); output(% return)
# fwd function: input(mkt data, lookfwd window); output(% return)
# backtest: inpt(mkt data, lookback window, lookfwd window, lookback threshold, comparison stock); output(date bought, stocks bought, date sold, return by stock, begin price, end price)



dow_list = si.tickers_dow()
ndx_list = si.tickers_nasdaq()
spx_list = si.tickers_sp500()

amazon_weekly= get_data("amzn", start_date="12/04/2009", end_date="12/04/2019", index_as_date = True, interval="1wk")

dow_data = {}


def get_stock_data_historical(list_of_tickers, start, end, interval, baseline_ticker):
	base_data = get_data(baseline_ticker, start_date=start, end_date=end, index_as_date = True, interval=interval)[['close']]
	base_data.rename(columns = {'close':baseline_ticker}, inplace = True)
	for ticker in list_of_tickers:
		try:
			temp = get_data(ticker, start_date=start, end_date=end, index_as_date = True, interval=interval)[['close']]
			temp.rename(columns = {'close':ticker}, inplace = True)
			base_data = base_data.merge(temp,how='left',left_index=True, right_index=True)
		except Exception:
			pass
	return base_data

dow_historical_data = get_stock_data_historical(dow_list,"12/04/2017","12/04/2019", "1wk", "spy")



def compute_backward_return(historical_data, period):
	output = historical_data
	output = output.rolling(window=period+1).apply(lambda x: 100.0*(x.iloc[period] - x.iloc[0])/x.iloc[0])
	return output


def compute_forward_return(historical_data, period):
	output = historical_data
	output = output.sort_index(ascending=False).rolling(window=period+1).apply(lambda x: 100.00*(x.iloc[0] - x.iloc[period])/x.iloc[period]).sort_index(ascending=True)
	return output



def calibrator(mkt_data, lookback_window, lookfwd_window, lookback_threshold, baseline_stock):
	# compute loockback returns
	# dtermine which stocks are lookback winners,
	# compute fwd returns 
	# output(date bought, stocks bought, date sold, return by stock, begin price, end price)
	# output df: rows = date, columns = list of stocks, date sold, list of return, list of begin price, list of end price
	loockback_returns = compute_backward_return(mkt_data,lookback_window).iloc[lookback_window : -lookfwd_window , :]
	loockback_returns_relative = loockback_returns.sub(loockback_returns[baseline_stock],axis=0) # returns vs baseline
	lookback_winners = loockback_returns_relative.applymap(lambda x: 1 if x > lookback_threshold  else 0)
	#need to remove spy from averages
	lookfwd_returns = compute_forward_return(mkt_data,lookfwd_window).iloc[lookback_window:-lookfwd_window, :]
	lookfwd_returns_relative = lookfwd_returns.sub(lookfwd_returns[baseline_stock],axis=0)
	winner_fwd = lookfwd_returns_relative.multiply(lookback_winners).reset_index()
	winning_stocks = lookback_winners.apply(lambda row: row[row == 1].index.values.tolist(), axis=1).to_frame() # this creates a dataframe with each row as list of winning stocks, date is index
	winning_stocks.columns = ['tickers']
	winning_stocks = winning_stocks.reset_index()
	list_of_gains = [['']]*len(winning_stocks)
	for ind in winning_stocks.index:
		ticker_list = winning_stocks.loc[ind]['tickers']
		list_of_gains[ind] = winner_fwd.loc[winner_fwd.index == ind, ticker_list].values.flatten().tolist()
	winning_stocks['gains'] = list_of_gains
	winning_stocks['num_stocks'] = winning_stocks.apply(lambda x: len(x['tickers']), axis = 1)
	winning_stocks['sell_date'] = winning_stocks.apply(lambda x: x['index']+timedelta(days=lookfwd_window*7), axis = 1)
	return winning_stocks


winning_stocks = calibrator(dow_historical_data, 8,2,2.0,'spy')




with pd.ExcelWriter('output.xlsx') as writer:  
    out.to_excel(writer, sheet_name='Sheet_name_1')




####### This is in cleanup







