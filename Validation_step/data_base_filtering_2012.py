# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 10:22:38 2022

@author: pietr
"""

import pandas as pd 
from scipy import stats
import numpy as np

def filtering_database(database, year): 
    
    first_filtering = database.loc[database['CATEGORY']==1]
    second_filtering = first_filtering.loc[first_filtering['YEAR']==year]
    third_filtering = second_filtering.loc[second_filtering['CONS_LEI_MWH']!=0] # do not really know if it is fundamental
    fourth_filtering = third_filtering[(np.abs(stats.zscore(third_filtering['CONS_LEI_MWH']))<3)]
    #df[(np.abs(stats.zscore(df[0])) < 3)]
    return fourth_filtering

# OSS : i should have created another function instead of repeating the operation 9 times ? YES!!! NEXT TIME FOR THE YEAR 2013 FOR EXAMPLE IT IS BETTER TO CREATE A FUNCTION FOR SURE 

#%% 
# santa cruz 1

santa_cruz_real_data_base = pd.read_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments/santacruz_sd.csv')


santa_cruz_real_data_base_filtered = filtering_database(santa_cruz_real_data_base,2012)

santa_cruz_real_data_base_filtered.to_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments_filtered/santacruz_sd.csv')


#%%
# cochabamba 2

cochabamba_real_data_base = pd.read_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments/cochabamba_sd.csv')


cochabamba_real_data_base_filtered = filtering_database(cochabamba_real_data_base,2012)

cochabamba_real_data_base_filtered.to_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments_filtered/cochabamba_sd.csv')

#%%
# la paz 3

la_paz_real_data_base = pd.read_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments/lapaz_sd.csv')


la_paz_real_data_base_filtered = filtering_database(la_paz_real_data_base)
la_paz_real_data_base_filtered.to_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments_filtered/lapaz_sd.csv')

#%%
#  chuquisaca 4 

chuquisaca_real_data_base = pd.read_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments/chuquisaca_sd.csv')

chuquisaca_real_data_base_filtered = filtering_database(chuquisaca_real_data_base)

chuquisaca_real_data_base_filtered.to_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments_filtered/chuquisaca_sd.csv')

#%%
# tarija 5 

tarija_real_data_base = pd.read_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments/tarija_sd.csv')

tarija_real_data_base_filtered = filtering_database(tarija_real_data_base)
tarija_real_data_base_filtered.to_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments_filtered/tarija_sd.csv')

#%%

# beni 6 #qua

beni_real_data_base = pd.read_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments/beni_sd.csv')

beni_real_data_base_filtered = filtering_database(beni_real_data_base)
beni_real_data_base_filtered.to_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments_filtered/beni_sd.csv')


#%%

#potosi 7 

potosi_real_data_base = pd.read_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments/potosi_sd.csv')

potosi_real_data_base_filtered = filtering_database(potosi_real_data_base,2012)
potosi_real_data_base_filtered.to_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments_filtered/potosi_sd.csv')


#%%

#pando 8 


pando_real_data_base = pd.read_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments/pando_sd.csv')

pando_real_data_base_filtered = filtering_database(pando_real_data_base,2012)
pando_real_data_base_filtered.to_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments_filtered/pando_sd.csv')



#%%
# oruro 9

oruro_real_data_base = pd.read_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments/oruro_sd.csv')

oruro_real_data_base_filtered = filtering_database(oruro_real_data_base)
oruro_real_data_base_filtered.to_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments_filtered/oruro_sd.csv')


