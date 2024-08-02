import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
from datetime import timedelta, datetime

data = pd.read_csv('../data/cleaned_data.csv')

# Ensure that the 'enter' and 'Exit' columns are in datetime format
data['enter'] = pd.to_datetime(data['enter'])
data['Exit'] = pd.to_datetime(data['Exit'])
# Expand a row to represent each minute a car was parked.
def expand_time(row):
    enter_time = row['enter']
    exit_time = row['Exit']
    carpark = row['carpark']
    minutes = [(enter_time + timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:%S') for i in range(int(row['duration']))]
    return [(minute, row['type'], carpark) for minute in minutes]
# Apply the expand_time_adjusted function to each row in parallel to speed up the process
expanded_data = Parallel(n_jobs=-1)(delayed(expand_time)(row) for _, row in data.iterrows())
# Flatten the list of lists to a single list of tuples
expanded_data_flat = [item for sublist in expanded_data for item in sublist]
# Convert the flattened list to a DataFrame
expanded_df = pd.DataFrame(expanded_data_flat, columns=['time', 'type', 'carpark'])
# Count the number of cars of each type for each minute
occupancy_minute = (expanded_df.groupby(['time', 'carpark', 'type'])
                            .size()
                            .unstack(fill_value=0)
                            .reset_index())
# Add a column for the total number of lots occupied
occupancy_minute['total_occupied'] = occupancy_minute[['hourly', 'student', 'esp', 'staff']].sum(axis=1)
# Rearrange columns for clarity and ensure all columns are present
cols = ['time', 'carpark', 'total_occupied', 'hourly', 'student', 'esp', 'staff']
occupancy_minute = occupancy_minute.reindex(columns=cols, fill_value=0)
# Convert the 'time' column to a datetime format
occupancy_minute['time'] = pd.to_datetime(occupancy_minute['time'])
# Extract the hour and date from the 'time' column
occupancy_minute['hour'] = occupancy_minute['time'].dt.hour
occupancy_minute['date'] = occupancy_minute['time'].dt.date
# Group by carpark, date, and hour and compute the maximum for each group
max_occupancy_hour_grouped = occupancy_minute.groupby(['carpark', 'date', 'hour']).max()
# Reset the index of the grouped DataFrame
max_occupancy_hour_final = max_occupancy_hour_grouped.reset_index()[['carpark', 'date', 'hour', 'total_occupied', 'hourly', 'student', 'esp', 'staff']]
max_occupancy_day_final = max_occupancy_hour_final.groupby(['carpark', 'date']).max().reset_index().drop(columns=['hour'])
occupancy_minute.to_csv('../data/occupancy_minute_final.csv', index=False)
max_occupancy_hour_final.to_csv('../data/max_occupancy_hour_final.csv', index=False)
max_occupancy_day_final.to_csv('../data/max_occupancy_day_final.csv', index=False)