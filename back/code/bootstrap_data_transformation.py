import numpy as np
import pandas as pd
import math
import itertools
from datetime import datetime, timedelta, date
## Helper Functions
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

data = pd.read_csv('../data/max_occupancy_hour_final.csv')
data.rename(columns={'staff': 'red'}, inplace=True)
data['white'] = data['total_occupied'] - data['red']
data['enter'] = pd.to_datetime(data['date'] + ' ' + data['hour'].astype(str) + ':00:00')
data['period'] = data.apply(lambda row: label_period(row), axis=1)
day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
data['day_of_week'] = data['enter'].dt.dayofweek.apply(lambda x: day_names[x])
data = data[['day_of_week', 'period', 'carpark', 'hour', 'red', 'white']]
data.to_csv('../data/bootstrap_occupancy_data.csv', index=False)