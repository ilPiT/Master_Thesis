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
for j in range(2,3):
    Profiles_list = Stochastic_Process(j)
    
# Post-processes the results and generates plots
    Profiles_avg, Profiles_list_kW, Profiles_series = Profile_formatting(Profiles_list)
    Profile_series_plot(Profiles_series) #by default, profiles are plotted as a series
    export_series(Profiles_series,j)

    if len(Profiles_list) > 1: #if more than one daily profile is generated, also cloud plots are shown
        Profile_cloud_plot(Profiles_list, Profiles_avg)

        Profiles_avg_test = pd.DataFrame(Profiles_avg)
        Profiles_avg_test.to_excel(r'C:\Users\pietr\PycharmProjects\Thesis_RAMP\VLIR_Energy_Demand-main\Statistical_analysis\Avg_Profiles/Profiles_avg_%d.xlsx' % j) # In questo modo sono riuscito ad estrapolare il profilo medio di una giornata tipo
### What if we try to do all the analysis inside this cyle without the need of writing every thing two times?

#%%Analisi su i profili medi per estrapolare informazioni fondamentali tipo max min etc

df1 = pd.read_excel(r'C:\Users\pietr\PycharmProjects\Thesis_RAMP\VLIR_Energy_Demand-main\Statistical_analysis\Avg_Profiles/Profiles_avg_1.xlsx')
df2 = pd.read_excel(r'C:\Users\pietr\PycharmProjects\Thesis_RAMP\VLIR_Energy_Demand-main\Statistical_analysis\Avg_Profiles/Profiles_avg_2.xlsx')
df3 = pd.read_excel(r'C:\Users\pietr\PycharmProjects\Thesis_RAMP\VLIR_Energy_Demand-main\Statistical_analysis\Avg_Profiles/Profiles_avg_3.xlsx')

#Energy_Demand = pd.read_excel('Example/Demand.xls',index_col=0,Header=None) # open the energy demand file

#print(df1.head())
#print(df2.head())
a1 = df1.sum(axis=0)
a2 = df2.sum(axis=0)
a3 = df3.sum(axis=0)
#a1.to_excel(r'C:\Users\pietr\PycharmProjects\Thesis_RAMP\VLIR_Energy_Demand-main\Statistical_analysis/a1.xlsx')
#a2.to_excel(r'C:\Users\pietr\PycharmProjects\Thesis_RAMP\VLIR_Energy_Demand-main\Statistical_analysis/a2.xlsx')

#print(type(a1))

### PERCENTAGE
Percentage_Community_needs = (a2/a1)
Percentage_IGA_needs = (a3/a1)

# concat--> not really good it should work also with a for cycle especially if you want to sue the multi-year version with multiple input files
df = pd.DataFrame()
#df = pd.DataFrame(columns=list('AB'),index=['jonny','jonny1']) #  in this way I am just creating two empty rows and columns and then the append
asd_1 = df.append(a1, ignore_index=True)
asd_2 = asd_1.append(a2, ignore_index=True)
asd_3 = asd_2.append(a3, ignore_index=True)
asd_Percentage_Community = asd_3.append(Percentage_Community_needs, ignore_index=True)
asd_Percentage_Community_IGA = asd_Percentage_Community.append(Percentage_IGA_needs, ignore_index=True)
###asdasdasd = asdasd.append(df1.describe(),ignore_index=True)#todo non riesco a mantenere gli indici --> non si capisce nulla

sum_percentage_sum = pd.DataFrame(asd_Percentage_Community_IGA)  # dovrebbe avere 5 righe non tre
#sum_percentage_new.rename(index={'jonny':'1'}) # niente non riesco a farlo

sum_percentage_sum.to_excel(r'C:\Users\pietr\PycharmProjects\Thesis_RAMP\VLIR_Energy_Demand-main\Statistical_analysis\Avg_Profiles/sum_and_percentages.xlsx')

###stat = pd.DataFrame([(df1.describe()), df2.describe()])  #todo try to understand-->ValueError: Must pass 2-d input. shape=(2, 8, 2)


### Statistical important data for the avererage profiles

Profiles_avg1_stat = df1.describe()
Profiles_avg2_stat = df2.describe()
Profiles_avg3_stat = df3.describe()
#concat
Stat = pd.DataFrame()
Prova = Stat.append(Profiles_avg1_stat)
prova = Prova.append(Profiles_avg2_stat)
prova1 = prova.append(Profiles_avg3_stat)
Stat_avg_fund = pd.DataFrame(prova1)
prova1.columns = ['useless', 'values'] #todo try to rename also the rows
prova1.to_excel(r'C:\Users\pietr\PycharmProjects\Thesis_RAMP\VLIR_Energy_Demand-main\Statistical_analysis\Avg_Profiles/Describe_concat_fundamental_stat_avg.xlsx')  ### Ricorda che il primo si riferisce a Profilo 1 poi sotto hai il Profilo 2

#%% Statistical important data for the output results
import pandas as pd

data1 = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/results/output_file_1.csv',index_col=0)
data2 = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/results/output_file_2.csv', index_col=0)
data3 = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/results/output_file_3.csv', index_col=0)

#%% Transforming the temporal resolution

#FIRST METHOD 

df =  pd.DataFrame(data2)
test = df.iloc[0:,0]

s = 0
z = 0 
mean_minuts_to_hours =[]

for i in test :
    z = z+1 # counting the indexes   
    if z % 60 == 0 :
        test = df.iloc[s:z,0]
        a = (test.values.sum(axis=0))/z
        s = z 
        mean_minuts_to_hours.append(a)

#mean_minuts_to_hours.to_excel(r'C:\Users\pietr\PycharmProjects\Thesis_RAMP\VLIR_Energy_Demand-main\Statistical_analysis\Results_output_profiles/Demand_adjusted .xlsx')
     

#%% Second method
data2 = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/results/output_file_2.csv', index_col=0)
index = pd.date_range(start=0,periods = len(data2), 
                                   freq=('1min'))

data2.index = index

data2['hours']= data2.index.hour
data2['days']= data2.index.dayofyear


data_hourly = data2.groupby([data2.index.hour]).mean() 

    

#%%
data1_sum = data1.sum(axis=0) 
data2_sum = data2.sum(axis=0)
data3_sum = data3.sum(axis=0)
print(data1_sum)

data_percentage_community = (data2_sum/data1_sum)

print(data_percentage_community)
data_percentage_IGA = (data3_sum/data1_sum)  # not really interesting because the percentages exceed 100% due to the different run in the same conditions


data_percentage = pd.DataFrame()
data_percentage_Community = data_percentage.append((data_percentage_community),ignore_index=True)  # not really interesting because the percentages exceed 100% due to the different run in the same conditions

data_percentage_Community_IGA = data_percentage_Community.append((data_percentage_IGA), ignore_index=True)

data_percentage_Community_IGA.to_excel(r'C:\Users\pietr\PycharmProjects\Thesis_RAMP\VLIR_Energy_Demand-main\Statistical_analysis\Results_output_profiles/Data_percentage_Community_IGA.xlsx')

desc1 = data1.describe()
desc2 = data2.describe()
desc3 = data3.describe()

### I could also concatenate this one

assessment_desc1 = pd.DataFrame(desc1)
assessment_desc2 = pd.DataFrame(desc2)
assessment_desc3 = pd.DataFrame(desc2)

assessment_desc1.to_excel(r'C:\Users\pietr\PycharmProjects\Thesis_RAMP\VLIR_Energy_Demand-main\Statistical_analysis\Results_output_profiles/Statistical_data_desc1.xlsx')
assessment_desc2.to_excel(r'C:\Users\pietr\PycharmProjects\Thesis_RAMP\VLIR_Energy_Demand-main\Statistical_analysis\Results_output_profiles/Statistical_data_desc2.xlsx')
assessment_desc3.to_excel(r'C:\Users\pietr\PycharmProjects\Thesis_RAMP\VLIR_Energy_Demand-main\Statistical_analysis\Results_output_profiles/Statistical_data_desc3.xlsx')


# next --> try to save the images in a folder and try to stop the appereance of images after every computation --> annoying


#todo for the moment when i try to run the program with 300HH it does not work saying something about max error etc --> really weird
# remember that i could also just run the program with the input file 1 becuase potentially the other profiles are not changing in this simulations --> any way in this case I would have to do the analysis with excel values