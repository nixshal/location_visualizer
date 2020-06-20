#warning: this code isn't clean at all

#locationhistory.py

import streamlit as st
import pandas as pd 
import numpy as np 
import pydeck as pdk #deckgl for python.
import plotly.express as px

#export MapboxAccessToken= pk.eyJ1Ijoibml4c2hhbCIsImEiOiJja2I1YXdvaW0xMjh6MnNtdmo4ajd1emh2In0.zCdwJaqAspr7-MmmlmU8Gg

#you will need your own .csv file with the first 4 columns titled:
#	  timestamp	  latitude	  longitude	  altitude


DATA_URL = ('locationhistory_UK.csv')

st.title('Nixshal\'s GPS data')
st.markdown('###### 16th December 2015 - 3 June 2020')
#16th December 2015 - 3 June 2020


#Load data function
@st.cache(persist=True) #decorate function, only rerun computation when code or inputs chnaged
def load_data(nrows):
	data = pd.read_csv(DATA_URL, nrows = nrows, parse_dates = ['timestamp'])
	#data.dropna(subset = ['LATITUDE', 'LONGITUDE'], inplace = True)
	lowercase = lambda x:str(x).lower()
	data.rename(lowercase, axis='columns', inplace = True)
	data.rename(columns={'lat_long' : 'date/time'}, inplace=True)
	return data

#Loading the data
data = load_data(41000)
original_data = data #keeping the original data in this variable if we need it

#Showing map of GPS locations
st.subheader('GPS Locations')

###THIS ONE WORKS###
#following example https://deckgl.readthedocs.io/en/stable/layer.html
#helps in understanding how to make the charts
st.write(pdk.Deck(
     #map_style='mapbox://styles/mapbox/dark-v9', #list of mapbox styles
     	 initial_view_state=pdk.ViewState(
         latitude=50.937341,     #USJ 16 lat, long = 3.030977, 101.576331
         longitude=-1.377285,  #Wessex Lane lat, long = 50.937341, -1.377285
         zoom=12,
         pitch=60, 
         #bearing = 40, #not sure what this does
         #min_zoom = 5
         #max_zoom = 40
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=data.drop(['timestamp','altitude'], axis =1), #original data has those two columns, remove them
            get_position='[longitude, latitude]',
            radius=20,
            elevation_scale=25,
            elevation_range=[0,5000],
            pickable=True,
            extruded=True,
            #to change colors https://github.com/visgl/deck.gl/blob/master/docs/layers/hexagon-layer.md
            #colorRange = [[241,238,246],[212,185,218],[201,148,199],[223,101,176],[221,28,119],[152,0,67]], #change color schemes with colorbrewer https://colorbrewer2.org/#type=sequential&scheme=YlOrRd&n=6
            colorRange = [[255, 0, 0],[255, 0, 0],[255, 0, 0],[255, 0, 0],[255, 0, 0],[255, 0, 0]],
         ),
         pdk.Layer(
             'ScatterplotLayer', #can use with HeatmapLayer or ScatterplotLayer
             data=data.drop(['timestamp','altitude'], axis =1),
             get_position='[longitude, latitude]',
             get_color=[0,255,0], #purple= get_color=[180, 0, 200, 40]
             opacity = 1,
             get_radius=25,
             pickable = True,
             #for HeatmapLayer
             intensity = 1,
         ),
     ],
 ))
###THIS ONE WORKS###




#Showing the raw data
st.subheader('Raw Data')
st.write(data)












# print(df.head())
# print(df.shape)
# print(data.drop(['timestamp','altitude'], axis =1).head())
# print(data.shape)

r = pdk.Deck(
     map_style='mapbox://styles/mapbox/dark-v9', #list of mapbox styles
     	 initial_view_state=pdk.ViewState(
         latitude=50.937341,     #USJ 16 lat, long = 3.030977, 101.576331
         longitude=-1.377285,  #Wessex Lane lat, long = 50.937341, -1.377285
         zoom=20,
         pitch=70, 
         #bearing = 40, #not sure what this does
         #min_zoom = 5
         #max_zoom = 40
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=data.drop(['timestamp','altitude'], axis =1), #original data has those two columns, remove them
            get_position='[longitude, latitude]',
            radius=100,
            elevation_scale=100,
            elevation_range=[0,1000],
            pickable=True,
            extruded=True,
            #to change colors https://github.com/visgl/deck.gl/blob/master/docs/layers/hexagon-layer.md
            #colorRange = [[241,238,246],[212,185,218],[201,148,199],[223,101,176],[221,28,119],[152,0,67]], #change color schemes with colorbrewer https://colorbrewer2.org/#type=sequential&scheme=YlOrRd&n=6
         ),
         pdk.Layer(
             'ScatterplotLayer',
             data=data.drop(['timestamp','altitude'], axis =1),
             get_position='[longitude, latitude]',
             get_color=[180, 0, 200, 40],
             opacity = 1,
             get_radius=300,
             pickable = True,
         ),
     ],
 )

#r.to_html('viewNixshalGPSdata.html')
#CAN EXPORT TO WEBSITE? mapbox api?