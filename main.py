import csv
import pandas as pd
import re
from datetime import datetime, timedelta
from utils.shift_utils import extract_month_number, get_shift_times
from calendar_service.cal_setup import get_calendar_service


def read_raw_data(filename):
    """
    opens the csv file and reads the raw data
    :param filename: file name
    :type filename: str
    :returns: list of 1/2/3/4 which means Morning/Evening/Night/Day off shift
    :rtype: list
    """

    shifts_converted = []

    with open(filename, 'r') as csv_file:
        # creating a csv reader object
        csv_reader = csv.reader(csv_file)

        # extracting field names through first row (there is a dummy field ('placeholder') for eliminate trimming the sheet, when there are no values in the first rows)
        next(csv_reader)

        for row in csv_reader:
            if 'x' in row[0]:
                shifts_converted.append("Morning Shift")
                continue
            elif 'x' in row[1]:
                shifts_converted.append("Evening Shift")
                continue
            elif 'x' in row[2]:
                shifts_converted.append("Night Shift")
                continue
            else:
                shifts_converted.append("Day off")
                continue

        # print(shifts_converted)
        return shifts_converted

        # print("length of shifts_converted: {}".format(len(shifts_converted)))


def get_date_range(filename):
    """
    By the name of the file, the function determines what is the date range of the given shifts
    :param filename: file name
    :type filename: str
    :returns: date range
    :rtype: str
    """
    # set the start_date
    # init today in order to init current year
    today = pd.Timestamp.now()
    start_date_year = today.year
    start_date_month = extract_month_number(filename)
    start_date = pd.Timestamp(year=start_date_year,
                              month=start_date_month, day=16)

    # init the end_date
    end_date_month = start_date_month
    end_date_year = start_date_year

    # check if month is 12. if it does, set the next month to 1, and year to 2024
    if start_date_month == 12:
        end_date_month = 1
        end_date_year = today.year + 1
    else:
        end_date_month = start_date_month+1

    # set the end_date
    end_date = pd.Timestamp(
        year=end_date_year, month=end_date_month,  day=15)

    # date_range = pd.date_range(start_date, end_date).strftime("%m/%d/%Y")
    date_range = pd.date_range(start_date, end_date).strftime("%Y-%m-%d")
    # print(f'date_range: {start_date} to {end_date}')

    return date_range


def add_1_day_delta(date):
    """
    A function that gets a date string, and returns the next day.
    :param date: A date 
    :type date: str
    :returns: the next day
    :rtype: str
    """
    # convert the string to a datetime object
    date = datetime.strptime(date, "%Y-%m-%d")

    # add one day using timedelta
    date_delta = date + timedelta(days=1)

    # parse back to string format
    date_delta_str = date_delta.strftime("%Y-%m-%d")

    return date_delta_str


def init_shifts_data(shifts, filename):
    """
    A function that adds to the shifts additional data required by Google Calendar:
    start date + end date (for 'all-day event')
    :param shifts: list of events summaries(aka Title of the event)
    :param filename: file name - relevant for the date range determination
    :type date: list
    :type filename: str
    :returns: new list that holds dicts each event data in a dict
    :rtype: list of dicts
    """
    shifts_data = []

    date_range = get_date_range(filename)

    shifts_itr = 0
    for single_date in date_range:
        single_date_plus_delta = add_1_day_delta(single_date)

        shifts_data.append(
            {"summary": shifts[shifts_itr], "start": single_date, "end": single_date_plus_delta})
        # print(shifts_data)
        shifts_itr += 1

    return shifts_data


def create_events_from_list(shifts):
    """
    The practical part of creating the events in Google calendar
    :param shifts: the full data of the shifts to be inserted in the calendar
    :type shifts: list of dicts
    :returns: whether the action succeeded.
    :rtype: int
    """
    service = get_calendar_service()

    # for testing purpose - cut shifts[] to include only one event.
    # shifts_lst = []
    # shifts_lst.append(shifts[0])

    for shift in shifts:
        # print(type(shift))
        print(shift['summary'], shift['start'], shift['end'])

        summary = shift['summary']
        start = shift['start']
        end = shift['end']

        try:
            event_result = service.events().insert(calendarId='primary',
                                                   body={
                                                       "summary": summary,
                                                       "start": {"date": start},
                                                       "end": {"date": end}
                                                   }).execute()

            print("created event")
            print("id: ", event_result['id'])
            print("summary: ", event_result['summary'])
            print("starts at: ", event_result['start']['date'])
            print("ends at: ", event_result['end']['date'])

        except Exception as e:
            print(f'An error occurred: {e}')
            print(f'last event tried to insert: {shift}')
            return 0  # return 0 if an error occurred

    return 1  # return 1 if an error occurred


def populate_fields(filename):
    """
    populating the fields of the csv file 
    :param filename: file name
    :type filename: str
    :returns: None
    :rtype: None
    """

    # field names
    fields = ['Subject', 'Start Date', 'Start Time', ' End Date',
              'End Time', 'All Day Event', 'Description', 'Location', 'Private']

    # writing to csv file
    with open(filename, 'w', newline='') as csv_file:
        # creating a csv writer object
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(fields)


def populate_rows(shifts, filename):
    """
    populating the rows of the csv file
    :param filename: file name
    :param shifts: list of the order of the shifts
    :type filename: str
    :type shifts: list
    :returns: None
    :rtype: None
    """

    # Remember that if the last rows doesnt have value(should be Day-off), I have to force-populate it until the 15/MM (maybe with a condition that do not stop until the date is 15*)

    # set the start_date
    # init today in order to init current year
    today = pd.Timestamp.now()
    start_date_year = today.year
    start_date_month = extract_month_number(filename)
    start_date = pd.Timestamp(year=start_date_year,
                              month=start_date_month, day=16)

    # init the end_date
    end_date_month = start_date_month
    end_date_year = start_date_year

    # check if month is 12. if it does, set the next month to 1, and year to 2024
    if start_date_month == 12:
        end_date_month = 1
        end_date_year = today.year + 1

    # set the end_date
    end_date = pd.Timestamp(
        year=end_date_year, month=end_date_month,  day=15)

    date_range = pd.date_range(start_date, end_date).strftime("%m/%d/%Y")

    # writing to csv file
    with open(filename, 'a', newline='') as csv_file:
        # creating a csv writer object
        csv_writer = csv.writer(csv_file)

        shift_itr = 0
        for single_date in date_range:
            try:
                # get start_time + end_time by the shift's type(Morning, Evening, etc.)
                start_time, end_time = get_shift_times(shifts[shift_itr])

                csv_writer.writerow(
                    [shifts[shift_itr], single_date, start_time, single_date, end_time, "TRUE"])
                shift_itr += 1
            except Exception as e:
                print(
                    f"An unexcpeted error occurred: {e}. date_range length is {len(date_range)} and shifts length is {len(shifts)}")
                break


def main():
    # original csv file name
    filename = ("January shifts.csv")
    shifts = read_raw_data(filename)

    shifts = init_shifts_data(shifts, filename)
    result = create_events_from_list(shifts)
    print(result)

    # create new file
    # new_filename = re.match(r'(\w+\s?\w+)', filename).group(1)
    # new_filename = (f'{new_filename}_new.csv')

    # populate_fields(new_filename)

    # populate_rows(shifts, new_filename)


main()


# steps CSV method:
# 1. read all the 'x' from the original file - to a list and parse it to Morning/Evening/Night/Day-off
# 2. create a new file ('{filename}_new.csv')
# 3. write the fixed fields
# 4. format the columns in a for loop:
#   a. shift type
#   b. date
#   c. Start time
#   d. date
#   e. End time
#   f. All day event
#   (note that for each iteration, the day must ++)

# steps for creating events via direct API :
# 1. read all the 'x' from the original file - to a list and parse it to Morning/Evening/Night/Day-off
# 2. create a dictionary that holds the following keys: subject, summary, start, end
# 3. create the evenets with calling the calendar service
