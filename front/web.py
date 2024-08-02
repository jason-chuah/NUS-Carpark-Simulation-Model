import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import random
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime


# Initialize session state variables
if 'selected_carpark' not in st.session_state:
    st.session_state.selected_carpark = None 
if 'total_lots' not in st.session_state:
    st.session_state.total_lots = 0
if 'red_lots' not in st.session_state:
    st.session_state.red_lots = 0
if 'white_lots' not in st.session_state:
    st.session_state.white_lots = 0
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
    st.session_state.expected_cars = None  
if 'event_carpark' not in st.session_state:
    st.session_state.event_carpark = None      

if 'carpark_to_view' not in st.session_state:
    st.session_state.carpark_to_view  = None 


# Load the car park data from the CSV
car_parks = pd.read_csv('carpark_data/car_parks.csv')

occupancy_image = "graphs/monthlyoccupancy.png"
parkinghr_image = "graphs/aveparkinghr.jpg"



# Define the three pages

def main_page():
    st.header("Map of NUS Carparks")
    carpark_map = folium.Map(location=[1.295876, 103.775758], zoom_start=15.4)
    
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
            popup=folium.Popup(html=popup_content, max_width=200),  # Set max width for the popup
        ).add_to(carpark_map)
    
    folium_static(carpark_map)

    if st.button(":violet[Dashboard]"):
        st.session_state.page = "Dashboard"
    if st.button(":red[Simulation]"): 
        st.session_state.page = "Simulation"




def dashboard_page():
    st.header("Dashboard")
    st.subheader("Monthly Carpark Occupancy Trend")
    st.image(occupancy_image, use_column_width=True)
    st.subheader("Smoothed Average Parking Hour Graph")
    st.image(parkinghr_image, use_column_width=True)
    if st.button("Back to Main Page"):
        st.session_state.page = "Main Page"


def simulation_page():
    if st.button("Back to Main Page"):
        st.session_state.page = "Main Page"

    carpark_map = folium.Map(location=[1.295876, 103.775758], zoom_start=15.4)
    
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
            popup=folium.Popup(html=popup_content, max_width=200),  # Set max width for the popup
        ).add_to(carpark_map)
    
    folium_static(carpark_map)

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
        st.write(f"Total Lots: {total_lots}")

        red_lots = st.slider("Red Lots", 0, total_lots, value=carpark_data['Red Lots'])
        white_lots = total_lots - red_lots
        st.slider("White Lots", 0, total_lots, value=white_lots)

    if st.button("Create Simulation"):
        
        st.session_state.total_lots = total_lots
        st.session_state.red_lots = red_lots
        st.session_state.white_lots = white_lots

        st.session_state.page = "Create Simulation"




def create_simulation_page():
    st.header("Create Simulation")
    if st.button("Back to Main Page"):
        st.session_state.page = "Main Page"

    with st.expander("**Simulation Period**", expanded=False):
        start_date = st.date_input("Start Date")
        start_time = st.time_input("Start Time", step=3600)  
        end_date = st.date_input("End Date")
        end_time = st.time_input("End Time", step=3600)  
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
        st.session_state.event_carpark = st.selectbox("Nearest Carpark", car_parks['Car Park Name'])
        event_start_date = st.date_input("Event Start Date")
        event_start_time = st.time_input("Event Start Time")
        event_end_date = st.date_input("Event End Date")
        event_end_time = st.time_input("Event End Time")
        st.session_state.event_start_datetime = datetime.combine(event_start_date, event_start_time)
        st.session_state.event_end_datetime = datetime.combine(event_end_date, event_end_time)

        if st.session_state.event_end_datetime < st.session_state.start_datetime:
            st.error("End time cannot be before the start time.")
        else:
            event_duration = st.session_state.end_datetime - st.session_state.start_datetime
            hours, remainder = divmod(event_duration.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            duration_sentence = f"Event Duration: {int(hours)} hours, and {int(minutes)} minutes"
            st.write(duration_sentence)
        st.session_state.expected_cars = st.number_input("Expected Number of Cars", step=1, value=0, format="%d")

    if st.button(":green[RUN]"):
        st.session_state.page = "Plot Simulation"

        



def plot_simulation_page():
    st.header("Car Park Occupancy Simulation Results")

    
    carpark_to_view = st.selectbox("Select a Carpark to view occupancy rates", car_parks['Car Park Name'])
    st.session_state.carpark_to_view = carpark_to_view
    
    #send variables to backend


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


    # Calculate the duration in hours
    duration = int((st.session_state.simulation_duration).total_seconds() / 3600)+1

    # Lists to store occupancy data
    total_occupancy = []
    red_occupancy = []
    white_occupancy = []

    # Lists to store percentage data
    percentage_total = []
    percentage_red = []
    percentage_white = []

    # Simulate car park occupancy and calculate percentages over the specified duration
    for hour in range(duration):
        if total_lots == 0 :
            total_occupancy.append(0)
            red_occupancy.append(0)
            white_occupancy.append(0)


            percentage_total.append(0)
            percentage_red.append(0)
            percentage_white.append(0)

        elif red_lots == 0:
            occupied_spaces = random.randint(0, total_lots)
            occupied_red = 0
            occupied_white = occupied_spaces - occupied_red

            # Ensure percentages don't exceed 100%
            occupied_spaces = min(occupied_spaces, total_lots)
            occupied_red = min(occupied_red, red_lots)
            occupied_white = min(occupied_white, white_lots)

            total_occupancy.append(occupied_spaces)
            red_occupancy.append(occupied_red)
            white_occupancy.append(occupied_white)


            percentage_total.append((occupied_spaces / total_lots) * 100)
            percentage_red.append(0)
            percentage_white.append((occupied_white / white_lots) * 100)

        elif white_lots == 0:
            occupied_spaces = random.randint(0, total_lots)
            occupied_red = occupied_spaces
            occupied_white = 0

            # Ensure percentages don't exceed 100%
            occupied_spaces = min(occupied_spaces, total_lots)
            occupied_red = min(occupied_red, red_lots)
            occupied_white = min(occupied_white, white_lots)

            total_occupancy.append(occupied_spaces)
            red_occupancy.append(occupied_red)
            white_occupancy.append(occupied_white)


            percentage_total.append((occupied_spaces / total_lots) * 100)
            percentage_red.append((occupied_red / red_lots) * 100)
            percentage_white.append(0)

        else: 
            occupied_spaces = random.randint(0, total_lots)
            occupied_red = random.randint(0, min(occupied_spaces, red_lots))
            occupied_white = occupied_spaces - occupied_red

            # Ensure percentages don't exceed 100%
            occupied_spaces = min(occupied_spaces, total_lots)
            occupied_red = min(occupied_red, red_lots)
            occupied_white = min(occupied_white, white_lots)

            total_occupancy.append(occupied_spaces)
            red_occupancy.append(occupied_red)
            white_occupancy.append(occupied_white)


            percentage_total.append((occupied_spaces / total_lots) * 100)
            percentage_red.append((occupied_red / red_lots) * 100)
            percentage_white.append((occupied_white / white_lots) * 100)

    # Create time points for plotting
    hours = range(duration)

    # Create Matplotlib plots
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(hours, percentage_total, label="Percentage of Total Lots Occupied")
    ax1.plot(hours, percentage_red, label="Percentage of Red Lots Occupied")
    ax1.plot(hours, percentage_white, label="Percentage of White Lots Occupied")
    ax1.set_xlabel("Hour")
    ax1.set_ylabel("Percentage")
    ax1.legend()
    ax1.set_title("Percentage of Car Park Lots Occupied Over Specified Duration")
    ax1.grid(True)

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

    # Add a button to go back to the home page
    if st.button("Back to Main Page"):
        st.session_state.page = "Main Page"




# Initialize the Streamlit app
st.title("Welcome to the Car Park Management System!")


# Define the app's state
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


