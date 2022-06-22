# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 15:28:43 2022

@author: pietr
"""

import pandas as pd

def string_check(database,column_check,dictionary):
    
    database.index = range(len(database))
    a = 0 
    for i in range(len(database)):
        if i == 0 :
            list_string = [database[column_check].loc[0]]
            
        else:
            
            if database[column_check].loc[i] in list_string:
                a = a + 1 
          
            else:
                
                list_string.append(database[column_check].loc[i])
        
        for j in list_string:
            data_base_filtered = database.loc[database[column_check]==j]
            dictionary[j] = dict(data_base_filtered)


            
    return dictionary
#%% filtering the list of municipalities that Claudia gave me 

municipalities_selection = pd.read_excel('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/municipalities_selection_final.xlsx')
column_list_municiapalities_selection = municipalities_selection.columns.values.tolist()


municipalities_selection_rural = municipalities_selection.loc[municipalities_selection['Tasa de urbanización, 2012 (% de población)']==0]
municipio_column = municipalities_selection_rural['Municipio']
# Next step should be to associate this municipalities with a value of altitude in order to use that variable for the zone differentiation
# this step is done  because in the real database we do not have a proper communitiy identification but only a bunch of users related to a certian municipality
# Thus now we try to assosiate the name of the munipio with the Onset database in order to then evaluate a sort of average of the altitude of all the communities that constitute each municipality
# Thus in this way we are alble to a symbolic altitude associated to a municipality.

#%%

data_base_validation = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/Validation.database.csv')

departments = ['La Paz', 'Cochabamba','Beni', 'Potosi', 'Oruro', 'Santa Cruz','Tarija' ,'Pando','Chuquisaca']


#%% municipalities grouping

data_base_depto_dict = {}


a = 0 
for department in departments:
    data_base_municipalities_dict = {}
    data_base_depto = data_base_validation.loc[data_base_validation['Depto']== department]
    data_base_depto.index = range(len(data_base_depto))
    for i in range(len(data_base_depto)):
        if i == 0 :
        # i = 0 first round 
            list_municipalities = [data_base_depto['Municipio'].loc[0]]
        else:
            
            if data_base_depto['Municipio'].loc[i] in list_municipalities:
                a = a+1 # not needed
            else:
                
                list_municipalities.append(data_base_depto['Municipio'].loc[i])
                
    for municipalities in list_municipalities:
            
        data_base_municipalities = data_base_depto.loc[data_base_depto['Municipio']==municipalities]
        data_base_municipalities_dict[municipalities] = dict(data_base_municipalities)
        
    
    data_base_depto_dict[department] = dict(data_base_municipalities_dict)

'''
#for the slicing of the name of the municipalities
string = 'Cuarta SecciÃ³n - Rurrenabaque'
string_sliced = string.partition('-'[0])
b= string_sliced[2]



# Huacaya finding the string match for the finidng of the right municipalities

aaa = ['jonny','jonny2','asdasdasdHuacaya']

# Carangas --> for oruro department

str_match = data_base_depto.loc[(s for s in data_base_depto['Municipio']  if "Carangas" in s).index]
str_match = [s for s in data_base_depto['Municipio']  if "Carangas" in s]
a = pd.DataFrame(str_match)
for i in range(len(str_match)):
    element = data_base_depto.loc[data_base_depto.loc(i)]
    '''
#%%
# merging the information of the two database in order to get an average values for the municipalities of : Altitude and UBN
# the method used is a string reaserch in each database 


municipalities_selection = pd.read_excel('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/municipalities_selection_final.xlsx')
column_list_municiapalities_selection = municipalities_selection.columns.values.tolist()


municipalities_selection_rural = municipalities_selection.loc[municipalities_selection['Tasa de urbanización, 2012 (% de población)']==0]
municipalities_selection_rural['Altitude'] = ''
municipalities_selection_rural['% unsatisfied basic needs'] = ''
municipalities_selection_rural.index = range(len(municipalities_selection_rural))

    #df[df['A'].str.contains(i)]
for keys in data_base_depto_dict:
    
    for i in range(len(municipalities_selection_rural['Municipio'])):
        
        a = municipalities_selection_rural.loc[i,['Municipio']]
        b = ''.join([str(elem) for elem in a])
        res = [val for key, val in data_base_depto_dict[keys].items() if b  in key]
        if len(res) == 0:
            c = 10 
        else:
            
            describe_altitude = res[0]['Elevation'].describe()    
            describe_poverty_level_UBN = res[0]['%Satisfied basic needs'].describe()    
            municipalities_selection_rural.loc[i,['Altitude']] = describe_altitude.loc['mean']
            municipalities_selection_rural.loc[i,['% unsatisfied basic needs']] = 100 - describe_poverty_level_UBN.loc['mean']

# IMP: problem with municipalities with the same name across different department and problem with the different type of writing of the municipalities

    
    
municipalities_selection_rural.to_excel('D:/poli_new/New_step/Validation_step/municipalities_selection_filtered.xlsx')      

    
#%%
#%% municipalities grouping USING THE MUNICIPAL CODE INSTEAD OF THE NAME OF THE MUNICIPALITIES

### the results found are not in line with the information about the real number of the municipalities insiede each department 
# Why is that ? how is it possible that the number of municipalities is so much bigger ? 


data_base_depto_dict_codigo = {}


a = 0 
for department in departments:
    data_base_municipalities_dict = {}
    data_base_depto = data_base_validation.loc[data_base_validation['Depto']== department]
    data_base_depto.index = range(len(data_base_depto))
    for i in range(len(data_base_depto)):
        if i == 0 :
        # i = 0 first round 
            list_municipalities = [data_base_depto['CODIGO'].loc[0]]
        else:
            
            if data_base_depto['CODIGO'].loc[i] in list_municipalities:
                a = a+1 # not needed
            else:
                
                list_municipalities.append(data_base_depto['CODIGO'].loc[i])
                
    for municipalities in list_municipalities:
            
        data_base_municipalities = data_base_depto.loc[data_base_depto['CODIGO']==municipalities]
        data_base_municipalities_dict[municipalities] = dict(data_base_municipalities)
        
    
    data_base_depto_dict_codigo[department] = dict(data_base_municipalities_dict)    
    
#%%


municipalities_selection = pd.read_excel('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/municipalities_selection_final.xlsx')
column_list_municiapalities_selection = municipalities_selection.columns.values.tolist()


municipalities_selection_rural = municipalities_selection.loc[municipalities_selection['Tasa de urbanización, 2012 (% de población)']==0]
municipalities_selection_rural['Altitude'] = ''
municipalities_selection_rural.index = range(len(municipalities_selection_rural))

    #df[df['A'].str.contains(i)]
for keys in data_base_depto_dict:
    
    for i in range(len(municipalities_selection_rural['Código'])):
        
        a = municipalities_selection_rural.loc[i,['Código']]
        b = ''.join([str(elem) for elem in a])
        res = [val for key, val in data_base_depto_dict[keys].items() if b  in key]
        if len(res) == 0:
            c = 10 
        else:
            
            describe_altitude = res[0]['Elevation'].describe()    
            municipalities_selection_rural.loc[i,['Altitude']] = describe_altitude.loc['mean']


# IMP: problem with municipalities with the same name across different department and problem with the different type of writing of the municipalities

    
municipalities_selection_rural.to_excel('D:/poli_new/New_step/Validation_step/municipalities_selection_filtered.xlsx')      



#%%
# Reading the selection of the municipalities that we have done and divide then using the altidute criteria defnided by Claudia
import pandas as pd


final_municipalities = pd.read_excel('D:/poli_new/New_step/Validation_step/municipalities_selection_filtered.xlsx')


# Highlands > 3000

highlands_municipalities = final_municipalities.loc[final_municipalities['Altitude']>3000]


# Valleys  1500 < altitude < 3000
valleys_municipalities = final_municipalities.loc[final_municipalities['Altitude']<3000]
valleys_municipalities = valleys_municipalities.loc[valleys_municipalities['Altitude']>1500]

# Lowlands Chaco and Amazzonia < 1500 
general_lowlands = final_municipalities.loc[final_municipalities['Altitude']<1500]


#%% Counting the missing information about the municipialities 
# it should be 30 municipalities that are missing out of 175 --> could be accetable but it could be also rresolved?
import numpy as np

missing = np.where(municipalities_selection_rural.applymap(lambda x: x == ''))


missing_values = pd.DataFrame(missing)
missing_values = missing_values.drop(1)
missing_values = missing_values.transpose()

for keys in data_base_depto_dict_codigo:
    
    for i in missing_values:
         a = missing_values.loc[i].values
         a = municipalities_selection_rural.loc[missing_values.loc[i].values,'Código']
         a.index = range(len(a))
         filtered = data_base_validation.loc[data_base_validation['CODIGO']==20701]

         

    
        
    

    
    
