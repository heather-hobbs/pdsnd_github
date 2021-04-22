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
    cities = ('chicago', 'new york city', 'washington')
    while True:
        city = input('Would you like to explore chicago, new york city, or washington? \n ').lower()
        if city not in cities:
            print('Please select a different city.')
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    months= ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input('Please select the month of interest. \n {} \n'.format(months)).lower()
        if month not in months:
            print("That is not included in this dataset. Please select a different month.")
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input('Please select the day of interest. \n {} \n'.format(days)).lower()
        if day not in days:
            print("That is not included in this dataset. Print select a different day.")
        else:
            break

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
    print(f"We are loading data for {city}, {month}, and {day}.")
    df = pd.read_csv(CITY_DATA[city])
    display_data(df)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extract month and day from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day'] = df['Start Time'].dt.day_name()

    if month == 'all' and day == 'all':
        return df

    month_filter = True
    day_filter = True

    #Filter the data by month and day if applicable using numpy where()
    if month != 'all':
        month_filter = (df['month'] == month.capitalize())
    if day != 'all':
        day_filter = (df['day'] == day.capitalize())

    filters = np.where((month_filter & day_filter))

    return df.loc[filters]

# Displaying 5 rows of raw data at a time based on the user's response
def display_data(df):
    index=0
    user_input=input('would you like to display 5 rows of raw data? ').lower()
    while user_input in ['yes','y','yep','yea'] and index+5 < df.shape[0]:
        print(df.iloc[index:index+5])
        index += 5
        user_input = input('would you like to display more 5 rows of raw data? ').lower()

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_popular_month = df['month'].mode()[0]
    print(f"The most popular month is {most_popular_month}")

    # TO DO: display the most common day of week
    most_popular_day = df['day'].mode()[0]
    print(f"The most popular day is {most_popular_day}")

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_popular_hour = df['hour'].mode()
    print(f"The most popular start hour is {(most_popular_hour.to_string(index=False, header=False))}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_popular_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is {most_popular_start_station}.")

    # TO DO: display most commonly used end station
    most_popular_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is {most_popular_end_station}.")

    # TO DO: display most frequent combination of start station and end station trip
    #I added the two strings together
    most_popular_start_end_station = (df['Start Station'] + df['End Station']).mode()
    print('The most commonly used start and end stations are', most_popular_start_end_station.to_string(index=False, header=False))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    trip_duration = df['Trip Duration'].sum()
    #Convert the current format of trip time (minutes) to h:m:s
    minute, second = divmod(trip_duration, 60)
    hour, minute = divmod(minute, 60)
    print(f"Total Travel Time: {hour}hr {minute}min {second}sec.")

    # TO DO: display mean travel time
    mean_travel = df['Trip Duration'].mean()
    #Convert the current format of trip time (minutes) to h:m:s
    minute, second = divmod(mean_travel, 60)
    hour, minute = divmod(minute, 60)
    print(f"Mean Travel Time: {hour}hr {minute}min {second}sec.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].value_counts()
    print(f"User Type: {user_type}")

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print(gender_count)
    else:
        print('No gender data to provide.')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_year = df['Birth Year']
        #earliest
        earliest_year = birth_year.min()
        print(f"The earliest birth year is {earliest_year}")

        #most recent
        most_recent_year = birth_year.max()
        print(f"The most recent birth year is {most_recent_year}")

        #most common
        most_common_year = birth_year.mode()
        print(f"The most common birth year is {most_common_year}")
    else:
        print('No birth year data to provide.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        # display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
