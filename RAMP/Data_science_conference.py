# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 16:30:25 2022

@author: pietr
"""
#%%
import os
import glob
import pandas as pd

#%% possible improvements --> trying to make different excels sheet insted of multiple different excel files 
                             #trying to make it more usefull involving a loop also for each community population --> mybe ask Sergio or Claudia if they have any idea
                             

### AVG analysis   
for i in range(1,5):
    path =r'C:/Users/pietr/Spyder/RAMP_spyder/Output_conference/1500pop/%d/Statistical_analysis/Avg_Profiles' %i
    filenames = glob.glob(path + "/*.csv")
    dfs = []

    for filename in filenames:
        dfs.append(pd.read_csv(filename,index_col=0))
    
# dfs è una lista di dataframes

# Concatenate all data into one DataFrame
    big_frame = pd.concat(dfs, ignore_index=True,axis=1)
    asd = ['Total','Residential','Community','IGA']
    big_frame.columns = asd

#SALVARE IN APPOSITE CARTELLE non proprio necessario big_frame.to_excel('../Statistical_analysis/Avg_Profiles/Avg_profiles_concat.xlsx')

# it is fundamental to check is the Residential sector will cause some problem due to the different size of the DataFrame
    df_sum = big_frame.sum()

# Percentage contribution fo the energy sector BUT relative to the avg profiles


    Community_contrib = df_sum['Community']/df_sum['Total']
    Incomegen_contrib = df_sum['IGA']/df_sum['Total']
    Residential_contrib = 1- Community_contrib - Incomegen_contrib
    energy_sector_contribution = [Residential_contrib, Community_contrib, Incomegen_contrib]
    energy_sector = pd.DataFrame(energy_sector_contribution)
    asdd= ['Residential','Community','IGA']
    energy_sector.index = asdd
    df_desc = big_frame.describe()

    df = pd.DataFrame()

    df_desc = pd.concat([df_desc,df_sum,energy_sector],axis =1, ignore_index= True) 
    asd_desc= ['Total','Residential','Community','IGA','Sums','% energy sector']
    df_desc.columns = asd_desc

    df_desc.to_excel('C:/Users/pietr/Spyder/RAMP_spyder/Data_science_outputs/1500pop/avg_analysis/avg_analysis_%d.xlsx' %i )


# quante colonne? 4 input quindi 4 avg profiles + colonna delle somme + 4 colonne di desc


#%% Data science on the output_file series

for i in range(1,5):
    path = r'C:/Users/pietr/Spyder/RAMP_spyder/Output_conference/1500pop/%d/results' %i
    filenames = glob.glob(path + "/*.csv")

    dfs = []

    for filename in filenames:
        dfs.append(pd.read_csv(filename,index_col=0))
    
# dfs è una lista di dataframes

# Concatenate all data into one DataFrame
    big_frame = pd.concat(dfs, ignore_index=True,axis=1)
    asd= ['Total','Residential','Community','IGA']
    big_frame.columns = asd

#SALVARE IN APPOSITE CARTELLE non proprio necessario big_frame.to_excel('../Statistical_analysis/Avg_Profiles/Avg_profiles_concat.xlsx')

# it is fundamental to check is the Residential sector will cause some problem due to the different size of the DataFrame
    df_sum = big_frame.sum()

# Percentage contribution fo the energy sector BUT relative to the avg profiles


    Community_contrib = df_sum['Community']/df_sum['Total']
    Incomegen_contrib = df_sum['IGA']/df_sum['Total']
    Residential_contrib = 1- Community_contrib - Incomegen_contrib
    energy_sector_contribution = [Residential_contrib, Community_contrib, Incomegen_contrib]
    energy_sector = pd.DataFrame(energy_sector_contribution)
    asdd= ['Residential','Community','IGA']
    energy_sector.index = asdd
    df_desc = big_frame.describe()

    df = pd.DataFrame()

    df_desc = pd.concat([df_desc,df_sum,energy_sector],axis =1, ignore_index= True) 
    asd_desc= ['Total','Residential','Community','IGA','Sums','% energy sector']
    df_desc.columns = asd_desc
    df_desc.to_excel('C:/Users/pietr/Spyder/RAMP_spyder/Data_science_outputs/1500pop/output_results/output_analysis_%d.xlsx' %i )



#%% Consumption per monthy --> unit of measure Kwh per month
## Plus Electricity per hour per a whole year transfiormation

#looping over the different scenarios of development of the same community (fixed number of household)

for i in range(1,5):
    path = r'C:/Users/pietr/Spyder/RAMP_spyder/Output_conference/1500pop/%d/results' %i
    filenames = glob.glob(path + "/*.csv")

    dfs = []

    for filename in filenames:
        dfs.append(pd.read_csv(filename,index_col=0))
    
# dfs è una lista di dataframes

# Concatenate all data into one DataFrame
    big_frame = pd.concat(dfs, ignore_index=True,axis=1)
    asd= ['Total','Residential','Community','IGA']
    big_frame.columns = asd
    

    index = pd.date_range(start='2016-01-01 00:00:00',periods = len(big_frame), 
                                   freq=('1min'))





    big_frame.index = index

    big_frame['day']  = big_frame.index.dayofyear
    big_frame['hour'] = big_frame.index.hour
    big_frame['month'] = big_frame.index.month
    
    
    Demand_adjusted = big_frame.groupby(['month']).sum()
                              

    
    Montly_consumption_all = pd.DataFrame(Demand_adjusted[:] /(60*1000)) # trasformation to Kwh
    Montly_consumption_all.to_excel('C:/Users/pietr/Spyder/RAMP_spyder/Data_science_outputs/1500pop/Monthly_consumption/Montlhy_consumption_%d.xlsx' %i)
    
    ## Electricity per hour per a whole year transfiormation
    
    Electricity_per_hour_whole_year = big_frame.groupby(['day', 'hour']).mean()
    Electricity_per_hour_whole_year.to_excel('C:/Users/pietr/Spyder/RAMP_spyder/Data_science_outputs/1500pop/Electricity_per_hour_whole_year/Electricity_per_hour_whole_year_%d.xlsx' %i)



#%% Libraries necessary to plot the FIRST GRAPH
### NOT WORKING

#### First Graph --> fixed poverty level --> 56% but variable population
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
import os 

# thus i need all the output data from the Scearios 4 for every folder of the population
path = r'C:/Users/pietr/Spyder/RAMP_spyder/Data_science_outputs/Graphs/First'
filenames = glob.glob(path + "/*.xlsx")
#test = pd.read_excel('C:/Users/pietr/Spyder/RAMP_spyder/Data_science_outputs/Graphs/First/Electricity_per_hour_whole_year_200pop_4.xlsx',index_col=0)
#Total = test['Total']

dfs = []

for filename in filenames:
    
    
    test = pd.read_excel(filename,index_col=0)
    Total = test['Total']        
    dfs.append(Total)
               
    
# dfs è una lista di dataframes

# Concatenate all data into one DataFrame
big_frame = pd.concat(dfs, ignore_index=True,axis=1)


total_energy_consumption = big_frame.sum()/1000 #MWh
total_power = big_frame.sum(axis= 0)/8760 # MW

# Verifica somma delle colonne OK   
sum_column = big_frame[1].sum()/1000



v = pd.DataFrame(total_energy_consumption)  ## the axis for the total energy consumption graph
vv = pd.DataFrame(total_power) ## the axis for the total_power graph

### transfor the dataframe into a list so that is possible to be plotted
 
y = v.values.tolist()
z = vv.values.tolist()

# Plotting the graph finally


x = [200,500,800,1000,1500]


plt.xlabel('HouseHolds')
plt.ylabel('MWh/year')

#setting the axis range

plt.ylim([1,100])
plt.xlim([1,600]) 

plt.plot(x, y, color='green', linestyle='dashed', linewidth = 0.5,
         marker='.', markerfacecolor='green', markersize=5)

plt.show()

### you should add another graph that is the one with the power consumption in funcion of the total number of households
