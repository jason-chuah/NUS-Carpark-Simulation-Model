import numpy as np
import pandas as pd
import os
from joblib import Parallel, delayed
from pandas import read_csv
# List all files in the 'data' directory that start with "raw_Cp"
files = [f for f in os.listdir('../data/') if f.startswith('raw_Cp') and f.endswith('.csv')]

# Read and concatenate all the matching files
df = pd.concat([pd.read_csv(os.path.join('../data/', f)) for f in files], ignore_index=True)
# Define conditions to check if each column value is not equal to '\\N'
conditions = [
    (df['hourly_du'] != '\\N'),       # Check for 'hourly_du' column
    (df['staff_du'] != '\\N'),       # Check for 'staff_du' column
    (df['student_du'] != '\\N'),     # Check for 'student_du' column
    (df['esp_du'] != '\\N')          # Check for 'esp_du' column
]

# Define the choice of pass types corresponding to each condition
choices = ['hourly', 'staff', 'student', 'esp']

# Define the choice of durations corresponding to each condition
choices_duration = [
    df['hourly_du'],                 # Duration from 'hourly_du' column
    df['staff_du'],                  # Duration from 'staff_du' column
    df['student_du'],                # Duration from 'student_du' column
    df['esp_du']                     # Duration from 'esp_du' column
]

# Assign values to 'type' column based on the conditions and choices. If no condition is met, default to '\\N'
df['type'] = np.select(conditions, choices, default='\\N')

# Assign values to 'duration' column based on the conditions and choices_duration. If no condition is met, default to '\\N'
df['duration'] = np.select(conditions, choices_duration, default='\\N')

# Drop the original columns as they are no longer needed
df = df.drop(columns=['hourly_du', 'staff_du', 'student_du', 'esp_du'])

# Define ExitId mapping
ExitId_data = {
    'ExitId': [48, 52, 70, 76, 82, 83, 92, 161]
}
mapping = {
    48: {'carpark': 'CP6B', 'carpark_exit': 'Exit_6B1'},
    52: {'carpark': 'CP6B', 'carpark_exit': 'Exit_6B2'},
    70: {'carpark': 'CP5', 'carpark_exit': 'Exit_5'},
    76: {'carpark': 'CP4', 'carpark_exit': 'Exit_4'},
    82: {'carpark': 'CP3', 'carpark_exit': 'Exit_3_1'},
    83: {'carpark': 'CP3', 'carpark_exit': 'Exit_3_2'},
    92: {'carpark': 'CP5B', 'carpark_exit': 'Exit_5B'},
    161: {'carpark': 'CP3A', 'carpark_exit': 'Exit_3A'},
}

# Map ExitId to carpark and carpark_exit
df['carpark'] = df['ExitId'].apply(lambda x: mapping.get(x, {}).get('carpark', None))
df['carpark_exit'] = df['ExitId'].apply(lambda x: mapping.get(x, {}).get('carpark_exit', None))
df = df.drop(columns=['ExitId'])
# for records with IU == 0, it has unusual data, so we drop it
df = df[df['IU'] != "0"]
# convert duration to int
df['duration'] = df['duration'].astype(int)
# remove completely duplicated records
df = df.drop_duplicates()
# Convert 'Enter' and 'Exit' columns to datetime format with dayfirst=True
df['enter'] = pd.to_datetime(df['enter'], dayfirst=True)
df['Exit'] = pd.to_datetime(df['Exit'], dayfirst=True)
# Find rows with negative duration and check if swapping makes the duration modulus of original
potential_swaps = df[df['duration'] < 0].copy()
potential_swaps['swapped_duration'] = (potential_swaps['enter'] - potential_swaps['Exit']).dt.total_seconds() / 60
mask_swap = potential_swaps['swapped_duration'] == potential_swaps['duration'].abs()
# Apply the swaps to the main dataframe
df.loc[mask_swap.index, ['enter', 'Exit']] = df.loc[mask_swap.index, ['Exit', 'enter']].values
df.loc[mask_swap.index, 'duration'] = potential_swaps.loc[mask_swap.index, 'swapped_duration']
# Filter rows with dates in the range 2022-2023, range should be adjusted accordingly
mask_dates = ((df['enter'] >= '2022-01-01') & (df['enter'] <= '2023-12-31')) & \
             ((df['Exit'] >= '2022-01-01') & (df['Exit'] <= '2023-12-31'))
df = df[mask_dates]
# for records with duration less than 10, it has no value since the grace period is 10 mins in determining lot allocation
df_short_duration = df[df['duration'] < 10]
df = df[df['duration'] > 9]
df.to_csv('../data/cleaned_data.csv', index=False)
df_short_duration.to_csv('../data/cleaned_data_short_duration.csv', index=False)