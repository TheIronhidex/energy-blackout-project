from dotenv import load_dotenv
import pandas as pd
import numpy as np
from pandas import json_normalize
from src.api_functions import *
from src.cleaning_functions import *
import requests
from bs4 import BeautifulSoup
import lxml.html as lh
from src.visual_functions import *
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from pylab import mpl

###--------------------------------------------API_adquisition--------------------------------------------------###
url_world = "https://world-population.p.rapidapi.com/worldpopulation"
world_pop = request_world_population(url_world)
format_json(world_pop) #Returns global population in .json

countries_name = []
url_countries = "https://world-population.p.rapidapi.com/allcountriesname"
test = request_country_names(url_countries)
dict_countries = format_json(test) #Returns a list of dicts of countries in .json
a = dict_countries.get('body')
list_countries = []
for i in a.values():
    list_countries.append(i) 
final_list = [item for sublist in list_countries for item in sublist] #Returns a list of countries

url_specific = "https://world-population.p.rapidapi.com/population"
database_api = request_all_countries_population(url_specific, final_list)
df1 = pd.DataFrame(database_api)
df1.rename(columns={"country_name": "country"}, inplace=True)

'''---------------------------------------------------------------------------------------------------------------'''
df1.to_csv('data/population-data.csv' , index = False)
'''---------------------------------------------------------------------------------------------------------------'''

###---------------------------------------Database_csv_managing--------------------------------------###

# df1 = dataframe from API
# df2 = dataframe from energy .csv
# df3 = dataframe from merging df1 and a modified version of df2
# df4 = dataframe derived from df3 containing only the year 2020
# df5 = dataframe derived from df4 without NaNs and with grouped columns by categories
# df6 = dataframe from avg-rate .csv (population)

csv0 = 'data/population-data.csv'
csv1 = 'data/energy-data/owid-energy-data.csv'
csv2 = 'data/avg-rate.csv'
df1 = load_csv(csv0)
df2 = load_csv(csv1)
df6 = load_csv(csv2)

list_1 = df1['country'] # df1 --> population
list_2 = df2['country'] # df2 --> energy
exclusion_list = np.setdiff1d(list_2,list_1)
df_ec = df2[df2['country'].isin(exclusion_list)] # Fork here, for correcting the prediction
df2_mod = df2[~df2['country'].isin(exclusion_list)]
df1.set_index('country', inplace=True)
df2_mod.set_index('country', inplace=True)
df3 = df1.merge(df2_mod, how='inner', on='country') # We combine both datasets through the common countries. The
# uncommon countries impact is estimated apart
df3.isna().sum()
df3.dropna(axis=1, how="all", inplace=True) # We don't use the function here because it must be applied to the columns
df3.drop(["iso_code","carbon_intensity_elec"], axis=1, inplace=True)

df6.drop(['LocID', 'VarID', 'Variant', 'Time', 'TFR',
       'NRR', 'CBR', 'Births', 'LEx', 'LExMale', 'LExFemale', 'IMR', 'Q5',
       'CDR', 'Deaths', 'DeathsMale', 'DeathsFemale', 'CNMR', 'NetMigrations',
          'NatIncr', 'SRB', 'MAC'], axis=1, inplace=True)

df6.set_index('MidPeriod',drop=True,inplace=True)
df6.rename(columns={"Location":"country"}, inplace=True)

csv3 = 'data/energy_ranged_with_pop'
df3 = load_csv(csv3)

list_1 = df3['country']
list_2 = df6['country']
exclusion_list = np.setdiff1d(list_2,list_1)
df6_mod = df6[~df6['country'].isin(exclusion_list)]
df3.set_index('country', inplace=True)
df6_mod.set_index('country', inplace=True)
df6_final = df3.merge(df6_mod, how='inner', on='country')

df7 = df6_final.groupby(['country'],as_index = True).mean() 
df7.dropna(axis=0, how='any') # We get the interannual variation rate of population (per country)

'''---------------------------------------------------------------------------------------------------------------'''
df7.to_csv('data/pop_avg_rate.csv' , index = True)
df3.to_csv('data/energy_ranged_with_pop',index = True)
'''---------------------------------------------------------------------------------------------------------------'''
url='https://www.antipodas.net/coordenadaspais/'
#Create a handle, page, to handle the contents of the website
page = requests.get(url)
#Store the contents of the website under doc
doc = lh.fromstring(page.content)
#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//tr')
#Check the length of the first 12 rows
[len(T) for T in tr_elements[:12]]
tr_elements = doc.xpath('//tr')
#Create empty list
col=[]
i=0
#For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    print('%d:"%s"'%(i,name))
    col.append((name,[]))
#Since out first row is the header, data is stored on the second row onwards
for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]
    
    #If row is not of size 3, the //tr data is not from our table 
    if len(T)!=3:
        break
    
    #i is the index of our column
    i=0
    
    #Iterate through each element of the row
    for t in T.iterchildren():
        data=t.text_content() 
        #Check if row is empty
        if i>0:
        #Convert any numerical value to integers
            try:
                data=int(data)
            except:
                pass
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1
[len(C) for (title,C) in col]
Dict={title:column for (title,column) in col}
coordinates=pd.DataFrame(Dict)
coordinates = coordinates.drop(['Nº de Habitantes'],axis=1)
coordinates = coordinates.rename(columns={'País':'country','Coordenadas Geográficas':'coordinates'})

csv3 = 'data/energy_ranged_with_pop'
df3 = load_csv(csv3)

list_1 = df3['country']
list_2 = coordinates['country']
exclusion_list = np.setdiff1d(list_2,list_1)
coordinates_mod = coordinates[~coordinates['country'].isin(exclusion_list)]
df3.set_index('country', inplace=True)
coordinates_mod.set_index('country', inplace=True)
dfinal = df3.merge(coordinates_mod, how='inner', on='country') # We combine both datasets through the common countries. The
# uncommon countries impact is estimated apart
dfinal_coords = dfinal['coordinates'].str.split(expand=True)

'''---------------------------------------------------------------------------------------------------------------'''
dfinal_coords.to_csv('output/dfinal_coords.csv' , index = True)
dfinal.to_csv('output/dfinal.csv' , index = True)
'''---------------------------------------------------------------------------------------------------------------'''

df3 = load_csv('data/energy_ranged_with_pop')
df4 = df3[df3['year']==2020]

table_hist_elec = df3.drop(['population_x', 'ranking', 'world_share', 'biofuel_share_elec', 'biofuel_elec_per_capita', 
       'coal_share_elec','coal_elec_per_capita','fossil_cons_per_capita','fossil_share_elec', 'gas_share_elec', 
       'gas_elec_per_capita', 'hydro_share_elec', 'hydro_elec_per_capita', 'low_carbon_share_elec',
       'low_carbon_elec_per_capita','nuclear_share_elec', 'nuclear_elec_per_capita', 'oil_share_elec',
       'oil_elec_per_capita', 'other_renewables_elec_per_capita','other_renewables_share_elec', 'per_capita_electricity',
       'renewables_elec_per_capita', 'renewables_share_elec','solar_share_elec', 'solar_elec_per_capita', 'wind_share_elec',
       'wind_elec_per_capita'], axis=1, inplace=False) # Includes the historical electricity production by source
table_2020_elec = df4.drop(['population_x', 'ranking', 'world_share', 'biofuel_share_elec', 'biofuel_elec_per_capita', 
       'coal_share_elec','coal_elec_per_capita','fossil_cons_per_capita','fossil_share_elec', 'gas_share_elec', 
       'gas_elec_per_capita', 'hydro_share_elec', 'hydro_elec_per_capita', 'low_carbon_share_elec',
       'low_carbon_elec_per_capita','nuclear_share_elec', 'nuclear_elec_per_capita', 'oil_share_elec',
       'oil_elec_per_capita', 'other_renewables_elec_per_capita','other_renewables_share_elec', 'per_capita_electricity',
       'renewables_elec_per_capita', 'renewables_share_elec','solar_share_elec', 'solar_elec_per_capita', 'wind_share_elec',
       'wind_elec_per_capita'], axis=1, inplace=False) # Includes the electricity production by source in 2020

table_hist_share = df3.drop(['population_x', 'ranking','biofuel_elec_per_capita', 'coal_elec_per_capita', 
        'electricity_generation', 'biofuel_electricity','coal_electricity', 'fossil_electricity', 'gas_electricity',
        'hydro_electricity', 'nuclear_electricity', 'oil_electricity','other_renewable_electricity',
        'other_renewable_exc_biofuel_electricity', 'renewables_electricity','solar_electricity', 'wind_electricity',
        'fossil_cons_per_capita','gas_elec_per_capita','hydro_elec_per_capita', 'low_carbon_electricity', 
        'low_carbon_elec_per_capita','nuclear_elec_per_capita', 'oil_elec_per_capita', 'other_renewables_elec_per_capita',
        'per_capita_electricity','renewables_elec_per_capita', 'solar_elec_per_capita', 'wind_elec_per_capita'],
                         axis=1, inplace=False) # Includes the historical % share of energy production
table_2020_share = df4.drop(['population_x', 'ranking','biofuel_elec_per_capita', 'coal_elec_per_capita', 
        'electricity_generation', 'biofuel_electricity','coal_electricity', 'fossil_electricity', 'gas_electricity',
        'hydro_electricity', 'nuclear_electricity', 'oil_electricity','other_renewable_electricity',
        'other_renewable_exc_biofuel_electricity', 'renewables_electricity','solar_electricity', 'wind_electricity',
        'fossil_cons_per_capita','gas_elec_per_capita','hydro_elec_per_capita', 'low_carbon_electricity', 
        'low_carbon_elec_per_capita','nuclear_elec_per_capita', 'oil_elec_per_capita', 'other_renewables_elec_per_capita',
        'per_capita_electricity','renewables_elec_per_capita', 'solar_elec_per_capita', 'wind_elec_per_capita'],
                         axis=1, inplace=False) # Includes the % share of energy production in 2020

table_hist_per_capita = df3.drop(['ranking', 'year','biofuel_share_elec', 'coal_share_elec',
       'electricity_generation', 'biofuel_electricity','coal_electricity', 'fossil_electricity', 'gas_electricity',
       'hydro_electricity', 'nuclear_electricity', 'oil_electricity','other_renewable_electricity',
       'other_renewable_exc_biofuel_electricity', 'renewables_electricity','solar_electricity', 'wind_electricity', 
       'fossil_share_elec', 'gas_share_elec','hydro_share_elec', 'low_carbon_share_elec','low_carbon_electricity',
       'nuclear_share_elec', 'oil_share_elec','other_renewables_share_elec','solar_share_elec', 'wind_share_elec'], 
                              axis=1, inplace=False) # Includes the historical electricity consumed per capita
table_2020_per_capita = df4.drop(['ranking', 'year','biofuel_share_elec', 'coal_share_elec',
       'electricity_generation', 'biofuel_electricity','coal_electricity', 'fossil_electricity', 'gas_electricity',
       'hydro_electricity', 'nuclear_electricity', 'oil_electricity','other_renewable_electricity',
       'other_renewable_exc_biofuel_electricity', 'renewables_electricity','solar_electricity', 'wind_electricity', 
       'fossil_share_elec', 'gas_share_elec','hydro_share_elec', 'low_carbon_share_elec','low_carbon_electricity',
       'nuclear_share_elec', 'oil_share_elec','other_renewables_share_elec','solar_share_elec', 'wind_share_elec'], 
                              axis=1, inplace=False) # Includes the electricity consumed per capita in 2020

'''---------------------------------------------------------------------------------------------------------------'''
table_hist_elec.to_csv('output/table-hist-elec.csv' , index = True)
table_2020_elec.to_csv('output/table-2020-elec.csv' , index = True)
table_hist_share.to_csv('output/table-hist-share.csv' , index = True)
table_2020_share.to_csv('output/table-2020-share.csv' , index = True)
table_hist_per_capita.to_csv('output/table-hist-capita.csv' , index = True)
table_2020_per_capita.to_csv('output/table-2020-capita.csv' , index = True)
'''---------------------------------------------------------------------------------------------------------------'''
###---------------------------------------Graphs-----------------------------------------------------------------###
