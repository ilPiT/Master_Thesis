# -*- coding: utf-8 -*-
"""
Created on Fri May 13 11:38:36 2022

@author: pietr
"""

import pandas as pd

#%% First analysis for the Chuquisaca department 

# import the codes for the municipalities that we need to analyse

municipalities_selection = pd.read_excel('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/municipalities_selection.xlsx')
column_list_municiapalities_selection = municipalities_selection.columns.values.tolist()
municipal_code = municipalities_selection['Código']



department_list = ['CHUQUISACA','SANTA CRUZ','ORURO','LA PAZ','BENI','COCHABAMBA','POTOSI','TARIJA','PANDO'] # maybe not super usefull because they are also classified with a number from 1 to 9 

# about the systems --> connected or not connected to the grid?
system_information = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/system_codes.csv')


system_information_CHUQUISACA = system_information.loc[system_information['DEPARTMENT']=='CHUQUISACA']
system_information_SANTACRUZ = system_information.loc[system_information['DEPARTMENT']=='SANTA CRUZ']
system_information_ORURO = system_information.loc[system_information['DEPARTMENT']=='ORURO']
system_information_LAPAZ = system_information.loc[system_information['DEPARTMENT']=='LA PAZ']
system_information_BENI = system_information.loc[system_information['DEPARTMENT']=='BENI']
system_information_COCHABAMBA = system_information.loc[system_information['DEPARTMENT']=='COCHABAMBA']
system_information_POTOSI = system_information.loc[system_information['DEPARTMENT']=='POTOSI']
system_information_TARIJA = system_information.loc[system_information['DEPARTMENT']=='TARIJA']
system_information_PANDO = system_information.loc[system_information['DEPARTMENT']=='PANDO']



# divide the municipalities code by departments --> WIP
 

# import the data from the real data base

chuquisaca_real_data_base = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/chuquisaca_sd.csv')

column_list_chuquisaca = chuquisaca_real_data_base.columns.values.tolist()


# Filtering process

# TODO : an initial filtering process that has to be done regards the connection with the main grid --> but still i need to check the document that Claudia told me in order to understand how to use "system code"  --> remember that the most reliable data comes from the grid

# 1 : Filtering for the residential sector

chuquisaca_data_base_residential = chuquisaca_real_data_base.loc[chuquisaca_real_data_base['CATEGORY'] == 1]

# 2 : Filtering for one month --> then it will be possible to use a for cycle to extend the analysis all year long 

chuquisaca_data_base_residential_gen = chuquisaca_data_base_residential.loc[chuquisaca_data_base_residential['MONTH']==1]

'''
# 2 : Filtering for one month --> then it will be possible to use a for cycle to extend the analysis all year long 

# WIP to extend the reasoning to all the year
chuquisaca_data_base_residential_all_months = pd.DataFrame()
for j in range (1,13):
    


#chuquisaca_data_base_residential_gen = chuquisaca_data_base_residential.loc[chuquisaca_data_base_residential['MONTH']==1]
    chuquisaca_data_base_residential_month = chuquisaca_data_base_residential.loc[chuquisaca_data_base_residential['MONTH']==j]
    a = chuquisaca_data_base_residential_month['CONS_LEI_MWH']
    chuquisaca_data_base_residential_all_months = pd.concat([chuquisaca_data_base_residential_all_months,a],axis =1)

# Remember that in this filtering we are selecting only the column we are interested in 
'''




# 4 : Filtering for a specific year --> 2012 

chuquisaca_data_base_residential_gen_2012 = chuquisaca_data_base_residential_gen.loc[chuquisaca_data_base_residential_gen['YEAR']==2012]

# 3 : Filtering for the municipalties that has been selected following some fundamental criteria and parameters --> example for one municipality but then it can be extended with a for cycle for all the municiplaities that have been selected


# work in progress 
chuquisaca_data_base_residential_gen_dict_2012 = {}
energy_analysis_gen_2012 = {}

for i in range (0,3):

    chuquisaca_data_base_residential_gen_munipality_2012 = chuquisaca_data_base_residential_gen_2012.loc[chuquisaca_data_base_residential_gen_2012['COD_MUNI']==municipal_code[i]] # Huacaya
    #chuquisaca_data_base_residential_gen_munipality = chuquisaca_data_base_residential_gen.loc[chuquisaca_data_base_residential_gen['COD_MUNI']==municipal_code[1]] # Huacaya
    chuquisaca_data_base_residential_gen_dict_2012[i] = dict(chuquisaca_data_base_residential_gen_munipality_2012)
    #chuquisaca_data_base_residential_gen_dict[1] = dict(chuquisaca_data_base_residential_gen_munipality)
    energy_analysis_gen_2012[i] = dict(chuquisaca_data_base_residential_gen_dict_2012[i]['CONS_LEI_MWH'].describe())

# the describe fiunction is really usefull because it gives you the percentiles that represents the distribution of values of the energy consumption 

# CONS_LEI_MWH ,CONS_FAC_MWH, FAC_ENERGY



#%%
# not really important--> about possible statistical analysis  

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

chuquisaca_data_base_residential_gen_munipality_id = chuquisaca_data_base_residential_gen_munipality.loc[chuquisaca_data_base_residential_gen_munipality['ID']=='acc952af0e8d6a55999c2d2346cdfbdb72b3f490']
chuquisaca_data_base_residential_gen_munipality_address = chuquisaca_data_base_residential_gen_munipality.loc[chuquisaca_data_base_residential_gen_munipality['ADDRESS']=='BARRIO SANTA ROSA CALLE NUMERO 1   , UV: 0000- , M']
'''

