import pandas as pd
import numpy as np

class RSI():
    def __init__(self, period = 14, column='Close Price',u_level = 70, l_level = 30,date_column = 'Date'):
        self.period = period
        self.column = column
        self.u_level = u_level
        self.l_level = l_level
        self.date_column = date_column
        self.entry_date_list = []
        self.RSI = []
        self.RSI_gains = []
        self.RSI_gain_periods = []
    
    def calc_averages(self, array):
        positives = 0
        negatives = 0
        n_positives = 0
        n_negatives = 0
        for i in array:
            if i>=0:
                positives+=i
                n_positives+=1
            else:
                negatives+=-i
                n_negatives+=1
        return (positives/n_positives,negatives/n_negatives)
    
    
    def generate(self, df,calc_returns = False):
        self.clean(df)
        self.RSI = [None for _ in range(self.period)]
        self.RSI_gains = []
        self.RSI_gain_periods = []
        self.position = False
        self.entry_price = 0
        self.entry_date = 0
        self.entry_date_list = []
        
        
        returns = df[self.column].pct_change().dropna(axis = 0)
        avg_gain, avg_loss = self.calc_averages(returns.iloc[:self.period])
        self.RSI.append(100-100/(1+avg_gain/avg_loss))
        
        for i in range(self.period,len(returns)):
            gain = 0
            loss = 0
            if returns.iloc[i]>=0:
                gain = returns.iloc[i]
            else:
                loss = -returns.iloc[i]
            
            avg_gain = (avg_gain*(self.period-1)+gain)/self.period
            avg_loss = (avg_loss*(self.period-1)+loss)/self.period
            self.RSI.append(100-100/(1+avg_gain/avg_loss))
            if(calc_returns):
                self.calculate_returns(self.RSI[-2],self.RSI[-1],df[self.date_column].iloc[i+1],
                                       df[self.column].iloc[i+1])
        return np.array(self.RSI)
    
    
    def calculate_returns(self,prev_RSI,curr_RSI,curr_day,curr_price):
        if(prev_RSI<=self.l_level and curr_RSI>self.l_level and self.position==False):
            self.position = True
            self.entry_date = curr_day
            self.entry_price = curr_price
        elif(prev_RSI>=self.u_level and curr_RSI<self.u_level and self.position):
            self.RSI_gains.append((curr_price-self.entry_price)/self.entry_price)
            self.RSI_gain_periods.append((curr_day-self.entry_date).days)
            self.entry_date_list.append(self.entry_date)
            self.position = False
            #print('Sale Price = {}\n Purchase Price = {}\n Purchase Date = {}\n Sale Date = {}'.format(curr_price,
            #                                                                                          self.entry_price,
             #                                                                                     self.entry_date,
              #                                                                                        curr_day))
    def clean(self,df):
        df[self.date_column] = pd.to_datetime(df[self.date_column])
        df.sort_values(by = self.date_column,inplace = True)
        df.dropna(axis = 0, inplace = True) 
        
    def get_returns(self):
        return np.array(self.RSI_gains)
    
    def get_return_period(self):
        return np.array(self.RSI_gain_periods)
    
    def get_entry_dates(self):
        return np.array(self.entry_date_list)
    
    def get_summary(self):
        return np.vstack((self.get_returns(),self.get_return_period(),self.get_entry_dates())).T
        
        
        