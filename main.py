import csv
import pandas as pd
import re
from utils.shift_utils import extract_month_number, get_shift_times


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
    filename = ("December shifts.csv")
    shifts = read_raw_data(filename)

    # create new file
    new_filename = re.match(r'(\w+\s?\w+)', filename).group(1)
    new_filename = (f'{new_filename}_new.csv')

    populate_fields(new_filename)

    populate_rows(shifts, new_filename)


main()


# steps:
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
