import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

VALID_CITIES = {'chicago', 'new york city', 'washington'}

VALID_MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

VALID_DAYS = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
              'saturday', 'sunday', 'all'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("\n")
    print("#" * 54)
    print('### WELCOME TO US BIKESHARE DATA ANALYSIS PROGRAM! ###')
    print("#" * 54)
    print("\n")

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Enter the name of the city to analyze (chicago, new york city, or washington)\n").lower()
        if city in VALID_CITIES:
            break
        else:
            print("Sorry, the input does not contain any of the valid cities.\nPlease try again!")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            "Enter the name of the month (from January to June) to filter by, or \"all\" to apply no month filter\n").lower()
        if month in VALID_MONTHS:
            break
        else:
            print("Sorry, the input does not contain any of the valid month names.\nPlease try again!")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter the name of the day of week to filter by, or \"all\" to apply no day filter\n").lower()
        if day in VALID_DAYS:
            break
        else:
            print("Sorry, the input does not contain any of the valid day names.\nPlease try again!")

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
    common_month = df['month'].mode()[0]
    common_month_name = VALID_MONTHS[common_month - 1].title()
    print("The most common month is {}".format(common_month_name))

    # display the most common day of week
    print("The most common day of week is {}".format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    common_hour = df['Start Time'].dt.hour.mode()[0]
    print("The most common start time is {}".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is: {}".format(df["Start Station"].mode()[0]))

    # display most commonly used end station
    print("The most commonly used end station is: {}".format(df["End Station"].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['Start and End Station'] = df['Start Station'] + " AND " + df['End Station']
    print("The most frequent combination of start and end station is: {}".format(df['Start and End Station'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time_days = df["Trip Duration"].sum() / 86400
    print("Total travel time is {:0.2f} days".format(total_time_days))

    # display mean travel time
    mean_time_mins = df["Trip Duration"].mean() / 60
    print("Mean travel time is {:0.2f} minutes".format(mean_time_mins))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df["User Type"].value_counts()
    print("This the count of records for each user type:")
    for i in user_type_count.index:
        print("{}: {}".format(i, user_type_count[i]))

    # Display counts of gender (when applicable)
    if "Gender" in df.columns:
        gender_count = df["Gender"].value_counts()
        print("\nThis the count of records for each gender:")
        for i in gender_count.index:
            print("{}: {}".format(i, gender_count[i]))

    # Display earliest, most recent, and most common year of birth (when applicable)
    if "Birth Year" in df.columns:
        print("\nThis is some information regarding year of birth:")
        print("Earliest: {:0.0f}".format(df["Birth Year"].min()))
        print("Most recent: {:0.0f}".format(df["Birth Year"].max()))
        print("Most common: {:0.0f}".format(df["Birth Year"].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    """Displays raw data of database on screen."""

    view_data = input('\nWould you like to see the raw data? Enter yes or no.\n').lower()

    if view_data == 'yes':
        df_ordered_index = pd.DataFrame(df.values, index=range(0, df.index.size), columns=df.columns)
        df_index = 0

        while df_index < len(df_ordered_index):
            for item in range(df_index, df_index + 5):
                print('*' * 74)
                print(df_ordered_index.loc[item])
                print('*' * 74)

            view_next = input("Do you want to see the next 5 items? Enter yes or no.\n").lower()
            if view_next != 'yes':
                print("Exiting raw data function...")
                print('-' * 40)
                break
            else:
                df_index += 5
    else:
        print("Exiting raw data function...")
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

        restart = input('\nWould you like to restart the program? Enter yes or no.\n').lower()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
