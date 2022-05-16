# -*- coding: utf-8 -*-
"""
Created on Fri May 13 11:38:36 2022

@author: pietr
"""

import pandas as pd

   


#%% First analysis for the Chuquisaca department then be extended to all the departements

# TODO : you can just put all the csv in the same place then read all the file with a for loop and then proceed with the analysis. 


# Reasoning still within one only department --> example the department of Chuquisaca
# import the codes for the municipalities that we need to analyse

municipalities_selection = pd.read_excel('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/municipalities_selection.xlsx')
column_list_municiapalities_selection = municipalities_selection.columns.values.tolist()
municipal_code = municipalities_selection['Código']


'''
department_list = ['CHUQUISACA','SANTA CRUZ','ORURO','LA PAZ','BENI','COCHABAMBA','POTOSI','TARIJA','PANDO'] # maybe not super usefull because they are also classified with a number from 1 to 9 

# about the systems --> connected or not connected to the grid?
system_information = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/system_codes.csv')

# it can be done in a smarter way for sure 

system_information_CHUQUISACA = system_information.loc[system_information['DEPARTMENT']=='CHUQUISACA']
system_information_SANTACRUZ = system_information.loc[system_information['DEPARTMENT']=='SANTA CRUZ']
system_information_ORURO = system_information.loc[system_information['DEPARTMENT']=='ORURO']
system_information_LAPAZ = system_information.loc[system_information['DEPARTMENT']=='LA PAZ']
system_information_BENI = system_information.loc[system_information['DEPARTMENT']=='BENI']
system_information_COCHABAMBA = system_information.loc[system_information['DEPARTMENT']=='COCHABAMBA']
system_information_POTOSI = system_information.loc[system_information['DEPARTMENT']=='POTOSI']
system_information_TARIJA = system_information.loc[system_information['DEPARTMENT']=='TARIJA']
system_information_PANDO = system_information.loc[system_information['DEPARTMENT']=='PANDO']

'''

# divide the municipalities code by departments --> WIP
 
#%%

# import the data from the real data base

chuquisaca_real_data_base = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/chuquisaca_sd.csv')

column_list_chuquisaca = chuquisaca_real_data_base.columns.values.tolist()


# Filtering process

# TODO : an initial filtering process that has to be done regards the connection with the main grid --> but still i need to check the document that Claudia told me in order to understand how to use "system code"  --> remember that the most reliable data comes from the grid

#system_information_CHUQUISACA = system_information.loc[system_information['DEPARTMENT']=='CHUQUISACA']


# 1 : Filtering for the residential sector

chuquisaca_data_base_residential = chuquisaca_real_data_base.loc[chuquisaca_real_data_base['CATEGORY'] == 1]

# 2 : Filtering for a specific year --> 2012  --> 2016

chuquisaca_data_base_residential_2012 = chuquisaca_data_base_residential.loc[chuquisaca_data_base_residential['YEAR']==2012]





#%% 
# 3 : Filtering for one month --> then it will be possible to use a for cycle to extend the analysis all year long 

#  : Filtering for one month --> then it will be possible to use a for cycle to extend the analysis all year long 

# WIP to extend the reasoning to all the year



# the describe fiunction is really usefull because it gives you the percentiles that represents the distribution of values of the energy consumption 

# CONS_LEI_MWH ,CONS_FAC_MWH, FAC_ENERGY

chuquisaca_data_base_residential_all_months_all_municipalities = {}
energy_analysis_2012_complete = {}

for j in range (1,13):
    
    energy_analysis_2012 = {}
    chuquisaca_data_base_residential_municipality_dict_2012 = {}
    chuquisaca_data_base_residential_month = chuquisaca_data_base_residential_2012.loc[chuquisaca_data_base_residential_2012['MONTH']==j]
    
    # let's say that we are reasoning for the month of january # thus in this loop we have a fixed month
    for i in range (0,28): # all the municipalities of chuquisaca department

        chuquisaca_data_base_residential_month_munipality_2012 = chuquisaca_data_base_residential_month.loc[chuquisaca_data_base_residential_month['COD_MUNI']==municipal_code[i]] # Huacaya
        #chuquisaca_data_base_residential_gen_munipality = chuquisaca_data_base_residential_gen.loc[chuquisaca_data_base_residential_gen['COD_MUNI']==municipal_code[1]] # Huacaya
        chuquisaca_data_base_residential_municipality_dict_2012[i] = dict(chuquisaca_data_base_residential_month_munipality_2012)
        #chuquisaca_data_base_residential_gen_dict[1] = dict(chuquisaca_data_base_residential_gen_munipality)
        energy_analysis_2012[i] = dict(chuquisaca_data_base_residential_municipality_dict_2012[i]['CONS_LEI_MWH'].describe())


## The most fundamental dict with all the information that you need stored with the right structure --> month division --> then municipality division --> then structure of the original database

# OSS: in this case the year is still fixed 
# first level : months --> thus 12 keys
# second level : municipalities --> thus the number of the municipalities for each department
# third level : strcuture of the original database with the 17 columns with all the information needed for every kind of analysis 


    chuquisaca_data_base_residential_all_months_all_municipalities[j] = dict(chuquisaca_data_base_residential_municipality_dict_2012)
    
## Fundamental databse for the residential energy consumption with the same structure of the previous dict but containing only informatio about the monthly energy consumption    
    energy_analysis_2012_complete[j] = dict (energy_analysis_2012)


### TODO : cleaning of the missing data --> there are some municipalities that does not have any data at all --> when we do the analysis we should not consider their values 

#%% Now we should work on the energy dict 

# 1 : Select a month
gen_energy_describe_final = pd.DataFrame()
gen_energy_info_all_municipalities = []
a = list(energy_analysis_2012_complete[1][1].keys()) # they are always the same
 

for columns in range(0,8):
    
    for i in range (0,28):
        
        gen_energy_describe_info = energy_analysis_2012_complete [1][i][a[columns]] 
        gen_energy_info_all_municipalities.append(gen_energy_describe_info)
        series = pd.Series(gen_energy_info_all_municipalities)
        
    gen_energy_describe_final = pd.concat([gen_energy_describe_final,series],ignore_index=False, axis=1)

    series = []
    gen_energy_info_all_municipalities = []


  
gen_energy_describe_final.columns = a



## Cleanning of the data that are zero?


clean_database = gen_energy_describe_final.dropna()
columns_clean_database = clean_database.columns.tolist()


# 2 : Analyse the overall trend of the describe function for each municipality

test_1 = clean_database['mean'].describe()
test_2 = clean_database['25%'].describe()
test_3 = clean_database['50%'].describe()
test_4 = clean_database['75%'].describe()

#%%

# not really important--> about possible statistical analysis  

'''
freq_disp_CONS_LEI_MWH = chuquisaca_data_base_residential_gen_munipality_2012_focus['CONS_LEI_MWH'].value_counts()
freq_disp_CONS_LEI_MWH_sort_index = chuquisaca_data_base_residential_gen_munipality_2012_focus['CONS_LEI_MWH'].value_counts().sort_index()
freq_disp_CONS_LEI_MWH_percentage = chuquisaca_data_base_residential_gen_munipality_2012_focus['CONS_LEI_MWH'].value_counts(normalize= True).sort_index()*100
freq_disp_CONS_LEI_MWH_percentage.describe()

count = chuquisaca_data_base_residential_gen_munipality_2012_focus.groupby(['CONS_LEI_MWH']).count()
count.describe()


## Example Frequency tables --> https://www.youtube.com/watch?v=UGV-GMIHLdY to dimensional tables if we will need them in future

my_tab = pd.crosstab(index= chuquisaca_data_base_residential_gen_munipality_2012['CONS_LEI_MWH'], columns = 'count')

# OSS: thus one of the usefull things of using pd.crosstab is that we have as an output a dataframe and then it is possible to use all the pandas functions
# remember that iloc is used to slice and cut datas
'''
# test filtering for ID or address to verify the number of users and their changes through the years
'''
chuquisaca_data_base_residential_gen_munipality_id = chuquisaca_data_base_residential_gen_munipality.loc[chuquisaca_data_base_residential_gen_munipality['ID']=='acc952af0e8d6a55999c2d2346cdfbdb72b3f490']
chuquisaca_data_base_residential_gen_munipality_address = chuquisaca_data_base_residential_gen_munipality.loc[chuquisaca_data_base_residential_gen_munipality['ADDRESS']=='BARRIO SANTA ROSA CALLE NUMERO 1   , UV: 0000- , M']
'''

