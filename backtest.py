from yahoo_fin.stock_info import get_data
import yahoo_fin.stock_info as si
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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

def compute_backward_return(historical_data, period):
	output = historical_data
	output = output.rolling(window=period+1).apply(lambda x: 100.0*(x.iloc[period] - x.iloc[0])/x.iloc[0])
	return output


def compute_forward_return(historical_data, period):
	output = historical_data
	output = output.sort_index(ascending=False).rolling(window=period+1).apply(lambda x: 100.00*(x.iloc[0] - x.iloc[period])/x.iloc[period]).sort_index(ascending=True)
	return output

def is_winner(bwd_return, fwd_return, tickers, backward_threshold): 
	backward = bwd_return.sub(bwd_return['spy'],axis=0)
	forward = fwd_return.sub(fwd_return['spy'],axis = 0)
	winners = fwd_return*0.0
	for i in tickers:
		backward[i] = bwd_return[i].apply(lambda x: 1 if x >backward_threshold  else 0)
		forward[i] = fwd_return[i].apply(lambda x: 1 if x >3  else 0)
		winners[i] = backward[i]*forward[i]
	return backward.fillna(0),forward.fillna(0),winners.fillna(0)

def backtest(backward_winners, returns, tickers):
	returns1 = returns.sub(returns['spy'],axis = 0)
	pnl = returns*0.0
	for i in tickers:
		pnl[i] = backward_winners[i]*returns1[i]
	return pnl.to_numpy().sum()/backward_winners.to_numpy().sum()


def backtest2(
	daily_prices, 
	bwd_window, 
	backward_threshold, 
	fwd_window,
	tickers
	):
	# daily_prices = raw data
	# bwd_window = # of weeks to calc return %
	# backward_threshold = % gain which we will consider as a winner
	# fwd_window = $ of weeks to calc return %
	# returns the avg fwd return across all "winners"
	bwd_return = compute_backward_return(daily_prices,bwd_window)
	fwd_return = compute_forward_return(daily_prices,fwd_window)
	backward,forward,winners = is_winner(bwd_return,fwd_return,tickers, backward_threshold)
	final = backtest(backward,forward,tickers)
	return final

def ann_return(nweek_return, bwd_window):
	exp = 52.0/bwd_window
	# return [(nweek_return+1)**(exp)-1]*100.00
	return (((nweek_return)/100.00+1.0)**(exp) - 1.0)*100.00

######################################### execute script ########################################################
dow_historical_data = get_stock_data_historical(dow_list,"12/04/2017","12/04/2019", "1wk", "spy")
bwd_return = compute_backward_return(dow_historical_data,10)
fwd_return = compute_forward_return(dow_historical_data,2)



backward,forward,winners = is_winner(bwd_return,fwd_return,dow_list, 15)


final_pnl = backtest(backward,one_week_return.fillna(0),dow_list)

testing = backtest2(dow_historical_data,5,5,2,dow_list)


backward_window = list(range(8,14)) ## x axis
backward_threshold = list(range(8,14)) ## y axis
forward_window = list(range(1,7))



# below is a sample code which runs avg pnl across a range of inputs. Need to put these entries into an array
for i in range(len(backward_window)):
	for j in range(len(backward_threshold)):
		Z[i][j] = backtest2(dow_historical_data,backward_window[i],backward_threshold[j],2,dow_list)
		

backtest2(dow_historical_data,8,9,2,dow_list)




lists = [backward_window, backward_threshold, forward_window]

df1 = pd.DataFrame(list(itertools.product(*lists)), columns=['backward_window', 'backward_threshold', 'forward_window'])

df1['n-week return'] = df1.apply(lambda row : backtest2(dow_historical_data, row['backward_window'].astype(int), row['backward_threshold'],row['forward_window'],dow_list), axis = 1)
df1['annual return'] = df1.apply(lambda row : ann_return(row['n-week return'], row['forward_window']), axis = 1)

out = df1.sort_values(by='annual return', ascending=False)




with pd.ExcelWriter('output.xlsx') as writer:  
    out.to_excel(writer, sheet_name='Sheet_name_1')




####### This is in cleanup







