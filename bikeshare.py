import time
import pandas as pd
import numpy as np

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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True :
        city = input('\nWould you like to see data for Chicago, New York City, or Washington?\n').lower().strip()
        if city in CITY_DATA.keys():
          break
        else:
          print(city ," Is not a valid input please try again")

    # TO DO: get user input for month (all, january, february, ... , june)
    while True :
        month = input("\nWhich month - January, February, March, April, May, or June? (Type 'all' if you want to show data for all the months)\n").lower().strip()
        if month in ['january' , 'february' , 'march' , 'april' , 'may' , 'june', 'all']:
          break
        else:
          print(month ," Is not a valid input please try again")


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True :
        day = input("\nWhich day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? (Type 'all' if you want to show data for all the days)\n").lower().strip()
        if day in ['monday' , 'tuesday' , 'wednesday' , 'thursday' , 'friday', 'saturday' , 'sunday' , 'all']:
          break
        else:
          print(day ," Is not a valid input please try again")

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

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
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # TO DO: display the most common month
    # extract month from the Start Time column to create an month column
    df['month'] = df['Start Time'].dt.month
    # find the most popular month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start month:', popular_month)

    # TO DO: display the most common day of week
    # extract week from the Start Time column to create an week column
    df['week'] = df['Start Time'].dt.week
    # find the most popular week
    popular_week = df['week'].mode()[0]
    print('Most Popular Start week:', popular_week)

    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("\nThe most commonly used start station is: '{}'".format(most_common_start_station))

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("\nThe most commonly used end station is: '{}'".format(most_common_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    most_common_combination = (df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    print("\nThe most frequent combination of start station and end station is: '{}'".format(most_common_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = (df['Trip Duration'].sum())
    total_travel_time = pd.to_timedelta(total_travel_time, unit='s')
    print('\nThe total travel time is: {} (#Days HH:MM:SS)\n'.format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = (df['Trip Duration'].mean())
    mean_travel_time = pd.to_timedelta(mean_travel_time, unit='s')
    print('\nThe mean travel time is: {} (#Days HH:MM:SS)\n'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    # print value counts for each user type
    user_types = df['User Type'].value_counts()
    print('\nCounts per user type:\n',user_types.to_string())

    # TO DO: Display counts of gender
    try:
        genders = df['Gender'].value_counts()
        print('\nCounts per gender:\n',genders.to_string())
    except KeyError:
        print("Gender information is not available for {}".format(city).title())


    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_yob = df['Birth Year'].min().astype("Int32")
        most_recent_yob = df['Birth Year'].max().astype("Int32")
        most_common_yob = df['Birth Year'].mode()[0].astype("Int32")
        print('\nThe earliest year of birth is {},the most recent is {} and the most common is {}.'.format(earliest_yob,most_recent_yob,most_common_yob))
    except KeyError:
        print("Year of birth information is not available for {}".format(city).title())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
       """Generates 5 rows of raw data based on the user input"""
       view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
       start_loc = 0
       while (view_data.lower() != "yes" and view_data != "no"):
            print("Thats not a valid input , please enter 'yes' or 'no'\n")
            view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
       while view_data == "yes":
            print(df.iloc[start_loc:(start_loc + 6)])
            start_loc += 5
            view_data = input("Do you wish to view 5 more rows ?: \n").lower()
       if view_data == "no":
        print('\nNo more rows will be printed!\n')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('\n Thank you & Good bye!!')
            break


if __name__ == "__main__":
	main()
