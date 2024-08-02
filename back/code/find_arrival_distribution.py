import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from sklearn.mixture import GaussianMixture
from datetime import datetime, date, time, timedelta
import warnings
warnings.filterwarnings(action="ignore")
data = pd.read_csv('../data/cleaned_data.csv')
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
data['enter'] = pd.to_datetime(data['enter'])
data['day_of_week'] = data['enter'].dt.dayofweek
data['period'] = data.apply(lambda row: label_period(row), axis=1)
data['duration'] = data['duration'].astype(int)
data['enter_hour'] = data['enter'].dt.hour
data['date'] = data['enter'].dt.date
data = data[['type', 'carpark', 'period', 'day_of_week', 'enter_hour', 'date']]
# if the car type is staff, change it to red, if it is not, change it to white
data['type'] = data['type'].apply(lambda x: 'red' if x == 'staff' else 'white')
# group by type, carpark, period, day_of_week, enter_hour
data = data.groupby(['type', 'carpark', 'period', 'day_of_week', 'date']).size().reset_index(name='counts')
median_counts = data['counts'].median()
std_dev_counts = data['counts'].std()
value_2sd_above_median = median_counts + 2 * std_dev_counts
grouped = data.groupby(['type', 'carpark', 'period', 'day_of_week'])
results = []

# Fit GMMs and select the best model using BIC
for name, group in grouped:
    lowest_bic = np.inf
    best_gmm = None

    # Reshape data for GMM fitting
    X = group['counts'].values.reshape(-1, 1)
    n_samples = X.shape[0]

    # Ensure the number of components does not exceed the number of samples
    max_components = min(n_samples, 6)

    for n_components in range(1, max_components + 1):
        gmm = GaussianMixture(n_components=n_components)
        gmm.fit(X)
        bic = gmm.bic(X)

        if bic < lowest_bic:
            lowest_bic = bic
            best_gmm = gmm

    # Store the results
    results.append({
        'type': name[0],
        'carpark': name[1],
        'period': name[2],
        'day_of_week': name[3],
        'Means': best_gmm.means_.flatten().tolist(),
        'Covariances': best_gmm.covariances_.flatten().tolist(),
        'Weights': best_gmm.weights_.flatten().tolist()
    })
results_df = pd.DataFrame(results)
results_df.to_csv('../data/gmm_arrival_info.csv', index=False)