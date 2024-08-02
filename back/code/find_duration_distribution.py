import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.mixture import GaussianMixture
import warnings
from datetime import datetime, date, time, timedelta
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
data = data[['type', 'duration', 'period', 'day_of_week']]
group_definitions = {
    'Red': {
        'School': [('Monday', 'Tuesday', 'Wednesday', 'Thursday'), ('Friday',), ('Saturday', 'Sunday')],
        'Holiday': [('Monday', 'Tuesday', 'Wednesday', 'Thursday'), ('Friday',), ('Saturday', 'Sunday')],
        'Exam': [tuple(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])]
    },
    'White': {
        'School': [('Monday',), ('Sunday',), ('Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')],
        'Holiday': [('Friday',), ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Saturday', 'Sunday')],
        'Exam': [('Monday', 'Tuesday',), ('Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')]
    }
}
def fit_best_gmm(data, group_color, period, days_tuple):
    filtered_data = data[(data['type'] != 'staff') if group_color == 'White' else (data['type'] == 'staff')]
    filtered_data = filtered_data[filtered_data['period'] == period]
    filtered_data = filtered_data[filtered_data['day_of_week'].isin(days_tuple)]
    
    duration = filtered_data['duration']
    median_duration = duration.median()
    std_deviation = duration.std()
    cutoff = median_duration + 2 * std_deviation
    filtered_duration = duration[duration <= cutoff].values.reshape(-1, 1)
    
    lowest_bic = np.infty
    bic = []
    n_components_range = range(1, 6)
    best_gmm = None
    
    for n_components in n_components_range:
        gmm = GaussianMixture(n_components=n_components, random_state=42)
        gmm.fit(filtered_duration)
        bic.append(gmm.bic(filtered_duration))
        
        if bic[-1] < lowest_bic:
            lowest_bic = bic[-1]
            best_gmm = gmm
    
    return best_gmm, filtered_duration
gmm_info_df = pd.DataFrame(columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'School', 'Holiday', 'Exam', 'Means', 'Covariances', 'Weights'])
for group_color, periods in group_definitions.items():
    for period, days_tuples in periods.items():
        for days_tuple in days_tuples:
            gmm, filtered_duration = fit_best_gmm(data, group_color, period, days_tuple)
            gmm_row = {
                'Monday': 'Monday' in days_tuple,
                'Tuesday': 'Tuesday' in days_tuple,
                'Wednesday': 'Wednesday' in days_tuple,
                'Thursday': 'Thursday' in days_tuple,
                'Friday': 'Friday' in days_tuple,
                'Saturday': 'Saturday' in days_tuple,
                'Sunday': 'Sunday' in days_tuple,
                'School': period == 'School',
                'Holiday': period == 'Holiday',
                'Exam': period == 'Exam',
                'Means': gmm.means_.flatten().tolist(),
                'Covariances': gmm.covariances_.flatten().tolist(),
                'Weights': gmm.weights_.flatten().tolist()
            }
            gmm_info_df = pd.concat([gmm_info_df, pd.DataFrame([gmm_row])], ignore_index=True)
            
            plt.figure(figsize=(10, 6))
            sns.histplot(filtered_duration, bins=30, color='g', legend=False, stat='density')
            
            duration_range = np.linspace(filtered_duration.min(), filtered_duration.max(), num=100)
            logprob = gmm.score_samples(duration_range.reshape(-1, 1))
            density = np.exp(logprob)
            
            plt.plot(duration_range, density, '-', label='Fitted Distribution', color='r')
            
            plt.title(f'{group_color} Group - {period} Period - Days: {", ".join(days_tuple)}')
            plt.xlabel('Duration')
            plt.ylabel('Density')
            plt.legend()
            plt.show()
gmm_info_df.to_csv('../data/gmm_info.csv', index=False)