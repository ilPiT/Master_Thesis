# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 15:11:47 2022

@author: pietr
"""

import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
import os 
import matplotlib.lines as mlines


data_base = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/Database_new.csv')
data_base_CNPV2012 = pd.read_excel('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/CNPV2012.xlsx') # Area : Rural or Urban 
data_base_Population_poverty2012 = pd.read_excel('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/Population_Poverty2012.xlsx',sheet_name = 'Database 2012',header= 1)
#OSS: actually it could be interesting to have a database where there are only the variables that we need to identifiy so that it could be more impactfull at first sight

#creating a new databse with all relevant information for the validation of the residential energy consumption

# FIRST: filtering for just the rural villages --> IsUrban

data_base_CNPV2012_rural = data_base_CNPV2012[data_base_CNPV2012['Area']=='Rural']
data_base_rural = data_base[data_base['IsUrban']==0] # pointid
data_base_Population_poverty2012_rural = data_base_Population_poverty2012[data_base_Population_poverty2012['IsUrban']==0] # pointid

# SECOND : filtering only the communities that are connected with the grid --> more reliable data
'''
data_base_CNPV2012_rural = data_base_CNPV2012_rural_no_grid[data_base_CNPV2012_rural_no_grid[]==]
data_base_rural = data_base_rural_no_grid[data_base_rural_no_grid['IsUrban']==0]
data_base_Population_poverty2012_rural = data_base_Population_poverty2012_rural_no_grid[data_base_Population_poverty2012_rural_no_grid['IsUrban']==0] # pointid
'''


#%%  verification step --> NOT NCESESSARY for the json file creation process

### ROUNDING PROCESS used then for the verification of the overlapping data from the database --> in this case for the X coordiantes

data_base_Population_poverty2012_rural['X_deg']= data_base_Population_poverty2012_rural['X_deg'].round(3)
data_base_CNPV2012_rural['POINT_X']= data_base_CNPV2012_rural['POINT_X'].round(3)


# verifying that we have the same villages for each different databse --> for sure the process can be imporved: still not really smart code lines

#### verification by point id  

data_base_Population_poverty2012_rural['pointid'].equals(data_base_rural['pointid']) # not working i don't know why

b = data_base_Population_poverty2012_rural['pointid']==data_base_rural['pointid'] # boolean series , not really usefull for the moment

#f = range(0,len(data_base_CNPV2012_rural)) # check for the correctness of the range 

for i in range(0,len(data_base_CNPV2012_rural)):

    if data_base_rural['pointid'].iloc[i] == data_base_Population_poverty2012_rural['pointid'].iloc[i]:
        i= i+1
    else :
        print ( 'something is not working')
        
#### this two databse are ok in terms of pointid

# check for the only one left data_base_CNPV2012 --> you will see that there is an error for what concerns the pointid thus we proceed checking the X coordinates and everything is ok 

j = 0
error = []
error_x =[]
error_x_deg =[]
counting = 0
        
for j in range(0,len(data_base_CNPV2012_rural)):
    
    if data_base_rural['pointid'].iloc[j] == data_base_CNPV2012_rural['OBJECTID'].iloc[j]:
        j= j+1
    else :
        error_value = data_base_CNPV2012_rural['OBJECTID'].iloc[j]
        error.append(error_value)
        
        error_value_x = data_base_CNPV2012_rural['POINT_X'].iloc[j]
        error_value_x_deg = data_base_Population_poverty2012_rural['X_deg'].iloc[j]
        
        error_x.append(error_value_x)
        error_x_deg.append(error_value_x_deg)
        #comparison = pd.concat([error_x, error,  error_x_deg], axis=1)
       
        if data_base_Population_poverty2012_rural['X_deg'].iloc[j] == data_base_CNPV2012_rural['POINT_X'].iloc[j]:
            
           #print ( 'just a missing index because the X coordinates are the same') # there is no 4971 dunque all the others sono sfasati di due invece che di uno rspetto agli indici 
           counting = counting + 1 

coordinate_x_check = error_x == error_x_deg


b = 0
i = 0 
for i in range(0,len(error_x)):
    
    if  error_x[i] == error_x_deg[i]:
        b = b + 1  
    else: 
            print ('the list are not identical for what concerns the indexes  ', i )
            
            
# thus at the end all the elements of the three database rural are refferred to the same rural village because we have verified the X  coordinates to be 100% sure it should be done for also the other databse and also for the Y coordinates

#%%

#### Actual selection of the relevant columns from each database thus creation of the validation_databse

# Also this can be improved in terms of coding

data_base_validation = pd.DataFrame()
columns = []

# columns selection

# First DATA BASE

column_list = data_base_Population_poverty2012_rural.columns.values.tolist() # super usefull

# useless but it gies a list of all the data used in an effective way

columns.append(data_base_Population_poverty2012_rural['Pop']) 
columns.append(data_base_Population_poverty2012_rural['% No poor population in 2012']) 
columns.append(data_base_Population_poverty2012_rural['%Poor population in 2012']) 
columns.append(data_base_Population_poverty2012_rural['index_pov']) 
columns.append(data_base_Population_poverty2012_rural['Households 2012']) 
columns.append(data_base_Population_poverty2012_rural['Electrification rate']) 

columns.append(round(data_base_Population_poverty2012_rural['Pop']/data_base_Population_poverty2012_rural['Households 2012'])) # fake it is just 4 always --> check maybe is not just because there is the rounding applied 
columns.append(data_base_Population_poverty2012_rural['Pop']/data_base_Population_poverty2012_rural['Households 2012']) #  the real number is 3.57 people per household --> but this number is not really usefull for anything


first = data_base_Population_poverty2012_rural[['Pop','% No poor population in 2012','%Poor population in 2012','index_pov','Electrification rate','COD_DEP']]

# Second DATA BASE

column_list1 = data_base_rural.columns.values.tolist() 

# useless
columns.append(data_base_rural['Elevation'])
columns.append(data_base_rural['RoadDist']) # distance in Km from the network
columns.append(data_base_rural['TravelHours']) # travel time to large city in hours


# GridCellArea ,ElectrificationOrder , Electrific , Actual_Elec_Status_2012 , FinalElecCode2012 , GridClassification

research_data = data_base_rural[['GridCellArea','ElectrificationOrder','Electrific','Actual_Elec_Status_2012','FinalElecCode2012','GridClassification']]
research_data_1 = data_base_rural[['CurrentMVLineDist','CurrentHVLineDist','PlannedHVLineDist','PlannedMVLineDist']]
research_data_1 = research_data_1[research_data_1['CurrentMVLineDist']<=2] 
 

second = data_base_rural[['Elevation','RoadDist','TravelHours']]

# Third  DATA BASE

column_list2 = data_base_CNPV2012_rural.columns.values.tolist()

# useless
columns.append(data_base_CNPV2012_rural['Provincia']) 
columns.append(data_base_CNPV2012_rural['Municipio']) 
columns.append(data_base_CNPV2012_rural['Comunidad'])
columns.append(data_base_CNPV2012_rural['Hog_Elec']) # hogares x electrification rate
columns.append(data_base_CNPV2012_rural['Hogares'])

third = data_base_CNPV2012_rural[['Provincia','Municipio','Comunidad','Hog_Elec','Hogares']]

#Cobertura

## New data_base used for the validation process of the residential sector

data_base_validation = pd.concat([first,second,third ],axis=1)
column_list_validation = data_base_validation.columns.values.tolist()
data_base_validation.to_csv('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/Validation.database.csv')


#%% Further filtering test

provincia_filtering = data_base_validation.loc[data_base_validation['Provincia']=='Cercado'] # beni dipartment

municipality_filtering_soracachi = data_base_validation.loc[data_base_validation['Municipio']=='Tercera SecciÃ³n - Soracachi'] # from this we know the number of communities that are present in the municipality that has been selected
municipality_filtering_elchoro = data_base_validation.loc[data_base_validation['Municipio']=='Segunda SecciÃ³n - El Choro'] # from this we know the number of communities that are present in the municipality that has been selected

municipality_filtering_elchoro_zona_norte = municipality_filtering_elchoro.loc[municipality_filtering_elchoro['Comunidad']=='ZONA NORTE'] # from this we know the number of communities that are present in the municipality that has been selected



#  IMP : good for selecting the rows where you need a certain condition on a certain column
#select_color = df.loc[df['Color'] == 'Green']


#%%

beni_real_data_base = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/beni_sd.csv')
chuquisaca_real_data_base = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/chuquisaca_sd.csv')

column_list_beni = beni_real_data_base.columns.values.tolist()
column_list_chuquisaca = chuquisaca_real_data_base.columns.values.tolist()

z = beni_real_data_base.head(5000)

# Filtering the data form Beni department 

# First going for the Category 1 that should be the residential sector 

beni_data_base_residential = beni_real_data_base.loc[beni_real_data_base['CATEGORY'] == 1]
chuquisaca_data_base_residential = chuquisaca_real_data_base.loc[chuquisaca_real_data_base['CATEGORY'] == 1]

# Second filtering for the Month of Genuary 

beni_data_base_residential_gen = beni_data_base_residential.loc[beni_data_base_residential['MONTH']==1]
chuquisaca_data_base_residential_gen = chuquisaca_data_base_residential.loc[chuquisaca_data_base_residential['MONTH']==1]

# checking some characteristics about the dist_systems --> don't think it is really usefull

Dist_system_beni =  beni_data_base_residential_gen['DIST_SYSTEM']
Dist_system_chuquisaca =  chuquisaca_data_base_residential_gen['DIST_SYSTEM']
aaaa = Dist_system_beni.describe()
bbbb = Dist_system_chuquisaca.describe()
# Third filtering for COD_Muni

beni_data_base_residential_gen_muni_filter_1 = beni_data_base_residential_gen.loc[beni_data_base_residential_gen['COD_MUNI']==80101]
beni_data_base_residential_gen_muni_filter_2 = beni_data_base_residential_gen.loc[beni_data_base_residential_gen['COD_MUNI']==80301] # it could be the municipality of el Choro !!!

# thus now we should be albe to filter in order to define the different communities inside a specific municipality i guess
# thus it could be usefull to have a list of all the communities that are present for each municipality code 


# filtering for address example : SAN PEDRO community

beni_data_base_residential_gen_muni_filter_2_address_norte = beni_data_base_residential_gen_muni_filter_2.loc[beni_data_base_residential_gen_muni_filter_2['ADDRESS']=='NORTE']
beni_data_base_residential_gen_muni_filter_2_address_zonanorte = beni_data_base_residential_gen_muni_filter_2.loc[beni_data_base_residential_gen_muni_filter_2['ADDRESS']=='ZONA NORTE']

# thus we have obtained a first sample of the database that now can be analyzed 


# alla ricerca della comunità di SAN PEDRO nel validation database

mission_impossible = data_base_validation.loc[data_base_validation['Comunidad']== 'SAN PEDRO']

# i have selcted all the communities named SAN PEDRO IN BOLIVIA then I should try to differentiate for departments using the provincie

 # IMPROVEMENTS : for sure it can be done with a cycle you just need to create a variable containing all the strings that rapresent the Provincia of Beni  and thus concat all the information 

mission_impossible_beni_1_province = mission_impossible.loc[mission_impossible['Provincia']=='Cercado'] # check
mission_impossible_beni_2_province = mission_impossible.loc[mission_impossible['Provincia']=='Vaca DÃ­ez'] # check not sure 100 %
mission_impossible_beni_3_province = mission_impossible.loc[mission_impossible['Provincia']=='JosÃ© BalliviÃ¡n'] # check 
mission_impossible_beni_4_province = mission_impossible.loc[mission_impossible['Provincia']=='Yacuma'] # check 
mission_impossible_beni_5_province = mission_impossible.loc[mission_impossible['Provincia']=='Moxos']
mission_impossible_beni_6_province = mission_impossible.loc[mission_impossible['Provincia']=='Marban']
mission_impossible_beni_7_province = mission_impossible.loc[mission_impossible['Provincia']=='Mamorè']
mission_impossible_beni_8_province = mission_impossible.loc[mission_impossible['Provincia']=='ItÃ©nez'] # check 

#%% Process for the creation of the different scripts --> probably it will be replaced by a json solution


for i in range (0,3) : # 0 , 1 ,2
    
    if data_base['IsUrban'].iloc[i] ==0 :
        with open('C:/Users/pietr/Spyder/RAMP_spyder/RAMP/input_file_original_DSC.py') as file:
         lines = [line for line in file if line.rstrip() != ''] 
         print(*lines[16:18]) #lines in which there are interested variables
    
    ## setting of the variables   
        Alt = data_base['Elevation'].iloc[i]
        lines[16] = Alt
        lines[16] = str(lines[16]) # just a file type conversion to transform the variable into a string
        lines[16] = str('Alt = '+ lines[16])
        
        P = data_base['Pop'].iloc[i]
        lines[17] = P
        lines[17] = str(lines[17]) # just a file type conversion to transform the variable into a string 
        lines[17] = str('P = '+ lines[17])
             
        
        with open('C:/Users/pietr/Spyder/RAMP_spyder/RAMP/input_file_original_DSC.py', 'w') as outfile:
            outfile.write('\n'.join(lines))
            
        with open('C:/Users/pietr/Spyder/RAMP_spyder/RAMP/input_file_original_DSC.py') as new_input:
            all_text = [line for line in new_input if line.rstrip() != ''] 
            
        #  i= i +1 # this is just to avoid having a input_file_0 but it could be canceled
        #with open('C:/Users/pietr/Spyder/RAMP_spyder/Inputs_files/input_file_%d.py' % i, 'w') as new_file:
        with open('input_file_%d.py' % i, 'w') as new_file:
            new_file.write('\n'.join(all_text))
    
    else: # if i want an easy run of RAMP run then i can delete these two lines
        print(str(i) + ' Community is not a rural')
     

# OSS: there could be a problem with the RAMP_run because the indexes are not linear , thus a solution could be just to run also for not rural communities or adjust the database in order to comprehend just rural communities
        


#%%  

# Using JSON insted of dat.dat  to store all the important information needed for the modelling of the inputfiles in RAMP 

import json
import pandas as pd


data_base = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/Database_new.csv')
data_base_validation_first_draft = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/Validation.database.csv')

with open('C:/Users/pietr/Spyder/RAMP_spyder/Initializing_json/Initial_input_file/Initial_data.json','r') as f :
    data = json.load(f) # there is not the s since now it is a json file
    
## the object series in not possible to have it in json
'''
data['Alt'] = data_base['Elevation']
data['Pop'] = data_base['Pop']
data['House_number'] = data_base['Pop']/data['People_per_household']

data['Low_income'] = round(data['House_number'].astype(int)*data['Poverty_rate']/100)
data['High_income'] = round(data['House_number'] - data['Low_income'] )


data['n_Public_lighting'] = (data['House_number']/10)

data['n_Water_system'] = (data['House_number']/100)
'''


# OSS: then here i could create a json file that select single indexes and then create a json file for the input_file for example

all_input_files = list()
for i in range(0,3):
    
    with open('C:/Users/pietr/Spyder/RAMP_spyder/Initializing_json/Output_files/Fundamental_first_output_%d.json' %i,'w') as f:  # you put a new name of the file because in this way we are creating a new file that it will be open in write mode 
        data['Alt'] = int(data_base_validation_first_draft['Elevation'].iloc[i])
        data['Pop'] =int(data_base_validation_first_draft['Pop'].iloc[i])
        data['House_number'] = int(data['Pop']/data['People_per_household'])
        data['Low_income'] = round(data['House_number']*data['Poverty_rate']/100)
        data['High_income'] = round(data['House_number'] - data['Low_income'] )
        data['Elevation_transition'] = 3000
        
        data['n_Public_lighting'] = int(data['House_number']/10)
        data['n_Water_system'] =int (data['House_number']/100)
        
        
        json.dump(data, f, indent=4)   # you first put the data that you wanna dump and then the file i wanna dump it to 
    
    with open('C:/Users/pietr/Spyder/RAMP_spyder/Initializing_json/Output_files/Fundamental_data_users/lowlands%d.json' %i, 'w') as f:
        
        d_lowlands = {}
        #### Lowlands

############ Defining the number of users for the IGA Agricultural ##############

        d_lowlands['n_LL_agro_productive_unit'] = int(round(data['House_number']/80))
    
        d_lowlands['n_LL_irrigation_water'] = int(round(data['House_number']/18))
         
       ############ Defining the number of users for the IGA NON-agricultural ##############
        
        d_lowlands['n_LL_grocery_store'] = int(round(data['House_number']/30))
        d_lowlands['n_LL_restaurant'] = int(round(data['House_number']/30))
        d_lowlands['n_LL_workshop'] = int(round(data['House_number']/60))
        d_lowlands['n_LL_entertainment_business'] = int(round(data['House_number']/60))
        
         
                
        json.dump(d_lowlands,f,indent = 4 )
   
        
        
    with open('C:/Users/pietr/Spyder/RAMP_spyder/Initializing_json/Output_files/Fundamental_data_users/highlands%d.json' %i, 'w') as f:
        

        d_highlands = {}
        #### Highlands

############ Defining the number of users for the IGA Agricultural ##############

        d_highlands['n_HI_agro_productive_unit'] = int(round(data['House_number']/200))
    
        d_highlands['n_HI_irrigation_water'] = int(round(data['House_number']/30))
         
       ############ Defining the number of users for the IGA NON-agricultural ##############
        
        d_highlands['n_HI_grocery_store'] = int(round(data['House_number']/25))
        d_highlands['n_HI_restaurant'] =  int(round(data['House_number']/30))
        d_highlands['n_HI_workshop'] = int(round(data['House_number']/80))
        d_highlands['n_HI_entertainment_business'] = int(round(data['House_number']/100))
        
         
                
        json.dump(d_highlands,f,indent = 4 )
        



    if (data['Alt'] <= data['Elevation_transition']):
        
        with open('C:/Users/pietr/Spyder/RAMP_spyder/Initializing_json/Output_files/Final_input_file%d.json' %i, 'w') as f:
            json.dump([data,d_lowlands],f, indent = 4)
            
            
            
    else:
        with open('C:/Users/pietr/Spyder/RAMP_spyder/Initializing_json/Output_files/Final_input_file%d.json' %i, 'w') as f:
            json.dump([data,d_highlands],f, indent = 4)


    #all_input_files.append(json.dump([data,d_lowlands],f, indent = 4))

super_dict ={}
for i in range (0,3):
    
    with open('C:/Users/pietr/Spyder/RAMP_spyder/Initializing_json/Output_files/Final_input_file%d.json' %i , 'r') as f :
            Final_data = json.load(f)
            super_dict[i] = Final_data 
            
with open ('C:/Users/pietr/Spyder/RAMP_spyder/Initializing_json/Output_files/Mega_data_input.json','w') as f :
    json.dump(super_dict, f, indent = 4)
            
    
 