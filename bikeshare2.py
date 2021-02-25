#import time and calendar library
import time
import calendar
#importing pandas
import pandas as pd
#importing numpy
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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # \n and colors used to break up inputs visually
    city = input('Would you like to see data for Chicago, New York City, or Washington?  \nPlease enter the city name exactly as shown.').title()
    while city not in ('Chicago','New York City','Washington'):
        city = input('\nOops! That city isn\'t valid. \nPlease enter the city of Chicago, New York City, or Washington.').title()
    print('\033[0;37;44m Great!  You\'ve selected ' + city)

    #Pop up an iconic image of the selected city
    from PIL import Image
    image_path = city + '.png'
    #read the image
    im = Image.open(image_path)
    #show image
    im.show()

    # get user input for month (all, january, february, ... , june)
    # \n and colors used to break up inputs visually
    month = input('\nPlease select a month for analyis: \nJanuary, February, March, April, May, June or All if you want to use all months.  \nPlease enter exactly as shown.').title()
    while month not in ('January','February','March','April','May','June','All'):
        month = input('\nNot so fast!  That answer won\'t work.  \nPlease input January, February, March, April, May, June or All.').title()
    if month == 'All':
        print('\033[0;37;44m You\'ve chosen All months.  That\'s a lot of cycling!')
    else:
         print('\033[0;37;44m You\'ve chosen the month of ' + month)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    # \n and colors used to break up inputs visually
    day = input('\nPlease select a day of the week for analyis: \nSunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or All if you want to use all days of the week.  \nPlease enter exactly as shown.').title()
    while day not in ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','All'):
        day = input('\nLet\'s try that again!  That answer won\'t work.  \nPlease input Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or All.').title()
    if day == 'All':
        print('\033[0;37;44m You\'ve chosen All days of the week.  No rest for the weary!')
    else:
         print('\033[0;37;44m You\'ve chosen the day of ' + day)

    #escape code reverts color back to normal
    print('\033[0m -'*40)

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
    #CREATE A function that only opens 1 file
    #replace any spaces with underscores to match new_york_city file name.
    city2 = city.replace(" ", "_")
    #specifies filename based upon city chosen
    city_path = city2 + '.csv'
    #creates unfiltered DataFrame for chosen city
    df = pd.read_csv(city_path)
    #convert start/end time column strings to dates
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    #extract month and hour from Start Time column to create a Month and Start Hour column
    df['Month'] = df['Start Time'].dt.month
    df['Start Hour'] = df['Start Time'].dt.hour
    #extract day of the week from Start Time column to create a Day of Week column
    df['Day_of_Week'] = df['Start Time'].dt.day_name()

    #create filters based on user inputs
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January','February','March','April','May','June']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['Month'] == month]
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['Day_of_Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['Month'].mode() [0]
    common_month_name = calendar.month_name[common_month]
    print('\nThe most common month of cycling is: ', common_month_name)

    # display the most common day of week
    common_day = df['Day_of_Week'].mode() [0]
    print('\nThe most common day for cycling is: ', common_day)

    # display the most common start hour
    common_hour = df['Start Hour'].mode() [0]
    print('\nThe most common start hour for a ride is: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode() [0]
    print('\nThe most frequently used start station is: ', common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode() [0]
    print('\nPeople most commonly ended their trip at: ', common_end)

    # display most frequent combination of start station and end station trip
    # creat a column combining the Start Station and End Station
    df['Start Finish'] = df['Start Station'] + ' | ' + df['End Station']
    common_combo = df['Start Finish'].mode() [0]
    print('\nThe most frequent starting and ending station is: ', common_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum(skipna = True)
    #convert seconds into min/sec
    converted_total_time = total_time / 60
    print('\nThe total travel time for the specified city, month, and day is (in min/sec): ', converted_total_time)

    # display mean travel time
    trip_avg_time = df['Trip Duration'].mean()
    #convert seconds into min/sec
    converted_trip_avg_time = trip_avg_time / 60
    print('\nThe average trip duration for the specified city, month, and day is (in min/sec): ', converted_trip_avg_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    df.dropna(subset=['User Type'])
    user_types = df['User Type'].value_counts()
    print('\nThe User Type counts are: \n', user_types)

    #Check to see if Gender column exists (missing for Washington csv file)
    if 'Gender' in df.columns:
        # Display counts of gender
        df.dropna(subset=['Gender'])
        genders = df['Gender'].value_counts()
        print('\nThe Gender counts are: \n', genders)


    #Check to see if Birth Year column exists (missing for Washington csv file)
    if 'Birth Year' in df.columns:
        #Display earliest, most recent, and most common year of birth
        #Remove nan and convert to int to remove decimal point
        df.dropna(subset=['Birth Year'])
        birth_earliest = int(df['Birth Year'].min())
        birth_latest = int(df['Birth Year'].max())
        birth_most = int(df['Birth Year'].mode() [0])
        print('\nThe earliest birth year of a rider is : ', birth_earliest)
        print('\nThe most recent birth year of a rider is : ', birth_latest)
        print('\nThe most common birth year of a rider is : ', birth_most)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no.\n').lower()
    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_data = input('Do you wish to see 5 more rows of data? Enter yes or no').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        user_stats(df)
        station_stats(df)
        time_stats(df)
        trip_duration_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
