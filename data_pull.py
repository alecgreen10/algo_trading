from yahoo_fin.stock_info import get_data
import yahoo_fin.stock_info as si
import pandas as pd


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

def is_winner(momentum, returns, tickers, backward_threshold): 
	backward = momentum.sub(momentum['spy'],axis=0)
	forward = returns.sub(returns['spy'],axis = 0)
	winners = returns*0.0
	for i in tickers:
		backward[i] = momentum[i].apply(lambda x: 1 if x >backward_threshold  else 0)
		forward[i] = returns[i].apply(lambda x: 1 if x >3  else 0)
		winners[i] = backward[i]*forward[i]
	return backward.fillna(0),forward.fillna(0),winners.fillna(0)

def backtest(backward_winners, returns, tickers):
	returns1 = returns.sub(returns['spy'],axis = 0)
	pnl = returns*0.0
	for i in tickers:
		pnl[i] = backward_winners[i]*returns1[i]
	return pnl.to_numpy().sum()/backward_winners.to_numpy().sum()

# need to build a function to remove duplicate winners
def remove dups():
	return 0

# need to generate a scatter plot where i vary the backward window, backward threshold, forward window

######################################### execute script ########################################################
dow_historical_data = get_stock_data_historical(dow_list,"12/04/2017","12/04/2019", "1wk", "spy")
four_week_momentum = compute_backward_return(dow_historical_data,10)
one_week_return = compute_forward_return(dow_historical_data,2)



temp = four_week_momentum.sub(four_week_momentum['spy'],axis=0)

temp['AAPL']=four_week_momentum['AAPL'].apply(lambda x: 1 if x >10  else 0)


backward,forward,winners = is_winner(four_week_momentum,one_week_return,dow_list, 10)



final = calc_stats(backward,forward,winners)
final_pnl = backtest(backward,one_week_return.fillna(0),dow_list)


##################################################################################################################


with pd.ExcelWriter('output.xlsx') as writer:  
    dow_historical_data.to_excel(writer, sheet_name='Sheet_name_1')
    four_week_momentum.to_excel(writer, sheet_name='Sheet_name_2')





