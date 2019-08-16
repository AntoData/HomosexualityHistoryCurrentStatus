# coding: utf-8
'''
Created on 23 jul. 2019

@author: ingov
'''
"""
Data sources: https://76crimes.com/76-countries-where-homosexuality-is-illegal/
            https://en.wikipedia.org/wiki/LGBT_rights_by_country_or_territory
            https://en.wikipedia.org/wiki/LGBT_rights_in_+country
            
"""
from API import MapGenerator as mg
from Wrapper import DecriminalizationHomosexualityWrapper as dhw
import pandas as pd
import os
import folium
#In this case, we set the following colours
colours = {"Never":"#003399","Prison":" #ff0000","Life imprisonment":"#800000","Death penalty":"#660033",1750:"#003300", 1800:"#006600",1850:"#009900",1900:"#00cc00",1950:"#1aff1a",2000:"#66ff66",2050:"#b3ffb3"}
#We are talking our same sex marriage approval rate, countries where the approval rate is as low as
#between 0 and 25 should be painted red as it is a very low approval rate, orange for approval rates
#as low as between 25 and 50, yellow between 50 and 75, green for values between
#75 and 100 as this is a good indicator of lgtbi tolerance and dark green for 100 for
#coherence between colours
#we use getcmd to get the absolute route of our json file
geo_world = os.getcwd()+"\..\data\world-countries.json"
#We get our excel file to a dataframe object
df_ssm = pd.read_csv(os.getcwd()+"\..\data\DecriminalizationStatusHomosexuality.csv",sep="\t")
print(df_ssm)
#df_ssa = pd.read_excel(os.getcwd()+"\..\data\SSM.xlsx")
#We create a folium map object
ssa_world = folium.Map(titles='Mapbox Bright',start_zoom = 3)
#We turn our dataframe to a dictionary with the information we are interested in
#country and same sex marriage approval rate expressed in a scale from 0 to 100
map_ssm = df_ssm.set_index('Country')['Year'].to_dict()
print(map_ssm)
#We define the path were our html file will be saved
pathHTML = os.getcwd()+"\..\\homosexuality_world_history_and_status_worldwide.html"
#we define the caption for our legend in the map
vCap = "Year of Decriminalization Of Homosexuality"
vCap2 = "Illegal?"
#we use the function we defined previously to generate the map
vMap = mg.buildMap(ssa_world, geo_world,map_ssm, colours, vCap,vCap2,'name')
#We use the function putMarkers to put markers in the capital cities of countries where
#same-sex marriage is legal
vMap = mg.putGenericMarkers(vMap, df_ssm, dhw.getWikiInfo,'Lat', 'Lon', 'blue')
#We save the map to a map
ssa_world.save(pathHTML)