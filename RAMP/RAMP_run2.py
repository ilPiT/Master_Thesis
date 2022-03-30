# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 14:35:00 2019
This is the code for the open-source stochastic model for the generation of 
multi-energy load profiles in off-grid areas, called RAMP, v.0.2.1-pre.

@authors:
- Francesco Lombardi, Politecnico di Milano
- Sergio Balderrama, Université de Liège
- Sylvain Quoilin, KU Leuven
- Emanuela Colombo, Politecnico di Milano

Copyright 2019 RAMP, contributors listed above.
Licensed under the European Union Public Licence (EUPL), Version 1.1;
you may not use this file except in compliance with the License.

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations
under the License.
"""

#%% Import required modules
import glob
import os

import pandas as pd  #todo sometimes it gives this error : Unused import statement ' import pandas as pd

from stochastic_process import Stochastic_Process
from post_process import*

# Calls the stochastic process and saves the result in a list of stochastic profiles
# In this default example, the model runs for 2 input files ("input_file_1", "input_file_2"),
# but single or multiple files can be run restricting or enlarging the iteration range 
# and naming further input files with progressive numbering
for j in range(1,2):
    Profiles_list = Stochastic_Process(j)
    
# Post-processes the results and generates plots
    Profiles_avg, Profiles_list_kW, Profiles_series = Profile_formatting(Profiles_list)
    Profile_series_plot(Profiles_series) #by default, profiles are plotted as a series
    export_series(Profiles_series,j)

    if len(Profiles_list) > 1: #if more than one daily profile is generated, also cloud plots are shown
        Profile_cloud_plot(Profiles_list, Profiles_avg)

        Profiles_avg_test = pd.DataFrame(Profiles_avg)
        Profiles_avg_test.to_csv('../Statistical_analysis/Avg_Profiles/Profiles_avg_%d.csv' % j) # In questo modo sono riuscito ad estrapolare il profilo medio di una giornata tipo
### What if we try to do all the analysis inside this cyle without the need of writing every thing two times?

#%%Analisi su i profili medi per estrapolare informazioni fondamentali tipo max min etc




#%% Trying to do datascience in a smarter way
'''
import glob
import pandas as pd

# get data file names
path =r'C:/Users/pietr/Spyder/RAMP_spyder/Statistical_analysis/Avg_Profiles'

filenames = glob.glob(path + "/*.csv")



dfs = []

for filename in filenames:
    dfs.append(pd.read_csv(filename,index_col=0))

# Concatenate all data into one DataFrame
big_frame = pd.concat(dfs, ignore_index=True,axis=1)


df_sum = big_frame.sum()
df_desc = big_frame.describe()

df = pd.DataFrame()

df = pd.concat([df,big_frame,df_sum,df_desc],axis =1, ignore_index= True) # me li concatena in fondo non proprio ottimale
asd = ['total', 'community' ,'iga','sums','desc1','desc2','desc3']
df.columns = asd 

# Percentages?? Really needed or it just a matter of graphs?
'''


#%% Analisi su i profili medi per estrapolare informazioni fondamentali tipo max min etc

'''
import pandas as pd

## 5 inputs for every run , is it necessary to separete the different contribution coming form the IGA?

df1 = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/Statistical_analysis/Avg_Profiles/Profiles_avg_1.csv') #Total
df2 = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/Statistical_analysis/Avg_Profiles/Profiles_avg_2.csv') # Residential
df3 = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/Statistical_analysis/Avg_Profiles/Profiles_avg_3.csv') # Community_serv
df3 = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/Statistical_analysis/Avg_Profiles/Profiles_avg_3.csv') # IGA_Non
df3 = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/Statistical_analysis/Avg_Profiles/Profiles_avg_3.csv') # IGA_agric

#Energy_Demand = pd.read_excel('Example/Demand.xls',index_col=0,Header=None) # open the energy demand file
Profiles_avg1_stat = df1.describe()
Profiles_avg1_stat.columns = ['0','Total']
Profiles_avg1_stat= Profiles_avg1_stat.drop(columns=('0'))
#Profiles_avg1_stat = Profiles_avg1_stat.drop(columns=['Unnamed:0']) Non funziona
Profiles_avg2_stat = df2.describe()
Profiles_avg2_stat.columns = ['0','Community_serv']
Profiles_avg2_stat= Profiles_avg2_stat.drop(columns=('0'))
Profiles_avg3_stat = df3.describe()
Profiles_avg3_stat.columns = ['0','IGA']
Profiles_avg3_stat= Profiles_avg3_stat.drop(columns=('0'))

Describe_avg = pd.DataFrame()
Describe_avg = pd.concat([Describe_avg,Profiles_avg1_stat,Profiles_avg2_stat,Profiles_avg3_stat],axis=1)


a1 = df1.sum(axis=0)
#a1 = a1.drop([0,0])
a2 = df2.sum(axis=0)
a3 = df3.sum(axis=0)
sums = pd.DataFrame()
sums = pd.concat([sums,a1,a2,a3],axis =1)
sums.to_excel('sum.xlsx')
sums = pd.read_excel('sum.xlsx',header=0,index_col=0)
#a1.to_excel(r'C:\Users\pietr\PycharmProjects\Thesis_RAMP\VLIR_Energy_Demand-main\Statistical_analysis/a1.xlsx')
#a2.to_excel(r'C:\Users\pietr\PycharmProjects\Thesis_RAMP\VLIR_Energy_Demand-main\Statistical_analysis/a2.xlsx')

#print(type(a1))

### PERCENTAGE
Percentage_Community_needs = (a2/a1)
Percentage_IGA_needs = (a3/a1)


# concat--> not really good it should work also with a for cycle especially if you want to sue the multi-year version with multiple input files
df = pd.DataFrame()
df = pd.concat([df,sums,Describe_avg,Percentage_Community_needs,Percentage_IGA_needs], axis=1)

df.to_excel('../Statistical_analysis/Avg_Profiles/Data_science_avg.xlsx')

'''

'''
df.columns = ['2','AA']
asd = ['A','B', 'C']
df_new = pd.DataFrame(columns= asd,index=['jonny','jonny1'])
 #  in this way I am just creating two empty rows and columns and then the append
'''


#%% Statistical important data for the output results

'''

#%% Trying a cycle for to simplfy the code
import glob
import pandas as pd


path =r'C:/Users/pietr/Spyder/RAMP_spyder/results'
filenames = glob.glob(path + "/*.csv")
data = pd.DataFrame()

for j in range(1,4):
    data =pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/results/output_file_%d.csv' %j,index_col=0, 'Sheet%d' %j)

'''
#%%
'''
data1 = pd.read_csv('../results/output_file_1.csv',index_col=0)
data2 = pd.read_csv('../results/output_file_2.csv', index_col=0)
data3 = pd.read_csv('../results/output_file_3.csv', index_col=0)
'''
      

#%%  Creating the Demand file for 20 years
'''
import pandas as pd

data30 = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/results/output_file_1.csv', index_col=0)
data31 = pd.DataFrame(data30)
data31 = data31.append(data30[0:1440])
index30 = pd.date_range(start='2016-01-01 00:00:00',periods = len(data30), 
                                   freq=('1min'))
index31 = pd.date_range(start='2016-01-01 00:00:00',periods = len(data31), 
                                   freq=('1min'))




data30.index30 = index30
data31.index31 = index31

data30['day']  = data30.index30.dayofyear
data31['day']  = data31.index31.dayofyear
data30['hour'] = data30.index30.hour
data31['hour'] = data31.index31.hour
Demand_adjusted30 = data30.groupby(['day', 'hour']).mean()
Demand_adjusted31 = data31.groupby(['day', 'hour']).mean()

Demand_30 = pd.DataFrame()
Demand_31 = pd.DataFrame()

for i in range(1,7+1):

    Demand_30 = pd.concat([Demand_adjusted30,Demand_30], axis=0)
    
for i in range(1,5+1):
    Demand_31 = pd.concat([Demand_adjusted31,Demand_31], axis=0)


Demand = pd.DataFrame()
Demand = pd.concat([Demand_31, Demand_30], axis=0) # This is the demand of one year constructed before with 8760 values


Demand_20years =pd.DataFrame()


for i in range(1,20+1):
    Demand_20years =pd.concat([Demand_20years, Demand],axis=1)

index = list(range(1,8760+1))
Demand_20years.index = index

years = list(range(1,20+1))
Demand_20years.columns = years
print(type(years))

Demand_20years.to_excel('C:/Users/pietr/Spyder/RAMP_spyder/results/Demand_20years.xlsx')

#Demand_final = pd.read_excel('C:/Users/pietr/Spyder/RAMP_spyder/results/Demand_20years.xlsx',index_col=0)

'''

#%% PRATICAMENTE INUTILE POSSO FARE MEGLIO COME HO FATTO PER L'AVG
''''
data1_sum = data1.sum(axis=0) 
data2_sum = data2.sum(axis=0)
data3_sum = data3.sum(axis=0)


data_percentage_community = (data2_sum/data1_sum)

data_percentage_IGA = (data3_sum/data1_sum)  # not really interesting because the percentages exceed 100% due to the different run in the same conditions


data_percentage = pd.DataFrame()
data_percentage_Community = data_percentage.append((data_percentage_community),ignore_index=True)  # not really interesting because the percentages exceed 100% due to the different run in the same conditions

data_percentage_Community_IGA = data_percentage_Community.append((data_percentage_IGA), ignore_index=True)

data_percentage_Community_IGA.to_excel('../Statistical_analysis/Results_output_profiles/Data_percentage_Community_IGA.xlsx')

desc1 = data30.describe()
desc2 = data2.describe()
desc3 = data3.describe()

### I could also concatenate this one

assessment_desc1 = pd.DataFrame(desc1)
assessment_desc2 = pd.DataFrame(desc2)
assessment_desc3 = pd.DataFrame(desc3)

assessment_desc1.to_excel('../Statistical_analysis/Results_output_profiles/Statistical_data_desc1.xlsx')
assessment_desc2.to_excel('../Statistical_analysis/Results_output_profiles/Statistical_data_desc2.xlsx')
assessment_desc3.to_excel('../Statistical_analysis/Results_output_profiles/Statistical_data_desc3.xlsx')

'''

# next --> try to save the images in a folder and try to stop the appereance of images after every computation --> annoying
