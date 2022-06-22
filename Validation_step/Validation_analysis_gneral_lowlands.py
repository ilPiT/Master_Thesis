# -*- coding: utf-8 -*-
"""
Created on Fri May 13 11:38:36 2022

@author: pietr
"""

import pandas as pd
from scipy import stats
import numpy as np
   



#%% First : analysis of a specific department then be extended to all the departements

# now USELESS


# import the municipal-codes for the municipalities that we need to analyse

# Real municipalities selection list done by Claudia
municipalities_selection = pd.read_excel('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/municipalities_selection_final.xlsx', sheet_name='selec_mun')
column_list_municiapalities_selection = municipalities_selection.columns.values.tolist()

# 'Code'
# Chaco zone 0 --> 6 

chaco_codes = municipalities_selection['Code'].iloc[:7] # involves three different departments thus three different database
tropical_lowlands_codes = municipalities_selection['Code'].iloc[7:15] # involves three different departments thus three different database
amazonia_codes = municipalities_selection['Code'].iloc[16:21] # involves three different departments thus three different database
valleys_codes = municipalities_selection['Code'].iloc[21:34] # involves three different departments thus three different database
highlands_codes = municipalities_selection['Code'].iloc[34:43] # involves three different departments thus three different database

# Departments involved : 1 Chuquisaca - 6 Tarija - 7 Santa Cruz

#%%


final_municipalities = pd.read_excel('D:/poli_new/New_step/Validation_step/municipalities_selection_filtered.xlsx')


# Highlands > 3000

highlands_municipalities = final_municipalities.loc[final_municipalities['Altitude']>3000]


# Valleys  1500 < altitude < 3000
valleys_municipalities = final_municipalities.loc[final_municipalities['Altitude']<3000]
valleys_municipalities = valleys_municipalities.loc[valleys_municipalities['Altitude']>1500]

# Lowlands Chaco and Amazzonia < 1500 
general_lowlands = final_municipalities.loc[final_municipalities['Altitude']<1500]



#### SPECIFIC FOR THE VALLEYS

general_lowlands_codes = general_lowlands['Código']
'''
general_lowlands_codes = general_lowlands_codes.append(tropical_lowlands_codes)
general_lowlands_codes = general_lowlands_codes.append(amazonia_codes)
general_lowlands_codes = general_lowlands_codes.append(chaco_codes)
'''
general_lowlands_codes.index = range(len(general_lowlands_codes))

# OSS the majority of this municipalities belong to the amazzonia region without doubt --> that should be the most rural part of the country where the condition of the national grid are the more scarse

# OSS the majority of all the municipalities that are from amazonia are from PANDO department

 
# from the results of the manual analysis THAT HAS TO BE IMPROVED

# Chaco manually improved : 10502 , 60201

chaco_codes = chaco_codes.append(general_lowlands_codes.iloc[1:2])
chaco_codes = chaco_codes.append(general_lowlands_codes.iloc[3:4])

chaco_codes.index = range(len(chaco_codes))

# Amazzonia : Bolpebra already present 90103 and 90402

amazonia_codes = amazonia_codes.append(general_lowlands_codes.iloc[2:3])
amazonia_codes = amazonia_codes.append(general_lowlands_codes.iloc[11:])

amazonia_codes.index = range(len(amazonia_codes))

# Tropical lowlands : nothing to add
tropical_lowlands_codes.index = range(len(tropical_lowlands_codes))
   

#%%



# import the data from the real data base  YEAR : 2012

tarija_real_data_base_filtered = pd.read_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments_filtered/tarija_sd.csv')
chuquisaca_real_data_base_filtered = pd.read_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments_filtered/chuquisaca_sd.csv')
santa_cruz_real_data_base_filtered = pd.read_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments_filtered/santacruz_sd.csv')
cochabamba_real_data_base_filtered = pd.read_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments_filtered/cochabamba_sd.csv')
la_paz_real_data_base_filtered = pd.read_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments_filtered/lapaz_sd.csv')

oruro_real_data_base_filtered = pd.read_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments_filtered/oruro_sd.csv')
potosi_real_data_base_filtered = pd.read_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments_filtered/potosi_sd.csv')
beni_real_data_base_filtered = pd.read_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments_filtered/beni_sd.csv')
pando_real_data_base_filtered = pd.read_csv('D:/poli_new/New_step/Data_base_real/Real_data_base_departments_filtered/pando_sd.csv')




column_list_tarija = tarija_real_data_base_filtered.columns.values.tolist()

frames = [tarija_real_data_base_filtered,chuquisaca_real_data_base_filtered,santa_cruz_real_data_base_filtered,cochabamba_real_data_base_filtered,la_paz_real_data_base_filtered,beni_real_data_base_filtered,pando_real_data_base_filtered,potosi_real_data_base_filtered,oruro_real_data_base_filtered] 
# the merged database --> it is a kind of long process mostly becasue the database can be really heavy
big_real_data_base = pd.concat(frames)
column_list_chaco = big_real_data_base.columns.values.tolist()


#%%
#TODO: here you could add another layer to the dictionary involving the different year analysis --> if you want to do a historical analysis you should change the function which filters the data 

# Filtering process
chaco_residential_all_months_selected_municipalities = {} # final dictionary with all the filtered information of the beni department
energy_analysis_2012_chaco_zone = {} # final dictionary with all the fundamental info about the montlhy energy consumption

'''
def months_looping(dict_1,dict_2_energy,department_real_database,codes):
    for j in range (1,13):
        energy_analysis_2012 = {}
        data_base_residential_municipality_dict_2012 = {}
        
        real_data_base_month = department_real_database.loc[department_real_database['MONTH']==j]
        
        for i in range(len(codes)):
            data_base_munipality = real_data_base_month.loc[real_data_base_month['COD_MUNI'] == codes[i]]
            data_base_residential_municipality_dict_2012[i] = dict(data_base_munipality)
            energy_analysis_2012[i] = dict(chaco_data_base_residential_municipality_dict_2012[i]['CONS_LEI_MWH'].describe())
'''
            


for j in range (1,13): # looping the months 
    
    energy_analysis_2012 = {}
    chaco_data_base_residential_municipality_dict_2012 = {}
    chuquisaca_real_data_base_month = big_real_data_base.loc[big_real_data_base['MONTH']==j]
    
    
    # Filter directily with the municipal codes
    for i in range (len(chaco_codes)): #looping on the first codes --> improvement : looping on a list of the different municipal codes could be the best way to do it
                
                chuquisaca_data_base_munipality = chuquisaca_real_data_base_month.loc[chuquisaca_real_data_base_month['COD_MUNI'] == chaco_codes[i]]
                chuquisaca_data_base_munipality_residential = chuquisaca_data_base_munipality.loc[chuquisaca_data_base_munipality['CATEGORY']==1]
                chuquisaca_data_base_munipality_residential_2012 = chuquisaca_data_base_munipality_residential.loc[chuquisaca_data_base_munipality_residential['YEAR']==2012]
                chaco_data_base_residential_municipality_dict_2012[i] = dict(chuquisaca_data_base_munipality_residential_2012)
                energy_analysis_2012[i] = dict(chaco_data_base_residential_municipality_dict_2012[i]['CONS_LEI_MWH'].describe())

    chaco_residential_all_months_selected_municipalities[j] = dict(chaco_data_base_residential_municipality_dict_2012)
    energy_analysis_2012_chaco_zone[j] = dict (energy_analysis_2012)
#%% 

#%% Now we should work on the energy dict 


energ_describe_final_dict ={}
gen_energy_describe_final = pd.DataFrame()
gen_energy_info_all_municipalities = []
a = list(energy_analysis_2012_chaco_zone[1][1].keys()) # they are always the same
 

for j in range (1,13): #looping of the months

    for columns in range(0,8): # looping on the columns /data that are the results of the describe function
        
        
        
        for i in range (len(chaco_codes)): # differentiation for the munipalities --> you should find a way in order to do that in auto 
            
            gen_energy_describe_info = energy_analysis_2012_chaco_zone [j][i][a[columns]] 
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
    over_all_energy_anergy_analysis_dic.to_excel('D:/poli_new/New_step/Validation_step/Results_chaco/chaco_energy_analysis_%d.xlsx' %j)

    gen_energy_describe_final = pd.DataFrame()
    energ_describe_final_dict[j] = dict(over_all_energy_anergy_analysis_dic)
    
over_all_energy_anergy_analysis_dic = pd.DataFrame()
clean_database = pd.DataFrame() 


#%%
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
import os 
import matplotlib.lines as mlines

#Plotting of the seasonal behavior 2012
mean_2012 = pd.DataFrame()
percentiles_25_2012 = pd.DataFrame()
percentiles_50_2012 = pd.DataFrame()
percentiles_75_2012 = pd.DataFrame()

for j in range(1,13):
    chaco_energy_analysis = pd.read_excel('D:/poli_new/New_step/Validation_step/Results_chaco/chaco_energy_analysis_%d.xlsx' %j) 
    mean_column = chaco_energy_analysis['mean']
    percentiles_25 = chaco_energy_analysis['25%']
    percentiles_50 = chaco_energy_analysis['50%']
    percentiles_75 = chaco_energy_analysis['75%']
    mean_2012 = pd.concat([mean_2012,mean_column],ignore_index= False,axis=1)
    percentiles_25_2012 = pd.concat([percentiles_25_2012,percentiles_25],ignore_index= False,axis=1)
    percentiles_50_2012 = pd.concat([percentiles_50_2012,percentiles_50],ignore_index= False,axis=1)
    percentiles_75_2012 = pd.concat([percentiles_75_2012,percentiles_75],ignore_index= False,axis=1)

index = chaco_energy_analysis['Unnamed: 0']
columns = [1,2,3,4,5,6,7,8,9,10,11,12]
mean_2012.columns = columns
mean_2012.index = index

### checking for the outliers and checking for if datas have a normal distribution 

a = mean_2012.loc['mean']*1000
#b = percentiles_25_2012.loc['mean']*1000
filtering_mean = a[(np.abs(stats.zscore(a))<3)]
a.hist()
#b.hist()

#%%
## Plotting MEAN --> but wh have already checked that because of the non-nomrality distribution then the mean does not represent the data in a good way.
x = columns

size = [20,15]
fig=plt.figure(figsize=size)

plt.plot(columns,mean_2012.loc['mean']*1000 , linestyle='--', marker='o',c='b')
plt.plot(columns, mean_2012.loc['25%']*1000, linestyle='--', marker='o',c='darkviolet')
plt.plot(columns, mean_2012.loc['50%']*1000, linestyle='--', marker='o',c='c')
plt.plot(columns, mean_2012.loc['count'], linestyle='', marker='*',c='r',markersize=25)
plt.axhline(y = 50, color = 'r', linestyle = '-',label="Tariff",linewidth = 4)

plt.xlabel("Months",size=30)
plt.ylabel("Monthly_energy_consumption_KWh",size=30)
plt.title('Mean information',size = 40)

tick_size = 25   
#mpl.rcParams['xtick.labelsize'] = tick_size     
plt.tick_params(axis='x', which='major', labelsize = tick_size )
plt.tick_params(axis='y', which='major', labelsize = tick_size )  


handle1 = mlines.Line2D([], [], color='b',
                                  label='Mean', 
                                  linestyle='--',
                                  marker = 'o')
handle2 = mlines.Line2D([], [], color='darkviolet',
                                  label='25%', 
                                  linestyle='--',
                                  marker = 'o')
handle3 = mlines.Line2D([], [], color='c',
                                  label='50%', 
                                  linestyle='-',
                                  )
handle4 = mlines.Line2D([], [], color='r',
                                  label='count', 
                                  linestyle='',
                                  marker ='*',
                                  markersize=25
                                  )

plt.legend(handles=[handle1,handle2,handle3,handle4],
                            bbox_to_anchor=(0.95, -0.07),fontsize = 30,
                            frameon=False,  ncol=3) 
plt.xticks(x,x)        
#plt.savefig('C:/Users/pietr/Spyder/RAMP_spyder/Graphs_comparison/Residential_comparison.png')
plt.show()  

#%% 
'''
index = chaco_energy_analysis['Unnamed: 0']
columns = [1,2,3,4,5,6,7,8,9,10,11,12]
percentiles_25_2012.columns = columns
percentiles_25_2012.index = index


# Plotting the 25% percentile information


x = columns

size = [20,15]
fig=plt.figure(figsize=size)

plt.plot(columns,percentiles_25_2012.loc['mean']*1000 , linestyle='--', marker='o',c='b')
plt.plot(columns, percentiles_25_2012.loc['25%']*1000, linestyle='--', marker='o',c='darkviolet')
plt.plot(columns, percentiles_25_2012.loc['50%']*1000, linestyle='--', marker='o',c='c')

plt.axhline(y = 50, color = 'r', linestyle = '-',label="Tariff",linewidth = 4)

plt.xlabel("Months",size=30)
plt.ylabel("Monthly_energy_consumption_KWh",size=30)
plt.title('25% percentile information',size = 40)

tick_size = 25   
#mpl.rcParams['xtick.labelsize'] = tick_size     
plt.tick_params(axis='x', which='major', labelsize = tick_size )
plt.tick_params(axis='y', which='major', labelsize = tick_size )  


handle1 = mlines.Line2D([], [], color='b',
                                  label='Mean', 
                                  linestyle='--',
                                  marker = 'o')
handle2 = mlines.Line2D([], [], color='darkviolet',
                                  label='25%', 
                                  linestyle='--',
                                  marker = 'o')
handle3 = mlines.Line2D([], [], color='c',
                                  label='50%', 
                                  linestyle='-',
                                  )

plt.legend(handles=[handle1,handle2,handle3],
                            bbox_to_anchor=(0.95, -0.07),fontsize = 30,
                            frameon=False,  ncol=3) 
plt.xticks(x,x)        
#plt.savefig('C:/Users/pietr/Spyder/RAMP_spyder/Graphs_comparison/Residential_comparison.png')
plt.show()  
'''

#%% CHACO

index = chaco_energy_analysis['Unnamed: 0']
columns = [1,2,3,4,5,6,7,8,9,10,11,12]
percentiles_50_2012.columns = columns
percentiles_50_2012.index = index


# Plotting the 50% percentile information

# due to the non normality distribution of the data the median and thus the 50th percentile represents at best the behaviour of the dataset 


#  COULD BE INTERESTING TO ADD A LINE THAT SHOWS THE AVERAGE %UBN in order to understand better the level of energy consumption 
# thus first of all --> need the values of UBN for the municipalities under study 
# then you do the average and you plot the value 

# the information are needed from the validation_database 
# you do a check using the municipal codes 
# and then you take the information needed and then average 

################### JUST TO PLOT THE AVERAGE OF THE UBN

data_base_validation = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/Validation.database.csv')
column_list_data_base_validation = data_base_validation.columns.values.tolist()

chaco_UBN = []
for i in range(len(chaco_codes)):
    d = str(chaco_codes[i])
    data_base_validation_chaco = data_base_validation.loc[data_base_validation['CODIGO']== d]
    chaco_UBN.append(data_base_validation_chaco)

chaco_list_UBN = []
for j in (chaco_UBN):
    
    describe_chaco_UBN = 100 - j['%Satisfied basic needs']
    chaco_value_UBN = describe_chaco_UBN.iloc[1]
    chaco_list_UBN.append(chaco_value_UBN)
    
chaco_describe_UBN = ((pd.DataFrame(chaco_list_UBN)).describe())
UBN = (float(chaco_describe_UBN.loc['mean']))

####################################################

x = columns

size = [20,15]
fig=plt.figure(figsize=size)

plt.plot(columns,percentiles_50_2012.loc['75%']*1000 , linestyle='--', marker='o',c='b')
plt.plot(columns, percentiles_50_2012.loc['25%']*1000, linestyle='--', marker='o',c='darkviolet')
plt.plot(columns, percentiles_50_2012.loc['50%']*1000, linestyle='--', marker='o',c='c')
plt.plot(columns, mean_2012.loc['count'], linestyle='', marker='*',c='r',markersize=25)
plt.axhline(y = 50, color = 'r', linestyle = '-',label ="Tariff",linewidth = 4, )
plt.axhline(y = UBN , color = 'g', linestyle = ':',label=" mean UBN%",linewidth = 4)

plt.xlabel("Months",size=30)
plt.ylabel("Monthly_energy_consumption_KWh",size=30)
plt.title('50% percentile information  Chaco',size = 40)
tick_size = 25   
#mpl.rcParams['xtick.labelsize'] = tick_size     
plt.tick_params(axis='x', which='major', labelsize = tick_size )
plt.tick_params(axis='y', which='major', labelsize = tick_size )  


handle1 = mlines.Line2D([], [], color='b',
                                  label='75%', 
                                  linestyle='--',
                                  marker = 'o')
handle2 = mlines.Line2D([], [], color='darkviolet',
                                  label='25%', 
                                  linestyle='--',
                                  marker = 'o')
handle3 = mlines.Line2D([], [], color='c',
                                  label='50%', 
                                  linestyle='-',
                                  )
handle4 = mlines.Line2D([], [], color='r',
                                  label='count', 
                                  linestyle='',
                                  marker ='*',
                                  markersize=25
                                  )

plt.legend(handles=[handle1,handle2,handle3,handle4],
                            bbox_to_anchor=(0.95, -0.07),fontsize = 30,
                            frameon=False,  ncol=3) 
plt.xticks(x,x)        
plt.savefig('D:/poli_new/New_step/Validation_step/Graphs_results/Seasonal_trends/Seasonal_trend_2012_50th_percentile_Chaco.png')
plt.show()  



#%%
'''
index = chaco_energy_analysis['Unnamed: 0']
columns = [1,2,3,4,5,6,7,8,9,10,11,12]
percentiles_75_2012.columns = columns
percentiles_75_2012.index = index


# Plotting the 75% percentile information


x = columns

size = [20,15]
fig=plt.figure(figsize=size)

plt.plot(columns,percentiles_75_2012.loc['mean']*1000 , linestyle='--', marker='o',c='b')
plt.plot(columns, percentiles_75_2012.loc['25%']*1000, linestyle='--', marker='o',c='darkviolet')
plt.plot(columns, percentiles_75_2012.loc['50%']*1000, linestyle='--', marker='o',c='c')
plt.axhline(y = 50, color = 'r', linestyle = '-',label="Tariff",linewidth = 4)

plt.xlabel("Months",size=30)
plt.ylabel("Monthly_energy_consumption_KWh",size=30)

plt.title('75% percentile information',size = 40)

tick_size = 25   
#mpl.rcParams['xtick.labelsize'] = tick_size     
plt.tick_params(axis='x', which='major', labelsize = tick_size )
plt.tick_params(axis='y', which='major', labelsize = tick_size )  


handle1 = mlines.Line2D([], [], color='b',
                                  label='Mean', 
                                  linestyle='--',
                                  marker = 'o')
handle2 = mlines.Line2D([], [], color='darkviolet',
                                  label='25%', 
                                  linestyle='--',
                                  marker = 'o')
handle3 = mlines.Line2D([], [], color='c',
                                  label='50%', 
                                  linestyle='-',
                                  )

plt.legend(handles=[handle1,handle2,handle3],
                            bbox_to_anchor=(0.95, -0.07),fontsize = 30,
                            frameon=False,  ncol=3) 
plt.xticks(x,x)        
#plt.savefig('C:/Users/pietr/Spyder/RAMP_spyder/Graphs_comparison/Residential_comparison.png')
plt.show()  
'''


#%%

# Tropical lowlands


# Filtering process
tropcial_lowlands_residential_all_months_selected_municipalities = {} # final dictionary with all the filtered information of the beni department
energy_analysis_2012_tropcial_lowlands_zone = {} # final dictionary with all the fundamental info about the montlhy energy consumption

'''
def months_looping(dict_1,dict_2_energy,department_real_database,codes):
    for j in range (1,13):
        energy_analysis_2012 = {}
        data_base_residential_municipality_dict_2012 = {}
        
        real_data_base_month = department_real_database.loc[department_real_database['MONTH']==j]
        
        for i in range(len(codes)):
            data_base_munipality = real_data_base_month.loc[real_data_base_month['COD_MUNI'] == codes[i]]
            data_base_residential_municipality_dict_2012[i] = dict(data_base_munipality)
            energy_analysis_2012[i] = dict(chaco_data_base_residential_municipality_dict_2012[i]['CONS_LEI_MWH'].describe())
'''
            


for j in range (1,13): # looping the months 
    
    energy_analysis_2012 = {}
    tropcial_lowlands_data_base_residential_municipality_dict_2012 = {}
    tropcial_lowlands_real_data_base_month = big_real_data_base.loc[big_real_data_base['MONTH']==j]
    
    
    # Filter directily with the municipal codes
    for i in range (len(tropical_lowlands_codes)): #looping on the first codes --> improvement : looping on a list of the different municipal codes could be the best way to do it
                
                tropcial_lowlands_data_base_munipality = tropcial_lowlands_real_data_base_month.loc[tropcial_lowlands_real_data_base_month['COD_MUNI'] == tropical_lowlands_codes[i]]
                tropcial_lowlands_data_base_munipality_residential = tropcial_lowlands_data_base_munipality.loc[tropcial_lowlands_data_base_munipality['CATEGORY']==1]
                tropcial_lowlands_data_base_munipality_residential_2012 = tropcial_lowlands_data_base_munipality_residential.loc[tropcial_lowlands_data_base_munipality_residential['YEAR']==2012]
                tropcial_lowlands_data_base_residential_municipality_dict_2012[i] = dict(tropcial_lowlands_data_base_munipality_residential_2012)
                energy_analysis_2012[i] = dict(tropcial_lowlands_data_base_residential_municipality_dict_2012[i]['CONS_LEI_MWH'].describe())

    tropcial_lowlands_residential_all_months_selected_municipalities[j] = dict(tropcial_lowlands_data_base_residential_municipality_dict_2012)
    energy_analysis_2012_tropcial_lowlands_zone[j] = dict (energy_analysis_2012)
#%% 

#%% Now we should work on the energy dict 


energ_describe_final_dict ={}
gen_energy_describe_final = pd.DataFrame()
gen_energy_info_all_municipalities = []
a = list(energy_analysis_2012_tropcial_lowlands_zone[1][1].keys()) # they are always the same
 

for j in range (1,13): #looping of the months

    for columns in range(0,8): # looping on the columns /data that are the results of the describe function
        
        
        
        for i in range (len(tropical_lowlands_codes)): # differentiation for the munipalities --> you should find a way in order to do that in auto 
            
            gen_energy_describe_info = energy_analysis_2012_tropcial_lowlands_zone [j][i][a[columns]] 
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
    over_all_energy_anergy_analysis_dic.to_excel('D:/poli_new/New_step/Validation_step/Results_tropical_lowlands/tropical_lowlands_energy_analysis_%d.xlsx' %j)

    gen_energy_describe_final = pd.DataFrame()
    energ_describe_final_dict[j] = dict(over_all_energy_anergy_analysis_dic)
    
over_all_energy_anergy_analysis_dic = pd.DataFrame()
clean_database = pd.DataFrame() 


#%%
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
import os 
import matplotlib.lines as mlines

#Plotting of the seasonal behavior 2012
mean_2012 = pd.DataFrame()
percentiles_25_2012 = pd.DataFrame()
percentiles_50_2012 = pd.DataFrame()
percentiles_75_2012 = pd.DataFrame()

for j in range(1,13):
    tropcial_lowlands_energy_analysis = pd.read_excel('D:/poli_new/New_step/Validation_step/Results_tropical_lowlands/tropical_lowlands_energy_analysis_%d.xlsx' %j) 
    mean_column = tropcial_lowlands_energy_analysis['mean']
    percentiles_25 = tropcial_lowlands_energy_analysis['25%']
    percentiles_50 = tropcial_lowlands_energy_analysis['50%']
    percentiles_75 = tropcial_lowlands_energy_analysis['75%']
    mean_2012 = pd.concat([mean_2012,mean_column],ignore_index= False,axis=1)
    percentiles_25_2012 = pd.concat([percentiles_25_2012,percentiles_25],ignore_index= False,axis=1)
    percentiles_50_2012 = pd.concat([percentiles_50_2012,percentiles_50],ignore_index= False,axis=1)
    percentiles_75_2012 = pd.concat([percentiles_75_2012,percentiles_75],ignore_index= False,axis=1)

index = tropcial_lowlands_energy_analysis['Unnamed: 0']
columns = [1,2,3,4,5,6,7,8,9,10,11,12]
mean_2012.columns = columns
mean_2012.index = index

### checking for the outliers and checking for if datas have a normal distribution 

a = mean_2012.loc['mean']*1000
#b = percentiles_25_2012.loc['mean']*1000
filtering_mean = a[(np.abs(stats.zscore(a))<3)]
a.hist()
#b.hist()

#%%
## Plotting MEAN --> but wh have already checked that because of the non-nomrality distribution then the mean does not represent the data in a good way.
x = columns

size = [20,15]
fig=plt.figure(figsize=size)

plt.plot(columns,mean_2012.loc['mean']*1000 , linestyle='--', marker='o',c='b')
plt.plot(columns, mean_2012.loc['25%']*1000, linestyle='--', marker='o',c='darkviolet')
plt.plot(columns, mean_2012.loc['50%']*1000, linestyle='--', marker='o',c='c')
plt.plot(columns, mean_2012.loc['count'], linestyle='', marker='*',c='r',markersize=25)
plt.axhline(y = 50, color = 'r', linestyle = '-',label="Tariff",linewidth = 4)

plt.xlabel("Months",size=30)
plt.ylabel("Monthly_energy_consumption_KWh",size=30)
plt.title('Mean information',size = 40)

tick_size = 25   
#mpl.rcParams['xtick.labelsize'] = tick_size     
plt.tick_params(axis='x', which='major', labelsize = tick_size )
plt.tick_params(axis='y', which='major', labelsize = tick_size )  


handle1 = mlines.Line2D([], [], color='b',
                                  label='Mean', 
                                  linestyle='--',
                                  marker = 'o')
handle2 = mlines.Line2D([], [], color='darkviolet',
                                  label='25%', 
                                  linestyle='--',
                                  marker = 'o')
handle3 = mlines.Line2D([], [], color='c',
                                  label='50%', 
                                  linestyle='-',
                                  )
handle4 = mlines.Line2D([], [], color='r',
                                  label='count', 
                                  linestyle='',
                                  marker ='*',
                                  markersize=25
                                  )

plt.legend(handles=[handle1,handle2,handle3,handle4],
                            bbox_to_anchor=(0.95, -0.07),fontsize = 30,
                            frameon=False,  ncol=3) 
plt.xticks(x,x)        
#plt.savefig('C:/Users/pietr/Spyder/RAMP_spyder/Graphs_comparison/Residential_comparison.png')
plt.show()  

#%% 
'''
index = tropcial_lowlands_energy_analysis['Unnamed: 0']
columns = [1,2,3,4,5,6,7,8,9,10,11,12]
percentiles_25_2012.columns = columns
percentiles_25_2012.index = index


# Plotting the 25% percentile information


x = columns

size = [20,15]
fig=plt.figure(figsize=size)

plt.plot(columns,percentiles_25_2012.loc['mean']*1000 , linestyle='--', marker='o',c='b')
plt.plot(columns, percentiles_25_2012.loc['25%']*1000, linestyle='--', marker='o',c='darkviolet')
plt.plot(columns, percentiles_25_2012.loc['50%']*1000, linestyle='--', marker='o',c='c')

plt.axhline(y = 50, color = 'r', linestyle = '-',label="Tariff",linewidth = 4)

plt.xlabel("Months",size=30)
plt.ylabel("Monthly_energy_consumption_KWh",size=30)
plt.title('25% percentile information',size = 40)

tick_size = 25   
#mpl.rcParams['xtick.labelsize'] = tick_size     
plt.tick_params(axis='x', which='major', labelsize = tick_size )
plt.tick_params(axis='y', which='major', labelsize = tick_size )  


handle1 = mlines.Line2D([], [], color='b',
                                  label='Mean', 
                                  linestyle='--',
                                  marker = 'o')
handle2 = mlines.Line2D([], [], color='darkviolet',
                                  label='25%', 
                                  linestyle='--',
                                  marker = 'o')
handle3 = mlines.Line2D([], [], color='c',
                                  label='50%', 
                                  linestyle='-',
                                  )

plt.legend(handles=[handle1,handle2,handle3],
                            bbox_to_anchor=(0.95, -0.07),fontsize = 30,
                            frameon=False,  ncol=3) 
plt.xticks(x,x)        
#plt.savefig('C:/Users/pietr/Spyder/RAMP_spyder/Graphs_comparison/Residential_comparison.png')
plt.show()  
'''

#%%
index = tropcial_lowlands_energy_analysis['Unnamed: 0']
columns = [1,2,3,4,5,6,7,8,9,10,11,12]
percentiles_50_2012.columns = columns
percentiles_50_2012.index = index


# Plotting the 50% percentile information

# due to the non normality distribution of the data the median and thus the 50th percentile represents at best the behaviour of the dataset 
################### JUST TO PLOT THE AVERAGE OF THE UBN

data_base_validation = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/Validation.database.csv')
column_list_data_base_validation = data_base_validation.columns.values.tolist()

tropcial_lowlands_UBN = []
for i in range(len(tropical_lowlands_codes)):
    d = str(tropical_lowlands_codes[i])
    data_base_validation_tropcial_lowlands = data_base_validation.loc[data_base_validation['CODIGO']== d]
    tropcial_lowlands_UBN.append(data_base_validation_tropcial_lowlands)

tropcial_lowlands_list_UBN = []
for j in (tropcial_lowlands_UBN):
    
    describe_tropcial_lowlands_UBN = 100 - j['%Satisfied basic needs']
    tropcial_lowlands_value_UBN = describe_tropcial_lowlands_UBN.iloc[1]
    tropcial_lowlands_list_UBN.append(tropcial_lowlands_value_UBN)
    
tropcial_lowlands_describe_UBN = ((pd.DataFrame(tropcial_lowlands_list_UBN)).describe())
UBN = (float(tropcial_lowlands_describe_UBN.loc['mean']))

####################################################


x = columns

size = [20,15]
fig=plt.figure(figsize=size)

plt.plot(columns,percentiles_50_2012.loc['75%']*1000 , linestyle='--', marker='o',c='b')
plt.plot(columns, percentiles_50_2012.loc['25%']*1000, linestyle='--', marker='o',c='darkviolet')
plt.plot(columns, percentiles_50_2012.loc['50%']*1000, linestyle='--', marker='o',c='c')
plt.plot(columns, mean_2012.loc['count'], linestyle='', marker='*',c='r',markersize=25)
plt.axhline(y = 50, color = 'r', linestyle = '-',label="Tariff",linewidth = 4)
plt.axhline(y = UBN , color = 'g', linestyle = ':',label=" mean UBN%",linewidth = 4)


plt.xlabel("Months",size=30)
plt.ylabel("Monthly_energy_consumption_KWh",size=30)
plt.title('50% percentile information  Tropical_lowlands',size = 40)
tick_size = 25   
#mpl.rcParams['xtick.labelsize'] = tick_size     
plt.tick_params(axis='x', which='major', labelsize = tick_size )
plt.tick_params(axis='y', which='major', labelsize = tick_size )  


handle1 = mlines.Line2D([], [], color='b',
                                  label='75%', 
                                  linestyle='--',
                                  marker = 'o')
handle2 = mlines.Line2D([], [], color='darkviolet',
                                  label='25%', 
                                  linestyle='--',
                                  marker = 'o')
handle3 = mlines.Line2D([], [], color='c',
                                  label='50%', 
                                  linestyle='-',
                                  )
handle4 = mlines.Line2D([], [], color='r',
                                  label='count', 
                                  linestyle='',
                                  marker ='*',
                                  markersize=25
                                  )

plt.legend(handles=[handle1,handle2,handle3,handle4],
                            bbox_to_anchor=(0.95, -0.07),fontsize = 30,
                            frameon=False,  ncol=3) 
plt.xticks(x,x)        
plt.savefig('D:/poli_new/New_step/Validation_step/Graphs_results/Seasonal_trends/Seasonal_trend_2012_50th_percentile_tropical_lowlands.png')
plt.show()  



#%%


######################## Amazonia


# Filtering process
amazonia_residential_all_months_selected_municipalities = {} # final dictionary with all the filtered information of the beni department
energy_analysis_2012_amazonia_zone = {} # final dictionary with all the fundamental info about the montlhy energy consumption

'''
def months_looping(dict_1,dict_2_energy,department_real_database,codes):
    for j in range (1,13):
        energy_analysis_2012 = {}
        data_base_residential_municipality_dict_2012 = {}
        
        real_data_base_month = department_real_database.loc[department_real_database['MONTH']==j]
        
        for i in range(len(codes)):
            data_base_munipality = real_data_base_month.loc[real_data_base_month['COD_MUNI'] == codes[i]]
            data_base_residential_municipality_dict_2012[i] = dict(data_base_munipality)
            energy_analysis_2012[i] = dict(chaco_data_base_residential_municipality_dict_2012[i]['CONS_LEI_MWH'].describe())
'''
            


for j in range (1,13): # looping the months 
    
    energy_analysis_2012 = {}
    amazonia_data_base_residential_municipality_dict_2012 = {}
    amazonia_real_data_base_month = big_real_data_base.loc[big_real_data_base['MONTH']==j]
    
    
    # Filter directily with the municipal codes
    for i in range (len(amazonia_codes)): #looping on the first codes --> improvement : looping on a list of the different municipal codes could be the best way to do it
                
                amazonia_data_base_munipality = amazonia_real_data_base_month.loc[amazonia_real_data_base_month['COD_MUNI'] == amazonia_codes[i]]
                amazonia_data_base_munipality_residential = amazonia_data_base_munipality.loc[amazonia_data_base_munipality['CATEGORY']==1]
                amazonia_data_base_munipality_residential_2012 = amazonia_data_base_munipality_residential.loc[amazonia_data_base_munipality_residential['YEAR']==2012]
                amazonia_data_base_residential_municipality_dict_2012[i] = dict(amazonia_data_base_munipality_residential_2012)
                energy_analysis_2012[i] = dict(amazonia_data_base_residential_municipality_dict_2012[i]['CONS_LEI_MWH'].describe())

    amazonia_residential_all_months_selected_municipalities[j] = dict(amazonia_data_base_residential_municipality_dict_2012)
    energy_analysis_2012_amazonia_zone[j] = dict (energy_analysis_2012)
#%% 

#%% Now we should work on the energy dict 


energ_describe_final_dict ={}
gen_energy_describe_final = pd.DataFrame()
gen_energy_info_all_municipalities = []
a = list(energy_analysis_2012_amazonia_zone[1][1].keys()) # they are always the same
 

for j in range (1,13): #looping of the months

    for columns in range(0,8): # looping on the columns /data that are the results of the describe function
        
        
        
        for i in range (len(amazonia_codes)): # differentiation for the munipalities --> you should find a way in order to do that in auto 
            
            gen_energy_describe_info = energy_analysis_2012_amazonia_zone [j][i][a[columns]] 
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
    over_all_energy_anergy_analysis_dic.to_excel('D:/poli_new/New_step/Validation_step/Results_amazonia/amazonia_energy_analysis_%d.xlsx' %j)

    gen_energy_describe_final = pd.DataFrame()
    energ_describe_final_dict[j] = dict(over_all_energy_anergy_analysis_dic)
    
over_all_energy_anergy_analysis_dic = pd.DataFrame()
clean_database = pd.DataFrame() 


#%%
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
import os 
import matplotlib.lines as mlines

#Plotting of the seasonal behavior 2012
mean_2012 = pd.DataFrame()
percentiles_25_2012 = pd.DataFrame()
percentiles_50_2012 = pd.DataFrame()
percentiles_75_2012 = pd.DataFrame()

for j in range(1,13):
    amazonia_energy_analysis = pd.read_excel('D:/poli_new/New_step/Validation_step/Results_amazonia/amazonia_energy_analysis_%d.xlsx' %j) 
    mean_column = amazonia_energy_analysis['mean']
    percentiles_25 = amazonia_energy_analysis['25%']
    percentiles_50 = amazonia_energy_analysis['50%']
    percentiles_75 = amazonia_energy_analysis['75%']
    mean_2012 = pd.concat([mean_2012,mean_column],ignore_index= False,axis=1)
    percentiles_25_2012 = pd.concat([percentiles_25_2012,percentiles_25],ignore_index= False,axis=1)
    percentiles_50_2012 = pd.concat([percentiles_50_2012,percentiles_50],ignore_index= False,axis=1)
    percentiles_75_2012 = pd.concat([percentiles_75_2012,percentiles_75],ignore_index= False,axis=1)

index = amazonia_energy_analysis['Unnamed: 0']
columns = [1,2,3,4,5,6,7,8,9,10,11,12]
mean_2012.columns = columns
mean_2012.index = index

### checking for the outliers and checking for if datas have a normal distribution 

a = mean_2012.loc['mean']*1000
#b = percentiles_25_2012.loc['mean']*1000
filtering_mean = a[(np.abs(stats.zscore(a))<3)]
a.hist()
#b.hist()

#%%
## Plotting MEAN --> but wh have already checked that because of the non-nomrality distribution then the mean does not represent the data in a good way.
x = columns

size = [20,15]
fig=plt.figure(figsize=size)

plt.plot(columns,mean_2012.loc['mean']*1000 , linestyle='--', marker='o',c='b')
plt.plot(columns, mean_2012.loc['25%']*1000, linestyle='--', marker='o',c='darkviolet')
plt.plot(columns, mean_2012.loc['50%']*1000, linestyle='--', marker='o',c='c')
plt.plot(columns, mean_2012.loc['count'], linestyle='', marker='*',c='r',markersize=25)
plt.axhline(y = 50, color = 'r', linestyle = '-',label="Tariff",linewidth = 4)

plt.xlabel("Months",size=30)
plt.ylabel("Monthly_energy_consumption_KWh",size=30)
plt.title('Mean information',size = 40)

tick_size = 25   
#mpl.rcParams['xtick.labelsize'] = tick_size     
plt.tick_params(axis='x', which='major', labelsize = tick_size )
plt.tick_params(axis='y', which='major', labelsize = tick_size )  


handle1 = mlines.Line2D([], [], color='b',
                                  label='Mean', 
                                  linestyle='--',
                                  marker = 'o')
handle2 = mlines.Line2D([], [], color='darkviolet',
                                  label='25%', 
                                  linestyle='--',
                                  marker = 'o')
handle3 = mlines.Line2D([], [], color='c',
                                  label='50%', 
                                  linestyle='-',
                                  )
handle4 = mlines.Line2D([], [], color='r',
                                  label='count', 
                                  linestyle='',
                                  marker ='*',
                                  markersize=25
                                  )

plt.legend(handles=[handle1,handle2,handle3,handle4],
                            bbox_to_anchor=(0.95, -0.07),fontsize = 30,
                            frameon=False,  ncol=3) 
plt.xticks(x,x)        
#plt.savefig('C:/Users/pietr/Spyder/RAMP_spyder/Graphs_comparison/Residential_comparison.png')
plt.show()  

#%% 
'''
index = amazonia_energy_analysis['Unnamed: 0']
columns = [1,2,3,4,5,6,7,8,9,10,11,12]
percentiles_25_2012.columns = columns
percentiles_25_2012.index = index


# Plotting the 25% percentile information


x = columns

size = [20,15]
fig=plt.figure(figsize=size)

plt.plot(columns,percentiles_25_2012.loc['mean']*1000 , linestyle='--', marker='o',c='b')
plt.plot(columns, percentiles_25_2012.loc['25%']*1000, linestyle='--', marker='o',c='darkviolet')
plt.plot(columns, percentiles_25_2012.loc['50%']*1000, linestyle='--', marker='o',c='c')

plt.axhline(y = 50, color = 'r', linestyle = '-',label="Tariff",linewidth = 4)

plt.xlabel("Months",size=30)
plt.ylabel("Monthly_energy_consumption_KWh",size=30)
plt.title('25% percentile information',size = 40)

tick_size = 25   
#mpl.rcParams['xtick.labelsize'] = tick_size     
plt.tick_params(axis='x', which='major', labelsize = tick_size )
plt.tick_params(axis='y', which='major', labelsize = tick_size )  


handle1 = mlines.Line2D([], [], color='b',
                                  label='Mean', 
                                  linestyle='--',
                                  marker = 'o')
handle2 = mlines.Line2D([], [], color='darkviolet',
                                  label='25%', 
                                  linestyle='--',
                                  marker = 'o')
handle3 = mlines.Line2D([], [], color='c',
                                  label='50%', 
                                  linestyle='-',
                                  )

plt.legend(handles=[handle1,handle2,handle3],
                            bbox_to_anchor=(0.95, -0.07),fontsize = 30,
                            frameon=False,  ncol=3) 
plt.xticks(x,x)        
#plt.savefig('C:/Users/pietr/Spyder/RAMP_spyder/Graphs_comparison/Residential_comparison.png')
plt.show()  
'''

#%%
index = amazonia_energy_analysis['Unnamed: 0']
columns = [1,2,3,4,5,6,7,8,9,10,11,12]
percentiles_50_2012.columns = columns
percentiles_50_2012.index = index


# Plotting the 50% percentile information

# due to the non normality distribution of the data the median and thus the 50th percentile represents at best the behaviour of the dataset 
################### JUST TO PLOT THE AVERAGE OF THE UBN

data_base_validation = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/Validation.database.csv')
column_list_data_base_validation = data_base_validation.columns.values.tolist()

amazonia_UBN = []
for i in range(len(amazonia_codes)):
    d = str(amazonia_codes[i])
    data_base_validation_amazonia = data_base_validation.loc[data_base_validation['CODIGO']== d]
    amazonia_UBN.append(data_base_validation_amazonia)

amazonia_list_UBN = []
for j in (amazonia_UBN):
    
    describe_amazonia_UBN = 100 - j['%Satisfied basic needs']
    amazonia_value_UBN = describe_amazonia_UBN.iloc[1]
    amazonia_list_UBN.append(amazonia_value_UBN)
    
amazonia_describe_UBN = ((pd.DataFrame(amazonia_list_UBN)).describe())
UBN = (float(amazonia_describe_UBN.loc['mean']))

####################################################


x = columns

size = [20,15]
fig=plt.figure(figsize=size)

plt.plot(columns,percentiles_50_2012.loc['75%']*1000 , linestyle='--', marker='o',c='b')
plt.plot(columns, percentiles_50_2012.loc['25%']*1000, linestyle='--', marker='o',c='darkviolet')
plt.plot(columns, percentiles_50_2012.loc['50%']*1000, linestyle='--', marker='o',c='c')
plt.plot(columns, mean_2012.loc['count'], linestyle='', marker='*',c='r',markersize=25)
plt.axhline(y = 50, color = 'r', linestyle = '-',label="Tariff",linewidth = 4)
plt.axhline(y = UBN , color = 'g', linestyle = ':',label=" mean UBN%",linewidth = 4)


plt.xlabel("Months",size=30)
plt.ylabel("Monthly_energy_consumption_KWh",size=30)
plt.title('50% percentile information  Amazonia',size = 40)
tick_size = 25   
#mpl.rcParams['xtick.labelsize'] = tick_size     
plt.tick_params(axis='x', which='major', labelsize = tick_size )
plt.tick_params(axis='y', which='major', labelsize = tick_size )  


handle1 = mlines.Line2D([], [], color='b',
                                  label='75%', 
                                  linestyle='--',
                                  marker = 'o')
handle2 = mlines.Line2D([], [], color='darkviolet',
                                  label='25%', 
                                  linestyle='--',
                                  marker = 'o')
handle3 = mlines.Line2D([], [], color='c',
                                  label='50%', 
                                  linestyle='-',
                                  )
handle4 = mlines.Line2D([], [], color='r',
                                  label='count', 
                                  linestyle='',
                                  marker ='*',
                                  markersize=25
                                  )

plt.legend(handles=[handle1,handle2,handle3,handle4],
                            bbox_to_anchor=(0.95, -0.07),fontsize = 30,
                            frameon=False,  ncol=3) 
plt.xticks(x,x)        
plt.savefig('D:/poli_new/New_step/Validation_step/Graphs_results/Seasonal_trends/Seasonal_trend_2012_50th_percentile_amazonia.png')
plt.show()  
