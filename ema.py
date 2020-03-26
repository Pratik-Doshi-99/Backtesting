import pandas as pd
import numpy as np

class EMA():
    def __init__(self, period_1 = 50, period_2 = 200, date_column = 'Date', column = 'Close'):
        self.s_period = period_1 #if period_1<period_2 else period_2
        self.l_period = period_2 #if period_1<period_2 else period_1
        self.date_column = date_column
        self.column = column
        self.sk = 2/(self.s_period+1)
        self.lk = 2/(self.l_period+1)
        self.ema_gains = []
        self.ema_gain_periods = []
        self.ema_spread = []
        self.entry_date_list = []
        
        '''
            ema_spread is positive when short period ema > long period ema
            ema_spread is negative when short period ema < long period ema
            if self.ema_spread[-1] is negative and current calculated ema is positive, buy call is generated
            if self.ema_spread[-1] is positive and current calculated ema is negative, sell call is generated
        '''
        
    
    def clean(self,df):
        df.dropna(axis = 0, inplace = True) 
        df[self.date_column] = pd.to_datetime(df[self.date_column])
        df.sort_values(by = self.date_column,inplace = True)
        
        
    def generate(self,df,calc_returns = False):
        self.clean(df)
        self.ema_spread = [None for _ in range(self.l_period-1)]
        
        #for calculating returns
        self.position = False
        self.entry_price = 0
        self.entry_date = 0
        self.ema_gains = []
        self.ema_gain_periods = []
        self.entry_date_list = []
        self.calc_average(df[self.column].iloc[0:self.l_period])
        
        
        for i in range(self.l_period,len(df)):
            self.l_last_avg = df[self.column].iloc[i]*self.lk + self.l_last_avg*(1-self.lk)
            self.s_last_avg = df[self.column].iloc[i]*self.sk + self.s_last_avg*(1-self.sk)
            #print(self.s_last_avg,self.l_last_avg)
            self.ema_spread.append(self.s_last_avg - self.l_last_avg)
            
            if(calc_returns):
                self.calculate_returns(self.ema_spread[-2],self.ema_spread[-1],df[self.date_column].iloc[i],
                                       df[self.column].iloc[i])
        return np.array(self.ema_spread)
        
        
    def calc_average(self, array):
        self.s_last_avg = array[-self.s_period:].mean()
        self.l_last_avg = array.mean()
        #print(self.s_last_avg,self.l_last_avg)
        self.ema_spread.append(self.s_last_avg - self.l_last_avg)
        
    def calculate_returns(self,prev_spread,curr_spread,curr_day,curr_price):
        if(prev_spread<=0 and curr_spread>0 and self.position==False):
            self.position = True
            self.entry_date = curr_day
            self.entry_price = curr_price
        elif(prev_spread>=0 and curr_spread<0 and self.position):
            self.ema_gains.append((curr_price-self.entry_price)/self.entry_price)
            self.ema_gain_periods.append((curr_day-self.entry_date).days)
            self.position = False
            self.entry_date_list.append(self.entry_date)
            #print('Sale Price = {}\n Purchase Price = {}\n Purchase Date = {}\n Sale Date = {}'.format(curr_price,
            #                                                                                          self.entry_price,
             #                                                                                     self.entry_date,
              #                                                                                        curr_day))
        
    def get_returns(self):
        return np.array(self.ema_gains)
    
    def get_return_period(self):
        return np.array(self.ema_gain_periods)
    
    def get_entry_dates(self):
        return np.array(self.entry_date_list)
    
    def get_summary(self):
        return np.vstack((self.get_returns(),self.get_return_period(),self.get_entry_dates())).T