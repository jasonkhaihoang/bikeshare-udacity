import time
from datetime import timedelta
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june',
          'july', 'august', 'september', 'october', 'november', 'december', 'all']

WEEK_DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city not in CITY_DATA:
        city = input('Enter the city: ').lower()

    # get user input for month (all, january, february, ... , june)
    month = ''
    while month not in MONTHS:
        month = input('Enter the month: ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day not in WEEK_DAYS:
        day = input('Enter the day of week: ').lower()

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1
        print(month)
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new data frame
        df = df[df['day_of_week'] == day.title()]

    return df
    # example: df = load_data('chicago', 'march', 'friday')


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]  # find the most common month using mode
    print('Most Frequent Start Month:', popular_month)

    # display the most common day of week
    df['day'] = df['Start Time'].dt.weekday_name
    popular_day = df['day'].mode()[0]  # find the most common week day using mode
    print('Most Frequent Start Day:', popular_day)

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]  # find the most common hour using mode
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_stations = df['Start Station'].value_counts()
    popular_start_station = start_stations.idxmax()
    print('Most commonly used start station:{} with {} turns'.format(popular_start_station, start_stations.max()))

    # display most commonly used end station
    end_stations = df['End Station'].value_counts()
    popular_end_station = end_stations.idxmax()
    print('Most commonly used end station: {} with {} turns'.format(popular_end_station, end_stations.max()))
    
    # display most frequent combination of start station and end station trip
    combined_stations = df.groupby(['Start Station', 'End Station']).count()
    popular_combined_station = "{} and {}".format(combined_stations['Start Time'].idxmax()[0],
                                                  combined_stations['Start Time'].idxmax()[1])
    print('Most commonly used combined station: {} with {} turns'.format(popular_combined_station,
                                                                         combined_stations['Start Time'].max()))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-' * 40)
    
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = df['Trip Duration'].sum()  # in seconds
    print('Total Trip Duration: {:02} days {:02} hours {:02} minutes and {:02} seconds '.
          format(total_trip_duration//86400,            # days
                 total_trip_duration % 86400//3600,     # hours
                 total_trip_duration % 3600//60,        # minutes
                 total_trip_duration % 60))             # seconds

    # display mean travel time
    mean_trip_duration = df['Trip Duration'].mean()  # in seconds
    print('Average Trip Duration: {:02} days {:02} hours {:02} minutes and {:02} seconds '.
          format(mean_trip_duration//86400,            # days
                 mean_trip_duration % 86400//3600,     # hours
                 mean_trip_duration % 3600//60,        # minutes
                 mean_trip_duration % 60))             # seconds
    
    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # print value counts for each user type
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender

    # Display earliest, most recent, and most common year of birth

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        # user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
