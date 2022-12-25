from yahoo_fin.stock_info import get_data
import yahoo_fin.stock_info as si
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta



# create a function which accepts a df of buy orders and outputs performance
# how to i do weighted avg performance

def generate_ledger(buy_orders, cash_start, fwd_holding_period):
	# buy_orders: buy_date | tickers | sell_date
	today = datetime(today)
	#suppose holding_period is 4 weeks, we need to invest 1/(4*4) of money each week
	#suppose holding_period is 5 weeks, we need to invest 1/(5*4) of money each week
	#suppose holding_period is 2 weeks, we need to invest 1/(2*4) of money each week
	#
	### Produce a ledger
	# going to generate a unique trade id for each date, store in a table. 
	# this table will have is_active flag, if sell_date > today's date
	# will have a pnl column, will be unrealized if is_active = 1, otherwise realized
	# going to have starting price column and finishing price column
	
	

def performance(ledger)
	#
	### produce a tracker by week
	# going to generate a table which shows week's date, starting value, ending value


