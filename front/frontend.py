import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import random
import matplotlib.pyplot as plt
import plotly.express as px
import requests
import json
from datetime import datetime

if 'selected_carpark' not in st.session_state:
    st.session_state.selected_carpark = None 
if 'total_lots' not in st.session_state:
    st.session_state.total_lots = None
if 'red_lots' not in st.session_state:
    st.session_state.red_lots = None
if 'white_lots' not in st.session_state:
    st.session_state.white_lots = None
if 'start_datetime' not in st.session_state:
    st.session_state.start_datetime = None
if 'end_datetime' not in st.session_state:
    st.session_state.end_datetime = None
if 'simulation_duration' not in st.session_state:
    st.session_state.simulation_duration = None

if 'event_start_datetime' not in st.session_state:
    st.session_state.event_start_datetime = None
if 'event_end_datetime' not in st.session_state:
    st.session_state.event_end_datetime = None
if 'expected_cars' not in st.session_state:
    st.session_state.expected_cars = 0  
if 'event_carpark' not in st.session_state:
    st.session_state.event_carpark = None      

if 'carpark_to_view' not in st.session_state:
    st.session_state.carpark_to_view  = None 

car_parks = pd.read_csv('carpark_data/car_parks2.csv')

occupancy_image = "graphs/monthlyoccupancy.png"
parkinghr_image = "graphs/aveparkinghr.jpg"


def main_page():
    st.header("Map of NUS Carparks")
    carpark_map = folium.Map(location=[1.300308, 103.774887], zoom_start=16.4)
    
    for index, row in car_parks.iterrows():
        description = row['Description']
        
        # HTML-formatted popup content with CSS styling
        popup_content = f"""
        <div style="font-family: Arial, sans-serif;">
            <h4 style="color: #0074D9; font-size: 16px;">{row['Car Park Name']}</h4>
            <p><strong>Description:</strong> {description}</p>
        </div>
        """
        
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(html=popup_content, max_width=200),  
        ).add_to(carpark_map)
    
    folium_static(carpark_map)

    if st.button(":violet[Dashboard]"):
        st.session_state.page = "Dashboard"
    if st.button(":red[Simulation]"): 
        st.session_state.page = "Simulation"




def dashboard_page():
    st.header("Dashboard")
    st.subheader("Monthly Carpark Occupancy Trend:")
    st.image(occupancy_image, use_column_width=True)
    st.subheader("Smoothed Average Parking Hour Graph:")
    st.image(parkinghr_image, use_column_width=True)
    if st.button("Back to Main Page"):
        st.session_state.page = "Main Page"


def simulation_page():

    selected_carpark = st.selectbox("Select a Carpark", car_parks['Car Park Name'])
    st.session_state.selected_carpark = selected_carpark
    carpark_data = car_parks[car_parks['Car Park Name'] == selected_carpark].iloc[0]

    selected = st.selectbox("Choose to", ["", "Close Carpark", "Reallocate Lots"])
    total_lots = carpark_data['Total Occupancy']
    red_lots = carpark_data['Red Lots']
    white_lots = carpark_data['White Lots']

    if selected == "Close Carpark":
        total_lots = carpark_data['Total Occupancy']
        red_lots = 0  # Set red lots to 0 when closing the carpark
        white_lots = 0  # Set white lots to 0 when closing the carpark
        st.write(f"Total Lots: {total_lots}")
        total_lots=0 #set total lots to 0 when carpark closed
        st.write("You chose to close this carpark.")
    elif selected == "Reallocate Lots":
        total_lots = carpark_data['Total Occupancy']
        st.warning("To reallocate lots, please use the **:red['Red Lots' Slider]** only. Using the White Lots Slider may result in an error.")
        red_lots = st.slider("Red Lots", 0, total_lots, value=carpark_data['Red Lots'])
        white_lots = total_lots - red_lots
        st.slider("White Lots", 0, total_lots, value=white_lots)



    if st.button(":red[Create Simulation]"):  
        st.session_state.total_lots = total_lots
        st.session_state.red_lots = red_lots
        st.session_state.white_lots = white_lots
        st.session_state.page = "Create Simulation"

    if st.button("Back to Main Page"):
        st.session_state.page = "Main Page"




def create_simulation_page():
    st.header("Create Simulation")

    with st.expander("**Simulation Period**", expanded=False):
        default_time = datetime.strptime('00:00', '%H:%M').time()
        start_date = st.date_input("Start Date")
        start_time = st.time_input("Start Time", value=default_time, step=3600)  
        end_date = st.date_input("End Date")
        end_time = st.time_input("End Time", value=default_time, step=3600)  
        st.session_state.start_datetime = datetime.combine(start_date, start_time)
        st.session_state.end_datetime = datetime.combine(end_date, end_time)

    if st.session_state.end_datetime < st.session_state.start_datetime:
        st.error("End time cannot be before the start time.")

    else:
        duration = st.session_state.end_datetime - st.session_state.start_datetime
        st.session_state.simulation_duration = duration
        hours, remainder = divmod(duration.total_seconds(), 3600)
        duration_sentence = f"Simulation Duration: {int(hours)} hours"
        st.write(duration_sentence)

    with st.expander("**Plan for an Event :red[(optional)]**", expanded=False):
        st.session_state.event_carpark = st.selectbox("Nearest Carpark", [""] + list(car_parks['Car Park Name']))
        if st.session_state.event_carpark == "" :
            st.session_state.event_carpark = None
        default_date = None
        event_start_date = st.date_input("Event Start Date",default_date)
        event_start_time = st.time_input("Event Start Time",default_date)
        event_end_date = st.date_input("Event End Date",default_date)
        event_end_time = st.time_input("Event End Time",default_date)

        

        if all(v is not None for v in [event_start_date, event_start_time, event_end_date, event_end_time]):
            st.session_state.event_start_datetime = datetime.combine(event_start_date, event_start_time)
            st.session_state.event_end_datetime = datetime.combine(event_end_date, event_end_time)

            if st.session_state.event_end_datetime < st.session_state.event_start_datetime:
                st.error("End time cannot be before the start time.")
            else:
                event_duration = st.session_state.event_end_datetime - st.session_state.event_start_datetime
                hours, remainder = divmod(event_duration.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                duration_sentence = f"Event Duration: {int(hours)} hours, and {int(minutes)} minutes"
                st.write(duration_sentence)

        st.session_state.expected_cars = st.number_input("Expected Number of Cars", step=1, value=0, format="%d")

    if st.button(":green[RUN]"):
        st.session_state.page = "Plot Simulation"

    if st.button("Back"):
        st.session_state.page = "Simulation"



def plot_simulation_page():
    st.header("Car Park Occupancy Simulation Results")

    
    carpark_to_view = st.selectbox("Select a Carpark to view occupancy rates", car_parks['Car Park Name'])
    st.session_state.carpark_to_view = carpark_to_view
    
    if st.session_state.event_start_datetime and st.session_state.event_end_datetime != None:
        data = {
        'selected_carpark': st.session_state.selected_carpark,
        'total_lots': int(st.session_state.total_lots),
        'red_lots': int(st.session_state.red_lots),
        'white_lots': int(st.session_state.white_lots),
        'start_datetime': st.session_state.start_datetime.isoformat(),
        'end_datetime': st.session_state.end_datetime.isoformat(),
        'carpark_to_view': st.session_state.carpark_to_view,
        'event_start_datetime': st.session_state.event_start_datetime.isoformat(),
        'event_end_datetime': st.session_state.event_end_datetime.isoformat(),
        'expected_cars': int(st.session_state.expected_cars),
        'event_carpark' : st.session_state.event_carpark,
        }
    else:
        data = {
        'selected_carpark': st.session_state.selected_carpark,
        'total_lots': int(st.session_state.total_lots),
        'red_lots': int(st.session_state.red_lots),
        'white_lots': int(st.session_state.white_lots),
        'start_datetime': st.session_state.start_datetime.isoformat(),
        'end_datetime': st.session_state.end_datetime.isoformat(),
        'carpark_to_view': st.session_state.carpark_to_view,
        'event_start_datetime': st.session_state.event_start_datetime,
        'event_end_datetime': st.session_state.event_end_datetime,
        'expected_cars': st.session_state.expected_cars,
        'event_carpark' : st.session_state.event_carpark,
        }


    
 
    #response = requests.post('http://127.0.0.1:5000/simulate', json=data)
    response = requests.post('http://flask-app:5000/simulate', json=data)


    if response.status_code == 200:
        red_occupancy, white_occupancy = response.json()
    else:
        st.error("Simulation failed. Please try again.")


    if st.session_state.carpark_to_view == st.session_state.selected_carpark :
        total_lots = st.session_state.total_lots
        red_lots = st.session_state.red_lots
        white_lots = st.session_state.white_lots

    else :
        carpark_data = car_parks[car_parks['Car Park Name'] == st.session_state.carpark_to_view].iloc[0]
        total_lots = carpark_data['Total Occupancy']
        red_lots = carpark_data['Red Lots']
        white_lots = carpark_data['White Lots']

    st.divider()


    
    duration = int((st.session_state.simulation_duration).total_seconds() / 3600)
    total_occupancy = [red + white for red, white in zip(red_occupancy, white_occupancy)]
    
    percentage_total = []
    percentage_red = []
    percentage_white = []

    for i in range(len(red_occupancy)):
        if total_lots == 0 :
            percentage_total.append(0)
            percentage_red.append(0)
            percentage_white.append(0)

        elif red_lots == 0:
        
            percentage_total.append((total_occupancy[i] / total_lots) * 100)
            percentage_red.append(0)
            percentage_white.append((white_occupancy[i] / white_lots) * 100)

        elif white_lots == 0:
            percentage_total.append((total_occupancy[i] / total_lots) * 100)
            percentage_white.append(0)
            percentage_red.append((red_occupancy[i] / red_lots) * 100)


        else: 

            percentage_total.append((total_occupancy[i] / total_lots) * 100)
            percentage_red.append((red_occupancy[i] / red_lots) * 100)
            percentage_white.append((white_occupancy[i] / white_lots) * 100)

    # Create time points for plotting
    hours = range(1, duration+1)

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(hours, percentage_total, label="Percentage of Total Lots Occupied")
    ax1.plot(hours, percentage_red, label="Percentage of Red Lots Occupied")
    ax1.plot(hours, percentage_white, label="Percentage of White Lots Occupied")
    ax1.axhline(y=70, color='gray', linestyle='--', label='Threshold at 70%')
    ax1.set_xlabel("Hour")
    ax1.set_ylabel("Percentage")
    ax1.legend()
    ax1.set_title("Percentage of Car Park Lots Occupied Over Specified Duration")
    ax1.grid(True)
    ax1.set_ylim(0, 100)

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.plot(hours, total_occupancy, label="Total Lots Occupied", color='blue')
    ax2.plot(hours, red_occupancy, label="Red Lots Occupied", color='red')
    ax2.plot(hours, white_occupancy, label="White Lots Occupied", color='green')
    ax2.set_xlabel("Hour")
    ax2.set_ylabel("Number of Occupied Lots")
    ax2.legend()
    ax2.set_title("Car Park Occupancy Over Specified Duration")
    ax2.grid(True)
    st.pyplot(fig1)
    st.pyplot(fig2)

    
    if st.button("Back to Main Page"):
        st.session_state.page = "Main Page"


st.title("Welcome to the Car Park Management System!")

if 'page' not in st.session_state:
    st.session_state.page = "Main Page"

# Page routing
if st.session_state.page == "Main Page":
    main_page()
elif st.session_state.page == "Dashboard":
    dashboard_page()
elif st.session_state.page == "Edit Carparks":
    edit_carparks_page()
elif st.session_state.page == "Simulation":
    simulation_page()
elif st.session_state.page == "Plot Simulation":
    plot_simulation_page()
elif st.session_state.page == "Create Simulation":
    create_simulation_page()
