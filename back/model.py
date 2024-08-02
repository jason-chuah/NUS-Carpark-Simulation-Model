## importing libraries
import numpy as np
import pandas as pd
import datetime
import random
import ast
import matplotlib.pyplot as plt
import seaborn as sns
import simpy
import math
import itertools
from numpy.random import normal, uniform
from datetime import datetime, timedelta, date
## Functions
### Simulation Functions

data1 = {'selected_carpark':'Carpark 3', 
            'total_lots': 243, 
            'red_lots': 20, 
            'white_lots': 223, 
            'start_datetime': '2023-11-13T10:00:00', 
            'end_datetime': '2023-11-13T17:00:00', 
            'carpark_to_view': 'Carpark 3A', 
            'event_start_datetime': None, 
            'event_end_datetime': None, 
            'expected_cars': 0, 
            'event_carpark': None}

data2 = {'selected_carpark':'Carpark 3', 
        'total_lots': 0, 
        'red_lots': 0, 
        'white_lots': 0, 
        'start_datetime': '2023-11-13T10:00:00', 
        'end_datetime': '2023-11-14T17:00:00', 
        'carpark_to_view': 'Carpark 3A', 
        'event_start_datetime': '2023-11-13T06:45:00', 
        'event_end_datetime': '2023-11-13T16:45:19', 
        'expected_cars': 427, 
        'event_carpark': 'Carpark 4/4A'}

data3 = {'selected_carpark': 'Carpark 3', 
        'total_lots': 0, 
        'red_lots': 0, 
        'white_lots': 0, 
        'start_datetime': '2023-11-13T00:00:00', 
        'end_datetime': '2023-11-13T08:00:00', 
        'carpark_to_view': 'Carpark 3A', 
        'event_start_datetime': None, 
        'event_end_datetime': None, 
        'expected_cars': None, 
        'event_carpark': None}

data4 = {"selected_carpark": "Carpark 3", 
        "total_lots": 243, 
        "red_lots": 70, 
        "white_lots": 173, 
        "start_datetime": "2023-11-13T00:00:00", 
        "end_datetime": "2023-11-14T00:00:00", 
        "carpark_to_view": "Carpark 4/4A", 
        "event_start_datetime": "2023-11-13T00:45:00", 
        "event_end_datetime": "2023-11-13T04:30:00", 
        "expected_cars": 20, 
        "event_carpark": "Carpark 3"}

data5 = {'selected_carpark': 'Carpark 3', 
        'total_lots': 0, 'red_lots': 0, 'white_lots': 0, 
        'start_datetime': '2023-11-14T10:00:00', 
        'end_datetime': '2023-11-14T17:00:00', 
        'carpark_to_view': 'Carpark 3', 
        'event_start_datetime': None, 
        'event_end_datetime': None, 
        'expected_cars': None, 
        'event_carpark': None}

data6 = {'selected_carpark': 'Carpark 3', 
         'total_lots': 0, 'red_lots': 0, 'white_lots': 0, 
         'start_datetime': '2023-11-13T15:00:00', 
         'end_datetime': '2023-11-13T17:00:00', 
         'carpark_to_view': 'Carpark 3A', 
         'event_start_datetime': None, 
         'event_end_datetime': None, 
         'expected_cars': None, 
         'event_carpark': None}

data7 = {'selected_carpark': 'Carpark 3', 
         'total_lots': 243, 'red_lots': 70, 'white_lots': 173, 
         'start_datetime': '2023-11-13T00:00:00', 
         'end_datetime': '2023-11-14T00:00:00', 
         'carpark_to_view': 'Carpark 4/4A', 
         'event_start_datetime': '2023-11-13T00:45:00', 
         'event_end_datetime': '2023-11-13T04:30:00', 
         'expected_cars': 20, 
         'event_carpark': 'Carpark 3'}

data8 = {'selected_carpark':'Carpark 3', 
            'total_lots': 243, 
            'red_lots': 20, 
            'white_lots': 223, 
            'start_datetime': '2023-11-13T00:00:00', 
            'end_datetime': '2023-11-13T06:00:00', 
            'carpark_to_view': 'Carpark 3A', 
            'event_start_datetime': None, 
            'event_end_datetime': None, 
            'expected_cars': 0, 
            'event_carpark': None}

def run_simulation(data):
    def handle_initial_cars(env, carpark, car_type, initial_count):
        if carpark == carpark_to_close:
            carpark = find_nearest_carpark(carpark, car_type)

        for _ in range(initial_count):
            # Assuming the car is already in the carpark for 1 hour
            duration = random.randint(64, 145) - 60  # Duration minus 1 hour
            yield env.timeout(max(0, duration))  # Simulate the car parked for 'duration'

            # Now simulate the car leaving
            #print(f"Before leaving: {car_parks[carpark][car_type].level}")
            yield car_parks[carpark][car_type].put(1) # Car is leaving, so we need to add a parking space
            #print(f"After leaving: {car_parks[carpark][car_type].level}")
    def record_hourly_occupancy(env, carpark_to_view):
        while True:
            # Temporary lists to store minute-by-minute occupancy for one hour
            red_occupancy = []
            white_occupancy = []

            # Record occupancy for each minute in the hour
            for _ in range(60):  # 60 minutes
                # print out the current occupancy level of the carpark
                #print('minute: ', env.now, 'red: ', car_parks[carpark_to_view]['red'].level, 'white: ', car_parks[carpark_to_view]['white'].level)
                red_occupancy.append(car_parks[carpark_to_view]['red'].capacity - car_parks[carpark_to_view]['red'].level)
                white_occupancy.append(car_parks[carpark_to_view]['white'].capacity - car_parks[carpark_to_view]['white'].level)
                yield env.timeout(1)  # Wait for one minute

            # Calculate the average occupancy for the hour
            hourly_avg_red = sum(red_occupancy) / len(red_occupancy)
            hourly_avg_white = sum(white_occupancy) / len(white_occupancy)

            # Append the hourly average to the main log
            hourly_occupancy[carpark_to_view]['red'].append(hourly_avg_red)
            hourly_occupancy[carpark_to_view]['white'].append(hourly_avg_white)
    # Function to find the nearest available carpark
    def find_nearest_carpark(carpark_name, car_type):
        for priority_carpark in CARPARK_PRIORITIES[carpark_name]:
            if car_parks[priority_carpark][car_type].level > 0:
                return priority_carpark
        return None
    def car_process(env, car_info):
        enter_time = car_info['enter_simulation']
        carpark = car_info['carpark']
        car_type = car_info['type']
        duration = round(car_info['car_duration'])
        
        # Wait until the car's entry time
        yield env.timeout(max(0, enter_time))

        # Check if there is enough space in the carpark or the carpark is closed
        if carpark == carpark_to_close or car_parks[carpark][car_type].level <= 0:
            # Find an alternative carpark if the intended one is full
            carpark = find_nearest_carpark(carpark, car_type)

        # Check if an alternative carpark was found (not None)
        if carpark:
            # Park the car in the carpark
            yield car_parks[carpark][car_type].get(1)
            #if carpark == carpark_to_view: print(f"Car of type {car_type} parked at carpark {carpark} at time {env.now}. {car_type} Carpark level: {car_parks[carpark][car_type].level}")
            # Car stays for the duration
            yield env.timeout(max(0, duration))
            # Car leaves the carpark
            yield car_parks[carpark][car_type].put(1)
            #if carpark == carpark_to_view: print(f"Car of type {car_type} left carpark {carpark} at time {env.now}. {car_type} Carpark level: {car_parks[carpark][car_type].level}")
        else:
            #print(f"No available carpark found for car of type {car_type} at time {env.now}")
            #for name in CARPARK_NAMES:
                #print(f"{name} red: {car_parks[name]['red'].level}, white: {car_parks[name]['white'].level}")
            pass

    def event_simulation(env, event_carpark, expected_cars, event_start, event_end):
        event_start_delay = event_start
        event_duration = event_end - event_start

        yield env.timeout(max(0, event_start_delay))

        # Temporary list to keep track of where each car is parked
        parked_cars = []
        # if expected car is not Nonetype, add the expected number of cars to the event carpark or redirect if full
        if expected_cars:
            for _ in range(expected_cars):
                current_carpark = event_carpark
                while True:
                    if car_parks[current_carpark]['white'].level > 0:
                        yield car_parks[current_carpark]['white'].get(1)
                        parked_cars.append(current_carpark)
                        break
                    else:
                        # Find the nearest carpark with available space
                        new_carpark = find_nearest_carpark(current_carpark, 'white')
                        if new_carpark and new_carpark != current_carpark:
                            current_carpark = new_carpark
                        else:
                            # No available space found in nearby carparks
                            break

        yield env.timeout(max(0, event_duration))

        # After the event, the cars leave
        for carpark in parked_cars:
            yield car_parks[carpark]['white'].put(1)
    ### Helper Functions
    def predict_arrival(means, covariances, weights, ratio):
        # Parse the string representations to lists of floats
        means = ast.literal_eval(means)
        covariances = ast.literal_eval(covariances)
        weights = ast.literal_eval(weights)
        ratio = float(ratio)

        sorted_indices = np.argsort(weights)[::-1]
        sorted_means = np.array(means)[sorted_indices]
        sorted_covariances = np.array(covariances)[sorted_indices]
        sorted_weights = np.array(weights)[sorted_indices]

        random_number = uniform(0, 1)

        cumulative_probability = 0
        arrival = 0 

        for mean, covariance, weight in zip(sorted_means, sorted_covariances, sorted_weights):
            cumulative_probability += weight
            if random_number <= cumulative_probability:
                arrival = normal(mean, np.sqrt(covariance))
                break

        if arrival == 0:
            arrival = normal(sorted_means[-1], np.sqrt(sorted_covariances[-1]))

        adjusted_arrival = arrival * ratio

        return max(0, round(adjusted_arrival / 24)) # arrival in an hour
    def predict_duration(means, covariances, weights, ratio):
        # Parse the string representations to lists of floats
        means = ast.literal_eval(means)
        covariances = ast.literal_eval(covariances)
        weights = ast.literal_eval(weights)
        ratio = float(ratio)

        sorted_indices = np.argsort(weights)[::-1]
        sorted_means = np.array(means)[sorted_indices]
        sorted_covariances = np.array(covariances)[sorted_indices]
        sorted_weights = np.array(weights)[sorted_indices]

        random_number = uniform(0, 1)

        cumulative_probability = 0
        duration = 0 

        for mean, covariance, weight in zip(sorted_means, sorted_covariances, sorted_weights):
            cumulative_probability += weight
            if random_number <= cumulative_probability:
                duration = normal(mean, np.sqrt(covariance))
                break

        if duration == 0:
            duration = normal(sorted_means[-1], np.sqrt(sorted_covariances[-1]))

        adjusted_duration = duration * ratio

        return max(-adjusted_duration, adjusted_duration) # in minutes
    def label_period(row):  ## row must has column 'enter' which is a datetime object
        year = row['enter'].year
        
        def find_nth_weekday(year, month, day, n):
            if n > 0:
                date_ = date(year, month, 1)
                # Forward to the first occurrence of the day.
                while date_.weekday() != day:
                    date_ += timedelta(days=1)
                # Forward to the nth occurrence.
                for _ in range(1, n):
                    date_ += timedelta(weeks=1)
            else:
                # Start from the last day of the month.
                last_day = date(year, month + 1, 1) - timedelta(days=1)
                date_ = last_day
                # Backward to the last occurrence of the day in the month.
                while date_.weekday() != day:
                    date_ -= timedelta(days=1)
                # Backward to the nth last occurrence.
                for _ in range(-n - 1):
                    date_ -= timedelta(weeks=1)
            return date_
        
        first_aug_mon = find_nth_weekday(year, 8, 0, 1)  # First Monday of August
        second_aug_mon = first_aug_mon + timedelta(weeks=1)
        
        first_dec_sat = find_nth_weekday(year, 12, 5, 1)  # First Saturday of December
        
        first_jan_mon = find_nth_weekday(year, 1, 0, 1)  # First Monday of January
        second_jan_mon = find_nth_weekday(year, 1, 0, 2)  # Second Monday of January
        
        first_may_sat = find_nth_weekday(year, 5, 5, 1)  # First Saturday of May
        
        # Exam periods
        third_nov_sat = find_nth_weekday(year, 11, 5, 3)  # Third Saturday of November
        first_dec_sat = find_nth_weekday(year, 12, 5, 1)  # First Saturday of December
        
        second_last_apr_sat = find_nth_weekday(year, 4, 5, -2)  # Second last Saturday of April
        
        # Additional holiday periods
        third_sep_sat = find_nth_weekday(year, 9, 5, 3)  # Third Saturday of September
        last_sep_sun = find_nth_weekday(year, 9, 6, -1)  # Last Sunday of September
        
        second_nov_sat = find_nth_weekday(year, 11, 5, 2)  # Second Saturday of November
        third_nov_fri = find_nth_weekday(year, 11, 4, 3)  # Third Friday of November
        
        second_feb_sat = find_nth_weekday(year, 2, 5, 2)  # Second Saturday of February
        last_feb_sun = find_nth_weekday(year, 2, 6, -1)  # Last Sunday of February
        
        third_last_apr_sat = find_nth_weekday(year, 4, 5, -3)  # Third last Saturday of April
        second_last_apr_fri = find_nth_weekday(year, 4, 4, -2)  # Second last Friday of April
        enter_date = row['enter'].date()
        if (third_nov_sat <= enter_date < first_dec_sat) or (second_last_apr_sat <= enter_date < first_may_sat):
            return 'Exam'
        elif (third_sep_sat <= enter_date <= last_sep_sun) or \
            (second_nov_sat <= enter_date <= third_nov_fri) or \
            (second_feb_sat <= enter_date <= last_feb_sun) or \
            (third_last_apr_sat <= enter_date <= second_last_apr_fri):
            return 'Holiday'
        elif (second_aug_mon <= enter_date <= first_dec_sat) or (second_jan_mon <= enter_date <= first_may_sat):
            return 'School'
        else:
            return 'Holiday'  # Default to Holiday if none of the above conditions are met
    def map_distribution(row): # the row must have columns 'period' and 'day_of_week'
        filtered_gmm = gmm_model_data[(gmm_model_data[row['period']] == True) & (gmm_model_data[row['day_of_week']] == True)]
        if not filtered_gmm.empty:
            match = filtered_gmm.iloc[0]
            return pd.Series({
                'Means': match['Means'],
                'Covariances': match['Covariances'],
                'Weights': match['Weights']
            })
        else:
            return pd.Series({
                'Means': None,
                'Covariances': None,
                'Weights': None
            })
    def map_arrival_distribution(row):
        filtered_gmm = gmm_arrival_info[
            (gmm_arrival_info['period'] == row['period']) & 
            (gmm_arrival_info['day_of_week'] == row['day_of_week']) & 
            (gmm_arrival_info['type'] == row['type']) & 
            (gmm_arrival_info['carpark'] == row['carpark'])
        ]
        if not filtered_gmm.empty:
            match = filtered_gmm.iloc[0]
            return pd.Series({
                'Means': match['Means'],
                'Covariances': match['Covariances'],
                'Weights': match['Weights']
            })
        else:
            return pd.Series({
                'Means': None,
                'Covariances': None,
                'Weights': None
            })
    # function for initial occupancy prediction
    def bootstrap_sample(data, n_bootstraps=1000):
        n = len(data)
        if n == 0:
            return 0  # Return 0 if there are no data points

        bootstrap_samples = np.empty(n_bootstraps)

        for i in range(n_bootstraps):
            sample = np.random.choice(data, size=n, replace=True)
            bootstrap_samples[i] = np.mean(sample)

        return np.median(bootstrap_samples)

    def get_bootstrap_samples(df, hour, day_of_week, period, carpark, n_bootstraps=1000):
        filtered_data = df[(df['hour'] == hour) & (df['day_of_week'] == day_of_week) &
                        (df['period'] == period) & (df['carpark'] == carpark)]

        median_red = math.ceil(bootstrap_sample(filtered_data['red'], n_bootstraps))
        median_white = math.ceil(bootstrap_sample(filtered_data['white'], n_bootstraps))

        return {'red': median_red, 'white': median_white}
    ## inputs
    MATCHED_CPS = {'Carpark 3':'CP3', 'Carpark 3A':'CP3A', 'Carpark 4/4A':'CP4', 
                   'Carpark 5':'CP5', 'Carpark 5B':'CP5B', 'Carpark 6B':'CP6B'}
    # Global Variables / User Inputs
    selected_carpark = MATCHED_CPS.get(data.get('selected_carpark'))
    total_lots = data.get('total_lots')                     # lots amount from selected cp
    red_lots = data.get('red_lots')
    white_lots = data.get('white_lots')
    start_datetime = datetime.strptime(data.get('start_datetime'), '%Y-%m-%dT%H:%M:%S')
    end_datetime = datetime.strptime(data.get('end_datetime'), '%Y-%m-%dT%H:%M:%S')
    carpark_to_view = MATCHED_CPS.get(data.get('carpark_to_view'))
    event_start_datetime = data.get('event_start_datetime')     # optional
    event_end_datetime = data.get('event_end_datetime')         # optional
    expected_cars = data.get('expected_cars')                   # optional
    event_carpark = MATCHED_CPS.get(data.get('event_carpark'))  # optional

    if event_start_datetime != None:
        event_start_datetime = datetime.strptime(event_start_datetime, '%Y-%m-%dT%H:%M:%S') 
        event_end_datetime = datetime.strptime(event_end_datetime, '%Y-%m-%dT%H:%M:%S')     

    if event_start_datetime == None:
        event_start_datetime = start_datetime
        event_end_datetime = start_datetime

    # check carpark purpose
    if total_lots == 0: 
        carpark_to_close = selected_carpark
    else:
        carpark_to_close = None
    #print all variables
    #print('selected_carpark: ', selected_carpark)
    #print('total_lots: ', total_lots)
    #print('red_lots: ', red_lots)
    #print('white_lots: ', white_lots)
    #print('start_datetime: ', start_datetime)
    #print('end_datetime: ', end_datetime)
    #print('carpark_to_view: ', carpark_to_view)
    #print('event_start_datetime: ', event_start_datetime)
    #print('event_end_datetime: ', event_end_datetime)
    #print('expected_cars: ', expected_cars)
    #print('event_carpark: ', event_carpark)
    #print('carpark_to_close: ', carpark_to_close)

    simulation_start = start_datetime
    simulation_end = (end_datetime - start_datetime).total_seconds() / 60  # Convert to minutes
    event_start = (event_start_datetime - start_datetime).total_seconds() / 60  # Convert to minutes, this is the delay
    event_end = (event_end_datetime - start_datetime).total_seconds() / 60  # Convert to minutes
    ## Constants
    CARPARK_NAMES = ['CP3', 'CP3A', 'CP4', 'CP5', 'CP5B', 'CP6B']
    CAR_TYPES = ['red', 'white']
    CARPARK_PRIORITIES = {
        'CP3': ['CP3A', 'CP4', 'CP5', 'CP5B', 'CP6B'],
        'CP3A': ['CP3', 'CP4', 'CP5', 'CP5B', 'CP6B'],
        'CP4': ['CP5', 'CP5B', 'CP6B', 'CP3', 'CP3A'],
        'CP5': ['CP4', 'CP5B', 'CP6B', 'CP3', 'CP3A'],
        'CP5B': ['CP5', 'CP6B', 'CP4', 'CP3', 'CP3A'],
        'CP6B': ['CP5B', 'CP5', 'CP4', 'CP3', 'CP3A']
    }
    CARPARK_CAPACITIES = {
        'CP3': {'red': 31, 'white': 212},
        'CP3A': {'red': 14, 'white': 53},
        'CP4': {'red': 21, 'white': 95},
        'CP5': {'red': 17, 'white': 53},
        'CP5B': {'red': 32, 'white': 1},
        'CP6B': {'red': 130, 'white': 43}
    }
    CARPARK_CAPACITIES[selected_carpark]['red'] = red_lots
    CARPARK_CAPACITIES[selected_carpark]['white'] = white_lots

    ## scaling of duration based on enter hour
    RATIO_BY_HOUR = pd.DataFrame({
        "enter_hour": range(24),
        "ratio": [
            1.028112, 0.839357, 1.574297, 1.277108, 0.650602, 1.004016, 1.092369,
            2.401606, 1.959839, 1.445783, 0.907631, 0.875502, 1.116466, 1.373494,
            0.995984, 0.787149, 0.755020, 0.819277, 1.253012, 1.108434, 0.827309,
            0.546185, 0.405622, 0.690763
        ]
    })

    ## scaling of arrival rate based on enter hour
    ARRIVAL_RATE_BY_HOUR = pd.DataFrame({
        "enter_hour": range(24),
        "ratio": [
            0.073257, 0.049532, 0.025049, 0.016542, 0.036960, 0.030815, 0.162679,
            1.162667, 2.992213, 2.556639, 1.730767, 1.512129, 1.537367, 2.182695,
            1.749294, 1.412215, 1.278556, 1.196318, 1.547954, 1.286496, 0.604776,
            0.454574, 0.261269, 0.139236
        ]
    })
    DAY_OF_WEEK = start_datetime.strftime('%A')
    PERIOD = label_period({'enter': start_datetime})
    combinations = list(itertools.product(CARPARK_NAMES, CAR_TYPES))
    comb_df = pd.DataFrame(combinations, columns=['carpark', 'type'])
    gmm_model_data = pd.read_csv('data/gmm_info.csv')
    gmm_arrival_info = pd.read_csv('data/gmm_arrival_info.csv')
    bootstrap_occupancy_data = pd.read_csv('data/bootstrap_occupancy_data.csv')

    ## process of inputs
    ### car_info_df creation
    start_time = start_datetime
    end_time = end_datetime
    hours_in_range = []
    current_time = start_time
    while current_time < end_time:
        hours_in_range.append(current_time)
        current_time += timedelta(hours=1)
    date_df = pd.DataFrame({'enter': hours_in_range})
    date_df['period'] = date_df.apply(lambda row: label_period(row), axis=1)
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    date_df['day_of_week'] = date_df['enter'].dt.dayofweek.apply(lambda x: day_names[x])
    date_df['enter_hour'] = date_df['enter'].dt.hour
    date_df['ratio'] = date_df['enter_hour'].apply(lambda x: ARRIVAL_RATE_BY_HOUR['ratio'][x])

    date_df['key'] = 1
    comb_df['key'] = 1

    date_df = pd.merge(date_df, comb_df, on='key').drop('key', axis=1)
        
    distribution_info = date_df.apply(map_arrival_distribution, axis=1)

    date_df = pd.concat([date_df, distribution_info], axis=1)

    date_df['predicted_arrival'] = date_df.apply(lambda row: predict_arrival(row['Means'], row['Covariances'], row['Weights'], row['ratio']), axis=1)
    date_df
    date_df_with_predicted_arrival = date_df[['enter', 'carpark', 'type', 'predicted_arrival']]
    date_df_with_predicted_arrival.head()
    car_info_df = pd.DataFrame(
        date_df_with_predicted_arrival.loc[idx].drop('predicted_arrival') 
        for idx, row in date_df_with_predicted_arrival.iterrows() 
        for _ in range(row.predicted_arrival)
    )

    if len(car_info_df) > 0: #if car_info_df is not empty
        car_info_df['period'] = car_info_df.apply(lambda row: label_period(row), axis=1)
        car_info_df['day_of_week'] = car_info_df['enter'].dt.dayofweek.apply(lambda x: day_names[x])
        car_info_df['enter_hour'] = car_info_df['enter'].dt.hour
        car_info_df['ratio'] = car_info_df['enter_hour'].apply(lambda x: RATIO_BY_HOUR['ratio'][x])

        distribution_info = car_info_df.apply(map_distribution, axis=1)
        car_info_df = pd.concat([car_info_df, distribution_info], axis=1)
        car_info_df['car_duration'] = car_info_df.apply(lambda row: predict_duration(row['Means'], row['Covariances'], row['Weights'], row['ratio']), axis=1)
        car_info_df = car_info_df[['enter', 'carpark', 'type', 'car_duration']]
        car_info_df['enter'] = pd.to_datetime(car_info_df['enter'])
        car_info_df.reset_index(drop=True, inplace=True)
        # randomize the minutes
    
        random_minutes = np.random.randint(0, 60, size=len(car_info_df))

        for idx, dt in enumerate(car_info_df['enter']):
            new_minute = int(random_minutes[idx])  # Convert to Python int
            car_info_df.at[idx, 'enter'] = dt.replace(minute=0) + timedelta(minutes=new_minute)

        car_info_df['enter_simulation'] = (car_info_df['enter'] - start_time).dt.total_seconds() / 60

    ### initial_occupancy creation
    initial_occupancy = comb_df
    initial_occupancy['period'] = PERIOD
    initial_occupancy['day_of_week'] = DAY_OF_WEEK
    initial_occupancy['hour'] = start_time.hour
    initial_occupancy['occupancy'] = initial_occupancy.apply(lambda row: get_bootstrap_samples(bootstrap_occupancy_data, row['hour'], row['day_of_week'], row['period'], row['carpark'])['red'] if row['type'] == 'red' else get_bootstrap_samples(bootstrap_occupancy_data, row['hour'], row['day_of_week'], row['period'], row['carpark'])['white'], axis=1)
    ## Execution of DES
    # Initialize environment
    env = simpy.Environment()

    simulation_start_time = start_datetime

    # Convert end_datetime to a duration in minutes from the start
    simulation_duration = (end_datetime - simulation_start_time).total_seconds() / 60

    # Initialize car parks
    car_parks = {
        name: {
            'red': simpy.Container(env, init=max(0, CARPARK_CAPACITIES[name]['red'] - initial_occupancy[(initial_occupancy['carpark'] == name) & (initial_occupancy['type'] == 'red')]['occupancy'].sum() if name != carpark_to_close else 0), capacity=max(1, CARPARK_CAPACITIES[name]['red'])),
            'white': simpy.Container(env, init=max(0, CARPARK_CAPACITIES[name]['white'] - initial_occupancy[(initial_occupancy['carpark'] == name) & (initial_occupancy['type'] == 'white')]['occupancy'].sum() if name != carpark_to_close else 0), capacity=max(1, CARPARK_CAPACITIES[name]['white']))
        } for name in CARPARK_NAMES
    }

    env.process(record_hourly_occupancy(env, carpark_to_view))

    for index, row in initial_occupancy.iterrows():
        carpark = row['carpark']
        car_type = row['type']
        occupancy = row['occupancy']
        # Update the initial level of the carpark
        if carpark == carpark_to_close:
            carpark = find_nearest_carpark(carpark, car_type)

        if carpark and occupancy > 0:
            car_parks[carpark][car_type].get(occupancy)
            # Start process for each initially parked car
            env.process(handle_initial_cars(env, carpark, car_type, occupancy))

    hourly_occupancy = {name: {'red': [], 'white': []} for name in CARPARK_NAMES}

    env.process(event_simulation(env, event_carpark, expected_cars, event_start, event_end))

    # Adding cars to the simulation if car_info_df is not empty
    if len(car_info_df) > 0:
        for index, row in car_info_df.iterrows():
            env.process(car_process(env, row))

    # Running the simulation
    env.run(until=simulation_duration + 1) # +1 to ensure info on the last hour is recorded

    # Calculate hourly average occupancy
    hourly_avg_occupancy = {'red': [], 'white': []}
    for hour in range(len(hourly_occupancy[carpark_to_view]['red'])):
        hourly_avg_occupancy['red'].append(hourly_occupancy[carpark_to_view]['red'][hour])
        hourly_avg_occupancy['white'].append(hourly_occupancy[carpark_to_view]['white'][hour])

    rounded_hourly_avg_occupancy = {
        'red': [round(value) for value in hourly_avg_occupancy['red']],
        'white': [round(value) for value in hourly_avg_occupancy['white']]
    }
    if carpark_to_close == carpark_to_view:
        # minus 1 to account for the initial occupancy
        red_list = [max(0, value - 1) for value in rounded_hourly_avg_occupancy['red']]
        white_list = [max(0, value - 1) for value in rounded_hourly_avg_occupancy['white']]
    else:
        red_list = rounded_hourly_avg_occupancy['red']
        white_list = rounded_hourly_avg_occupancy['white']
    return red_list,white_list

""" print(run_simulation(data1))
print(run_simulation(data2))
print(run_simulation(data3))
print(run_simulation(data4))
print(run_simulation(data5))
print(run_simulation(data6))
print(run_simulation(data7))
print(run_simulation(data8)) """