import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')


# Caching the Data
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data['date/time'] = pd.to_datetime(data['date/time'])
    return data

def print_raw_data(data):
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

def plot_pickups_by_hour(data):
    st.subheader('Number of pickups by hour')
    hist_values = np.histogram(data['date/time'].dt.hour, bins=24, range=(0,24))[0]
    st.bar_chart(hist_values)

def custom_filter_slider(data):
    # st.header('Map of all pickups')
    # st.map(data)
    hour_to_filter = st.slider('hour', 0, 23, 17)
    filtered_data = data[data['date/time'].dt.hour == hour_to_filter]
    st.subheader('Map of all pickups at {}:00'.format(hour_to_filter))
    st.map(filtered_data)

if __name__ == '__main__':
    data_load_state = st.text('Loading Data...')
    data = load_data(10000)
    data_load_state.text('Loading Data...done!')

    print_raw_data(data)

    plot_pickups_by_hour(data)

    custom_filter_slider(data)