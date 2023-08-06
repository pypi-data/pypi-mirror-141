# FMP Module for Target Prices

from ctypes import Union
import pandas as pd
import numpy as np
from typing import Type, Union

class Target_Price:
    """ 
    Options:

    Equals
    Greater Than
    Less Than
    Inside Channel
    Outside Channel
    Moving Up %
    Moving Down %
    Crossing Up
    Crossing Down
    Bouncing Up
    Bouncing Down
    
    """

    def __init__(self,
                 target_ticker:str,
                 price:float,
                 option:str = None,
                 price_data:pd.DataFrame = None,
                 target_price:Union[float,str]= None,
                 var_price:float = 10,
                 high_channel:Union[float,str] = None,
                 low_channel:Union[float,str] = None,
                 moving_up_pct:float = None,
                 moving_down_pct:float = None,
                 open:float = 'open',
                 high:float = 'high',
                 low:float = 'low'):

        self._price_data = price_data
        self._price = price
        self._target_ticker = target_ticker
        self._option = option
        self._target_price = target_price
        self._var_price = var_price
        self._high_channel = high_channel
        self._low_channel = low_channel
        self._moving_up_pct = moving_up_pct
        self._moving_down_pct = moving_down_pct
        self._open = open
        self._high = high
        self._low = low


    def set_prices(self,price_data):
      self._price_data = price_data

    def get_title(self):

      base = self._target_ticker + ' ' + self._option + ' '

      if self._option == 'Equals' or self._option == 'Greater Than' or self._option == 'Less Than':

        title = base + str(self._target_price)

      elif self._option == 'Inside Channel' or self._option == 'Outside Channel':

        title = base + str(self._low_channel) + ' and ' + str(self._high_channel)

      elif self._option == 'Moving Up %':
        title = base + str(self._moving_up_pct) + '%'

      elif self._option == 'Moving Down %':
        title = base + str(self._moving_down_pct) + '%'
      else:
        title = base

      return title

    
    def set_expired_alert(self):
        self._expired = True

    def reset_expiration(self):
      self._expired = False

    def get_price_df(self) -> pd.Series:

        if isinstance(self._price_data,tuple):
            return self._price_data[0]

        elif isinstance(self._price_data, pd.DataFrame):
            return self._price_data
        else:
            return self._price_data

    def get_target_series(self,df:pd.DataFrame, val:Union[float,int,str]):

        if isinstance(val,int) or isinstance(val,float):

            return val
        elif isinstance(val,str):

            return df[val]
        else:

            raise TypeError('Val must be either a float, int or col name')

    def get_target_price(self) -> pd.Series:

        """ 
        Return Target Price Series, if the target price is just a number,
        it will create a pd.Series the size of the given dataframe
        
        """

        price_data = self.get_price_df()

        if isinstance(self._target_price,float):

            tseries = pd.Series([self._target_price] * price_data.shape[0])

            tseries.index = price_data.index

            return tseries

        elif isinstance(self._target_price, pd.Series):

            return self._target_price

        elif isinstance(self._target_price, str):

            nseries = price_data[self._target_price]

            return nseries

        else:

            raise TypeError(f'Target Price must be either a float or a Pandas Series, its a ',type(self._target_price))



    def get_current_price(self) -> float:

        return self.get_price_df()[self._price]

        

    # Options Logic

    
    def equals(self,target_price=None): 
        
        price_df = self.get_price_df()

        target_price = self._target_price if target_price is None else target_price

        target_price = self.get_target_series(price_df,target_price)

        current_price = self.get_current_price()

        low_range = target_price - self._var_price

        high_range = target_price + self._var_price

        nseries = pd.Series(np.where((current_price <= high_range) & (current_price >= low_range),1,0))

        nseries.index = self.get_price_df().index 

        return nseries

    def greater_less_than(self,option:str,target_price=None):



        current_price = self.get_current_price()

        prices_df = self.get_price_df()

        target_price = self._target_price if target_price is None else target_price

        target_price = self.get_target_series(prices_df, target_price)

        if option == 'Greater Than':

            nseries = pd.Series(np.where(current_price > target_price,1,0))

            nseries.index = self.get_price_df().index

            return nseries
        
        elif option == 'Less Than':


            nseries = pd.Series(np.where(current_price > target_price,0,1))

            nseries.index = self.get_price_df().index

            return nseries

            
        else:
            raise ValueError(f'{option} as an option is  not supported. Must be either Greater Than or Less Than')
        
    def inside_outside_channel(self,option:str,high_channel_price=None,low_channel_price=None):

        price_df = self.get_price_df()

        if isinstance(self._high_channel,float):

            high_channel = self._high_channel if high_channel_price is None else high_channel_price
        
        elif isinstance(self._high_channel, str):

            high_channel_col = self._high_channel if high_channel_price is None else high_channel_price

            high_channel = price_df[high_channel_col]

        else:
            raise TypeError('High Channel must be either a col name or a float, its',type(self._high_channel))

        
        if isinstance(self._low_channel,float):

            low_channel = self._low_channel if low_channel_price is None else low_channel_price

        elif isinstance(self._low_channel, str):

            low_channel_col = self._low_channel if low_channel_price is None else low_channel_price

            low_channel = price_df[low_channel_col]

        else:
            raise TypeError('Low Channel must be either a col name or a float, its', type(self._low_channel))

        
        prices = self.get_current_price()


        if option == 'Inside Channel':

            nseries = pd.Series(np.where((prices <= high_channel) & (prices >= low_channel),1,0))

        elif option == 'Outside Channel':

            nseries = pd.Series(np.where((prices <= high_channel) & (prices >= low_channel),0,1))

        else:
            raise TypeError('Unsupported option, must be either Inside Channel or Outside Channel')

        nseries.index = price_df.index

        return nseries


    def moving_up_down_pct(self,option:str,target_price=None):

        current_price = self.get_current_price()

        price_df = self.get_price_df()

        target_price = self._target_price if target_price is None else target_price

        target_price = self.get_target_series(price_df,target_price)

        change = (current_price / target_price - 1) * 100

        prices_df = self.get_price_df()

        if option == 'Moving Up %':

            target_change = self._moving_up_pct

            nseries = pd.Series(np.where(change >= target_change,1,0))

        elif option == 'Moving Down %':

            target_change = self._moving_down_pct

            nseries = pd.Series(np.where(change <= target_change,1,0))

        else:

            raise TypeError('Unsupported option, must be either Moving Up % or Moving Down %')

        nseries.index = prices_df.index

        return nseries

    def crossing(self,option:str,target_price = None):

        price_df = self.get_price_df()

        # Check if Open is of a correct type
        if isinstance(self._open,float) or isinstance(self._open,int):
            open_price = self._open
        elif isinstance(self._open, str):
            open_price = price_df[self._open]
        else:
            raise TypeError('option must be either a float, int or column name')

        # Check if closing price has a correct type

        target_price_value = self._target_price if target_price is None else target_price

        target_price_series = self.get_target_series(price_df,target_price_value)


        if isinstance(self._price,float) or isinstance(self._price, int):
            close_price = self._price
        elif isinstance(self._price, str):
            close_price = price_df[self._price]
        else:
            raise TypeError('Close price must be either a float,int or column name')


        if option == 'Crossing Up':
            nseries = np.where((open_price < target_price_series) & (close_price > target_price_series), 1, 0)

        elif option == 'Crossing Down':
            nseries = np.where((open_price > target_price_series) & (close_price < target_price_series), 1, 0)
        else:
            raise TypeError('option must be either Crossing Up or Crossing Down')

        nseries = pd.Series(nseries)
        nseries.index = self.get_price_df().index

        return nseries

    def bouncing(self,option:str,target_price = None):

        price_df = self.get_price_df()

        def get_value(val) -> Union[float,int,pd.Series]:

            if isinstance(val, float) or isinstance(val, int):

                return val
            elif isinstance(val, str):

                return price_df[val]
            else:
                raise TypeError('Must be either a column name, float or int')

        close_price = get_value(self._price)

        open_price = get_value(self._open)

        low_price = get_value(self._low)

        high_price = get_value(self._high)

        target_price_val = self._target_price if target_price is None else target_price

        target_price_series = self.get_target_series(price_df,target_price_val)

        if option == 'Bouncing Up':

            bouncing_up_condition = (open_price > target_price_series) & (low_price <= target_price_series) & (close_price >= target_price_series)

            nseries = np.where(bouncing_up_condition,1,0)

        elif option == 'Bouncing Down':

            bouncing_down_condition = (high_price > target_price_series) & (close_price <= target_price_series) & (open_price <= target_price_series)

            nseries = np.where(bouncing_down_condition,1,0)

        else:

            raise TypeError('Option must be either Bouncing Up or Bouncing Down')

        nseries = pd.Series(nseries)
        nseries.index = price_df.index

        return nseries



        

        






    



        
        

    

    
