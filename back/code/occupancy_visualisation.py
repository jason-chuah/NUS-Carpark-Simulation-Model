import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
data = pd.read_csv('../data/max_occupancy_day_final.csv')
current_slot_statuses = {
    'CP3': {'red': 31, 'white': 212},
    'CP3A': {'red': 14, 'white': 53},
    'CP4': {'red': 21, 'white': 95},
    'CP5': {'red': 17, 'white': 53},
    'CP5B': {'red': 32, 'white': 0},
    'CP6B': {'red': 130, 'white': 43}
}
data["red_occupied"] = data["staff"].astype(int)
data["white_occupied"] = (data["student"] + data["esp"] + data["hourly"]).astype(int)
data = data[["carpark", "date", "red_occupied", "white_occupied"]]
data['date'] = pd.to_datetime(data['date'])
min_date = data['date'].min()
max_date = data['date'].max()
carparks = data['carpark'].unique()

# Create two figures, one for red occupancy and one for white occupancy
fig_red, axs_red = plt.subplots(len(carparks), 1, figsize=(10, 5 * len(carparks)))
fig_white, axs_white = plt.subplots(len(carparks), 1, figsize=(10, 5 * len(carparks)))

# Check if we have only one carpark to avoid indexing issues
single_carpark = len(carparks) == 1
if single_carpark:
    axs_red = [axs_red]
    axs_white = [axs_white]

# Loop through each car park and plot its trend for red and white occupancy
for index, carpark in enumerate(carparks):
    # Filter the data for the current car park
    carpark_data = data[data['carpark'] == carpark]
    
    # Get the max occupancy values for the current car park
    max_red = current_slot_statuses[carpark]['red']
    max_white = current_slot_statuses[carpark]['white']
    
    # Plot the 'red_occupied' trend in the red figure
    axs_red[index].plot(carpark_data['date'], carpark_data['red_occupied'], label='Occupied Red Lots', color='red')
    axs_red[index].axhline(y=max_red, label='Total Red Lots', color='darkred', linestyle='--')
    axs_red[index].set_title(f'Red Occupancy Trend for {carpark}')
    axs_red[index].set_xlabel('Date')
    axs_red[index].set_ylabel('Occupancy')
    axs_red[index].legend()
    axs_red[index].axhline(y=max_red * 0.7, label='Theoretical Optimal Occupancy', color='green', linestyle='--')

    # Plot the 'white_occupied' trend in the white figure
    axs_white[index].plot(carpark_data['date'], carpark_data['white_occupied'], label='Occupied White Lots', color='grey')
    axs_white[index].axhline(y=max_white, label='Total White Lots', color='black', linestyle='--')
    axs_white[index].set_title(f'White Occupancy Trend for {carpark}')
    axs_white[index].set_xlabel('Date')
    axs_white[index].set_ylabel('Occupancy')
    axs_white[index].legend()
    axs_white[index].axhline(y=max_white * 0.7, label='Theoretical Optimal Occupancy', color='green', linestyle='--')
    
    axs_red[index].set_xlim(min_date, max_date)
    axs_white[index].set_xlim(min_date, max_date)
if not single_carpark:
    fig_red.tight_layout()
    fig_white.tight_layout()
fig_red.savefig('../data/red_occupancy_plot.png')
fig_white.savefig('../data/white_occupancy_plot.png')
plt.show()