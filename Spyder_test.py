# -*- coding: utf-8 -*-

#dist = getattr(stats.stats, 'distribution name')
#params = dist.fit(data)

"""
Created on Wed Apr  8 21:15:06 2020

@author: ibratenkov001
"""

import pandas as pd
import requests
import re

import scipy.stats as st
from datetime import datetime


class Asset():

    def fit(self, 
            criteria = "SSE",
            dist = [st.norm, st.lognorm,st.alpha, st.beta, st.pareto]
            ):
        
        def SSE(x, y):
            return np.sum(np.power(y - x, 2.0)) 
          
        best_distribution = st.norm
        best_params = (0.0, 1.0)
        best_sse = np.inf



        for i in DISTRIBUTIONS:
            pass
        return i
    
class Commodity(Asset):

    def __init__(self, spot, 
                 name = "Empty_Name"):
        
        """
        Parameters
        ----------  

        spot : Цены товарно-сырьевого актива Series или Dict
        name : Имя товарно-сырьевого актива
        
        """                         
        self.spot = spot           
        self.name = name
        

    def check_spot(self, df):
        return(df)
    
    
    def calculate_first_diff(self, df):
        previous = 0
        result = {}
        
        for index, value in df.items():
            result.update( {index :  ((value - previous)/value)} )
            previous = value
            
        return (pd.Series(result))
    
    
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str):
            self.__name = new_name
        else:
            raise TypeError('Значение имени актива должно быть типа Str ')
            
    @property
    def spot(self):
        return self.__spot
    
    @spot.setter
    def spot(self, new_spot):
        
        if isinstance(new_spot, Series):
            self.__spot = self.check_spot(new_spot)
        elif isinstance(new_spot, dict):
            self.__spot = self.check_spot(pd.Series(new_spot))            
        else:
            raise TypeError('Значения цен должны быть типа Series или Dict ')
            
        self.__first_diff  = self.calculate_first_diff(self.__spot)
        
    @property
    def first_diff(self):
        return self.__first_diff
    
    @first_diff.setter
    def first_diff(self, new):
        raise TypeError('Задайте сначала значения цен')
        
    

        
        
class Currency(Asset):
    def __init__(self, 
                 start_date = "2010-01-01", 
                 end_date = datetime.today().strftime('%Y-%m-%d'),
                 base = None,
                 name = "Empty_name"):
        
        """
        Parameters
        ----------  

        name : Наименование иностранной валюты
        base : Код иностранной валюты
        start_date : Дата начала исторического периода
        end_date : Дата окончания исторического периода
        
        """      
        self.init = True
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.__base = base
        self.init = False
        self.__data = self.load_data()
                   
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str):
            self.__name = new_name
        else:
            raise TypeError('Значение имени актива должно быть типа Str ')
            
    @property
    def base(self):
        return self.__base
    
    @base.setter
    def base(self, new_name):
        if self.init == True:
            if isinstance(new_name, str):
                self.__base = new_name
            else:
                raise TypeError('Значение кода базового актива должно быть типа Str ')
        raise TypeError('Значение базового актива не подлежит изменению')
                
    @property
    def start_date(self):
        return self.__start_date
    
    @start_date.setter
    def start_date(self, new_value):
        if re.fullmatch(r'\d\d\d\d-\d\d-\d\d', new_value) == None: 
            raise TypeError('Значение даты должно быть в формате YYYY-MM-DD ')
            
        try:
            datetime.strptime(new_value, '%Y-%m-%d')
        except:
            raise TypeError('Значение не является датой')
            
        if datetime.strptime(new_value, '%Y-%m-%d') >= datetime.today():
            raise TypeError('Значение даты начала больше текущей даты')
           
        self.__start_date = new_value
        
        if self.init == False:
            self.loaddata()                        
       
                
    @property
    def end_date(self):
        return self.__end_date
    
    @end_date.setter
    def end_date(self, new_value):
        if re.fullmatch(r'\d\d\d\d-\d\d-\d\d', new_value) == None:
            raise TypeError('Значение даты должно быть в формате YYYY-MM-DD ')
        
        try:
            datetime.strptime(new_value, '%Y-%m-%d')
        except:
            raise TypeError('Значение не является датой')
            
        if datetime.strptime(new_value, '%Y-%m-%d') <= datetime.strptime(self.__start_date, '%Y-%m-%d'):
            raise TypeError('Значение даты начала больше значения даты окончания')
            
        self.__end_date = new_value
        
        if self.init == False:
            self.loaddata()
                               
    def load_data(self):
        try:
            url = f'https://api.exchangeratesapi.io/history?start_at={self.__start_date}&end_at={self.__end_date}&base={self.__base}'
            return(requests.get(url).json()['rates'])
        except:
            raise TypeError('Произошла ошибка при загрузке данных')
            
    def get_rate(self, curr, date):
        if date in self.__data.keys():
            if curr in self.__data[date].keys():
                return self.__data[date][curr]
            else:
                return -1
        else:
            return -1
        

if  __name__ == '__main__':
    
    USD = Currency(base="USD", name = "Доллар") 
    EUR = Currency(base="EUR", name = "Евро")   