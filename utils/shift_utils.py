import re


def extract_month_number(filename):
    """
    A function that extracts the month number from the file name
    :param filename: the file name 
    :type filename: str
    :returns: the related month number (for example: for month: December, returns: 12)
    :rtype: int
    """
    # Define a mapping between month names and numbers
    month_mapping = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
                     'May': 5, 'June': 6, 'July': 7, 'August': 8,
                     'September': 9, 'October': 10, 'November': 11, 'December': 12}

    # Extract the first word of the file
    first_word = re.match(r'\b(\w+)\b', filename).group(1)

    # Convert the first word to title case and get the corresponding month number
    month_number = month_mapping.get(first_word.capitalize())

    return month_number
# move to utils folder


def get_shift_times(shift):
    """
    A function that gets fixed shift type and returns that proper start + end time of the shift
    :param shift: shift type(name)
    :type shift: str
    :returns: start time + end time of the shift
    :rtype: tuple
    """
    shift_times = {
        "Morning Shift": ("07:00 AM", "5:00 PM"),
        "Evening Shift": ("4:00 PM", "11:59 PM"),
        "Night Shift": ("11:00 PM", "08:00 AM"),
        "Day off": ("", ""),
    }

    # Default to ("", "") for unknown shift types
    return shift_times.get(shift, ("N", "N"))
