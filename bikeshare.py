import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv'}

# make global scope variables to be used in any function i want:
# Project Cities:
Cities = ['chicago', 'new york city']
# Project Months:
Months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
# Project Weekdays:
Days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


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
    while True:
        city = input('Would you like to see data for chicago, new york city , or washington? \n> ')
        city = city.lower()
        if city in Cities:
            break
        else:
            print("invalid input. Please enter a valid input")
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('All right! Which month - January, February, March, April, May, or June?'
                      ' or just say \'all\' to apply no month filter. \n> ')
        month = month.lower()
        if month in Months:
            break
        else:
            print("invalid input. Please enter a valid input")

        # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('All right! Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?'
                    'or just say \'all\' to apply no day filter. \n> ')
        day = day.lower()
        if day in Days:
            break
        else:
            print("invalid input. Please enter a valid input")


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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Same as Practice Problem #3: Load and Filter the Dataset
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month

    '''
        df['day_of_the_week'] = df['Start Time'].dt.weekday_name
        AttributeError: 'DatetimeProperties' object has no attribute 'weekday_name'
        Resolved
        https://stackoverflow.com/questions/60339049/weekday-name-from-a-pandas-dataframe-date-object?answertab=votes#tab-top
        _/ weekday_name to day_name() _/
    '''

    df['week_day'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = Months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['week_day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most Frequent Month is :', common_month)
    # display the most common day of week
    common_week_day = df['week_day'].mode()[0]
    print('Most Frequent Day is :', common_week_day)
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour is :', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    most_commonly_start_stat = df['Start Station'].mode()[0]
    print('Most Commonly used Start Station is :', most_commonly_start_stat)
    # display most commonly used end station
    most_commonly_end_stat = df['End Station'].mode()[0]
    print('Most Commonly used End Station is :', most_commonly_end_stat)
    # display most frequent combination of start station and end station trip
    '''
      File "F: lib\site-packages\pandas\core\indexes\base.py", line 3363, in get_loc
    raise KeyError(key) from err
    KeyError: ('Start Station', 'End Station')
    Resolved
    _/ instead of [0] use .loc[0] _/
    '''
    commonly_start_to_end_stat = df[['Start Station', 'End Station']].mode().loc[0]
    print('Most Frequent Combination of Start Station and End Station trip : {}, {}'
          .format(commonly_start_to_end_stat[0], commonly_start_to_end_stat[1]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total Travel Time : ', total_time)
    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Mean Travel Time : ', mean_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    # Display counts of gender
    while True:
        if 'Gender' in df.columns or 'Birth Year' in df.columns:
            gender_types = df['Gender'].value_counts()
            print(gender_types)
            # Display earliest, most recent, and most common year of birth:
            birth_year = df['Birth Year']
            # the most common birth year
            common_year = birth_year.mode()[0]
            print("The most common birth year:", common_year)
            # the most recent birth year
            most_recent = birth_year.max()
            print("The most recent birth year:", most_recent)
            # the most earliest birth year
            earliest_year = birth_year.min()
            print("The most earliest birth year:", earliest_year)
            break
        else:
            print('Gender Stats can\'t be determined')
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    print('\nCalculating Raw Data Stats...\n')
    start_time = time.time()
    x = 0
    while True:
        raw = input('Do you like to see example from the raw Data, if you want type \'yes\' if else type \'no\' \n>')
        raw = raw.lower()
        if raw != 'yes':
            print('Thank you for Exploring US BikeShare')
            break
        else:
            x = x + 5
            print(df.iloc[x: x + 5])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
