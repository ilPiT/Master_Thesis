# -*- coding: utf-8 -*-
"""
Created on Fri May 13 11:38:36 2022

@author: pietr
"""

import pandas as pd

   



#%% First : analysis of a specific department then be extended to all the departements

# In this case we are using the beni database

# import the municipal-codes for the municipalities that we need to analyse

municipalities_selection = pd.read_excel('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/municipalities_selection.xlsx')
column_list_municiapalities_selection = municipalities_selection.columns.values.tolist()


municipal_code_beni = municipalities_selection.loc[municipalities_selection['Departamento']== 'Beni']

municipal_code_beni = municipal_code_beni['Código'] # this variable will be used for the next filtering of the database municipalities


# Usefull index information : range 305 --> 323



#%%

# import the data from the real data base

#chuquisaca_real_data_base = pd.read_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments/chuquisaca_sd.csv')
beni_real_data_base = pd.read_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments/beni_sd.csv')

column_list_beni = beni_real_data_base.columns.values.tolist()


# Filtering process


# 1 : Filtering for the residential sector

beni_data_base_residential = beni_real_data_base.loc[beni_real_data_base['CATEGORY'] == 1]

# 2 : Filtering for a specific year --> 2012  --> 2016

# In this case we are considering 2012

beni_data_base_residential_2012 = beni_data_base_residential.loc[beni_data_base_residential['YEAR']==2012]





#%% 
# 3 : Filtering for all the months in a year 


# Defining some usefull dictionaries for the storing of data

beni_data_base_residential_all_months_all_municipalities = {} # final dictionary with all the filtered information of the beni department


energy_analysis_2012_complete = {} # final dictionary with all the fundamental info abou the montlhy energy consumption

for j in range (1,13): # looping the months 
    
    energy_analysis_2012 = {}
    beni_data_base_residential_municipality_dict_2012 = {}
    beni_data_base_residential_month = beni_data_base_residential_2012.loc[beni_data_base_residential_2012['MONTH']==j]
    
    
    
    for i in range (305,323): #  looping on all the municipalities of beni department

        beni_data_base_residential_month_munipality_2012 = beni_data_base_residential_month.loc[beni_data_base_residential_month['COD_MUNI']==municipal_code_beni[i]]

        # TODO : adding the next line you are not considering in the next analysis all the users that have not consuming electricity --> not super sure?
        #beni_data_base_residential_month_munipality_2012 = beni_data_base_residential_month_munipality_2012.loc[beni_data_base_residential_month_munipality_2012['CONS_LEI_MWH']!=0] 
        

        beni_data_base_residential_municipality_dict_2012[i] = dict(beni_data_base_residential_month_munipality_2012)
        
        energy_analysis_2012[i] = dict(beni_data_base_residential_municipality_dict_2012[i]['CONS_LEI_MWH'].describe())
        


## The most fundamental dict with all the information that you need stored with the right structure --> month division --> then municipality division --> then structure of the original database

# OSS: in this case the year is still fixed 
# first level : months --> thus 12 keys
# second level : municipalities --> thus the number of the municipalities for each department
# third level : strcuture of the original database with the 17 columns with all the information needed for every kind of analysis 


    beni_data_base_residential_all_months_all_municipalities[j] = dict(beni_data_base_residential_municipality_dict_2012)
    
## Fundamental databse for the residential energy consumption with the same structure of the previous dict but containing only informatio about the monthly energy consumption
    
    energy_analysis_2012_complete[j] = dict (energy_analysis_2012)


#%% Now we should work on the energy dict 


energ_describe_final_dict ={}
gen_energy_describe_final = pd.DataFrame()
gen_energy_info_all_municipalities = []
a = list(energy_analysis_2012_complete[1][305].keys()) # they are always the same
 

for j in range (1,13): #looping of the months

    for columns in range(0,8): # looping on the columns /data that are the results of the describe function
        
        
        
        for i in range (305,323): # differentiation for the munipalities --> you should find a way in order to do that in auto 
            
            gen_energy_describe_info = energy_analysis_2012_complete [j][i][a[columns]] 
            gen_energy_info_all_municipalities.append(gen_energy_describe_info)
            series = pd.Series(gen_energy_info_all_municipalities)
            
        gen_energy_describe_final = pd.concat([gen_energy_describe_final,series],ignore_index=False, axis=1)
    
    
        
        series = []
        gen_energy_info_all_municipalities = []
             
    
          
    gen_energy_describe_final.columns = a
    
    
    
    ## Cleanning of the data that are zero
    
    
    clean_database = gen_energy_describe_final.dropna()
    columns_clean_database = clean_database.columns.tolist()
    
    over_all_energy_anergy_analysis = pd.DataFrame()
    
    # 2 : Analyse the overall trend of the describe function for each municipality with another desccribe function
    
    test_1 = clean_database['mean'].describe()
    test_2 = clean_database['25%'].describe()
    test_3 = clean_database['50%'].describe()
    test_4 = clean_database['75%'].describe()
    
    over_all_energy_anergy_analysis_dic = pd.concat([over_all_energy_anergy_analysis,test_1,test_2,test_3,test_4],axis=1)
    over_all_energy_anergy_analysis_dic.to_excel('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/Results_beni/beni_energy_analysis_%d.xlsx' %j)

    gen_energy_describe_final = pd.DataFrame()
    
over_all_energy_anergy_analysis_dic = pd.DataFrame()
clean_database = pd.DataFrame() 
