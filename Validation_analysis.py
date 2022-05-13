# -*- coding: utf-8 -*-
"""
Created on Fri May 13 11:38:36 2022

@author: pietr
"""

import pandas as pd

#%% First analysis for the Chuquisaca department 

# import the data from the real data base

chuquisaca_real_data_base = pd.read_csv('C:/Users/pietr/Spyder/RAMP_spyder/All_data_base_claudia/chuquisaca_sd.csv')

column_list_chuquisaca = chuquisaca_real_data_base.columns.values.tolist()


# Filtering process

# TODO : an initial filtering process that has to be done regards the connection with the main grid --> but still i need to check the document that Claudia told me in order to understand with system code can be associated to a connection to the grid and which not --> remember that the most reliable data comes from the grid

# 1 : Filtering for the residential sector
chuquisaca_data_base_residential = chuquisaca_real_data_base.loc[chuquisaca_real_data_base['CATEGORY'] == 1]

# 2 : Filtering for one month --> then it will be possible to use a for cycle to extend the analysis all year long 

chuquisaca_data_base_residential_gen = chuquisaca_data_base_residential.loc[chuquisaca_data_base_residential['MONTH']==1]

# 3 : Filtering for the municipalties that has been selected following some fundamental criteria and parameters --> example for one municipality but then it can be extended with a for cycle for all the municiplaities that have been selected

chuquisaca_data_base_residential_gen_munipality = chuquisaca_data_base_residential_gen.loc[chuquisaca_data_base_residential_gen['COD_MUNI']==11002] # Huacaya

# 4 : Filtering for a specific year --> 2012 


chuquisaca_data_base_residential_gen_munipality_2012 = chuquisaca_data_base_residential_gen_munipality.loc[chuquisaca_data_base_residential_gen_munipality['YEAR']==2012]
chuquisaca_data_base_residential_gen_munipality_2016 = chuquisaca_data_base_residential_gen_munipality.loc[chuquisaca_data_base_residential_gen_munipality['YEAR']==2016]
