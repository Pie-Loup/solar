# Import python packages
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from sunposition import sunpos

def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta

def gaussian(x, mu, sigma):
   return (1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-0.1 * (((x) - mu) / sigma) ** 2))

mu = 0  # Mean
sigma = 1 # std dev

# Write directly to the app
st.title("Solar panel")
st.write(
    """Enter a GPS position and get the solar amount per day
    """
)

pos_lat = st.number_input(
    "Lat",
    min_value=-180.,
    max_value=180.,
    value=48.8566,
    help="Use this to set the latitude of the position",
)

pos_long = st.number_input(
    "Long",
    min_value=-180.,
    max_value=180.,
    value=2.3522,
    help="Use this to set the longitude of the position",
)

date_comp = st.date_input("date")
datetime_comp = datetime.combine(date_comp, datetime.min.time())


dts = [
        dt for dt in
        datetime_range(datetime_comp, datetime_comp + timedelta(days=5), 
        timedelta(minutes=10))
      ]
az,zen = sunpos(dts,pos_lat,pos_long,10)[0:2]


azen = {"az": az, "zen": zen}

data_plot = pd.DataFrame(
  azen
  , index=dts
  , columns=azen
)

data_plot["az"] = (180-abs(180-data_plot["az"]))/180
data_plot["zen"] = (180-data_plot["zen"])/180
data_plot["pu"] = data_plot["az"]*data_plot["zen"]

data_plot["time_in_day"] = data_plot.index.hour + data_plot.index.minute/60

data_plot['gaussian'] = 2*data_plot['time_in_day'].apply(lambda x: gaussian(x-6, 2*mu, sigma))

st.line_chart(data_plot[["pu", "gaussian"]])

st.dataframe(data_plot)

