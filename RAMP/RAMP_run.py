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

# added by me
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import pandas as pd  #todo sometimes it gives this error : Unused import statement ' import pandas as pd

from stochastic_process import Stochastic_Process
from post_process import*
from PIL import Image

# Calls the stochastic process and saves the result in a list of stochastic profiles
# In this default example, the model runs for 2 input files ("input_file_1", "input_file_2"),
# but single or multiple files can be run restricting or enlarging the iteration range 
# and naming further input files with progressive numbering
for j in range(1,3):
    Profiles_list = Stochastic_Process(j)
    
# Post-processes the results and generates plots
    Profiles_avg, Profiles_list_kW, Profiles_series = Profile_formatting(Profiles_list)
    Profile_series_plot(Profiles_series) #by default, profiles are plotted as a series
    export_series(Profiles_series,j)

    if len(Profiles_list) > 1: #if more than one daily profile is generated, also cloud plots are shown
        Profile_cloud_plot(Profiles_list, Profiles_avg)
        

        Profiles_avg_test = pd.DataFrame(Profiles_avg)
        Profiles_avg_test.to_csv('../Statistical_analysis/Avg_Profiles/Profiles_avg_%d.csv' % j)
        
        img = Image.open('profiles_avg.png')
        img = img.save('C:/Users/pietr/Spyder/RAMP_spyder/Statistical_analysis/Avg_Profiles/Profile_avg_%d.png' % j)
        #plt.imshow()
        #img=mpimg.imread('profiles_avg.png')
        #plt.imshow(img)
        #plt.savefig('../Statistical_analysis/Avg_Profiles/profiles_avg%d.png' % j)
        
        # In questo modo sono riuscito ad estrapolare il profilo medio di una giornata tipo
### What if we try to do all the analysis inside this cyle without the need of writing every thing two times?


#%% Da tener conto che tutte queste analisi posso anche essere fatte a posteriori visto che utlizzano i dati di output di RAMP

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
asd= ['Total','Residential','Community','IGA']
big_frame.columns = asd
big_frame.to_excel('../Statistical_analysis/Avg_Profiles/Avg_profiles_concat.xlsx')


df_sum = big_frame.sum()
df_desc = big_frame.describe()

df = pd.DataFrame()

df_desc = pd.concat([df_desc,df_sum],axis =1, ignore_index= True) 
asd_desc= ['Total','Residential','Community','IGA','Sums']
df_desc.columns = asd_desc

df_desc.to_excel('../Statistical_analysis/Avg_Profiles/desc_avg_concat.xlsx')


# quante colonne? 4 input quindi 4 avg profiles + colonna delle somme + 4 colonne di desc

#%% trying to save the different plots but the quality is a shit do not understand why
'''



'''

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img=mpimg.imread('profiles_avg.png')
plt.imshow(img)
plt.savefig('../Statistical_analysis/Avg_Profiles/profiles_avg%d.png' % j)

'''