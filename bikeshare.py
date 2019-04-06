import json
import time

import numpy as np
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    city = input('Give city name (Chicago, New York City, or Washington): ').lower()
    while CITY_DATA.get(city) is None:
        city = input('Give city name (Chicago, New York City, or Washington): ').lower()
        if not city:
            print("Sorry, that didn't work. Please try again by typing Chicago, New York City, or Washington: ")
    # get user input for month (all, january, february, ... , june)
    months_allowed = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = input('Give the month (January through June or type all): ').lower()
    while month not in months_allowed:
        month = input('Give the month of January, February, March, April, May, June, or all: ')
        if not month:
            print("Sorry, that didn't work. Please try a month January, February, March, April, May, June, or all.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days_allowed = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    day = input('Give the day of the week or type all: ').lower()
    while day not in days_allowed:
        day = input('Give the day of the week Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all: ')
        if not day:
            print("Sorry, that didn't work. Please try a day of the week Monday, Tuesday, Wednesday, Thursday, Friday, or all.")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('\nThe most common month is (1=January...6=June):\n', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('\nThe most common day of the week is:\n', popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('\nThe most common start hour is:\n', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().nlargest(1)
    print('\nThe most common start station is:\n', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().nlargest(1)
    print('\nThe most popular end station is:\n', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_station_combo =  df.groupby(['Start Station'])['End Station'].value_counts().nlargest(1)
    # df.groupby(['Start Station'],['End Station']).value_counts().nlargest(1)
    print('\nThe most frequent combination of start and end station is:\n', popular_station_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time_hours = (df['Trip Duration'].sum()) / 3600
    print('\nThe total travel time in hours is:\n', travel_time_hours)

    # display mean travel time
    mean_travel_time = (df['Trip Duration'].mean()) / 60
    print('\nThe mean travel time in minutes is:\n', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('\nThe count for each user type is:\n', user_type_count)

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('\nThe count for each gender is:\n', gender_count)
    except KeyError:
        print('\nNo gender data.')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birthyear = df['Birth Year'].min()
        youngest = df['Birth Year'].max()
        popular_birthyear = df['Birth Year'].mode()[0]
        print('\nThe oldest users were born in {},\nthe youngest were born in {},\nand the most common birth year is {}'.format(int(earliest_birthyear), int(youngest), int(popular_birthyear)))
    except KeyError:
         print('\nNo Birth Year data.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_data(df):
    """Displays Data from user filter."""
    more = input('\nWould you like to see five rows of the data? Enter yes or no.\n')
    d=0
    while more == "yes":
        print(df.iloc[[d, d+1, d+2, d+3, d+4]])
        d=d+5
        more = input('\nWould you like to see five rows of the data? Enter yes or no.\n')
    else:
        print("Ok, moving on.")
    return()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
if __name__ == "__main__":
	main()
