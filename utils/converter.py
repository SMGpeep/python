import re
import datetime
from timer import timer

@timer
def stringToDatetime(date_string: str) -> 'datetime.datetime':

    match = searchStringForEveryPossibleDateFormat_rx(date_string)
    if not match:
        raise ValueError(f"Date string '{date_string}' does not match any known format.")

    groups = match.groups()
    if len(groups[0]) == 4:
        year, month, day, hour, minute, second = map(int, groups)
    elif len(groups[2]) == 4:
        day, month, year, hour, minute, second = map(int, groups)
    else:
        day, month, year_short, hour, minute, second = map(int, groups)
        year = 2000 + year_short if year_short < 50 else 1900 + year_short

    return datetime.datetime(year, month, day, hour, minute, second)


def searchStringForYYYYMMdd_rx(string):
    # Regex pattern for year (4 digits), month (2 digits), day (2 digits), hour (2 digits), minute (2 digits), second (2 digits)
    # delimiter can be anything non-digit
    pattern = r"(\d{4})\D+(\d{2})\D+(\d{2})\D+(\d{2})\D+(\d{2})\D+(\d{2})"

    return re.match(pattern, string)

def searchStringForDDMMYYYY_rx(string):
    # Regex pattern for day (2 digits), month (2 digits), year (4 digits), hour (2 digits), minute (2 digits), second (2 digits)
    # delimiter can be anything non-digit
    pattern = r"(\d{2})\D+(\d{2})\D+(\d{4})\D+(\d{2})\D+(\d{2})\D+(\d{2})"

    return re.match(pattern, string)

def searchStringForDDMMYY_rx(string):
    # Regex pattern for day (2 digits), month (2 digits), year (2 digits), hour (2 digits), minute (2 digits), second (2 digits)
    # delimiter can be anything non-digit
    pattern = r"(\d{2})\D+(\d{2})\D+(\d{2})\D+(\d{2})\D+(\d{2})\D+(\d{2})"
    return re.match(pattern, string)

def searchStringForLongDate_rx(string):
    # Regex pattern for long date format with month name
    # Example: "05 October 2023 14:30:45"
    pattern = r"(\d{2})\s+([A-Za-z]+)\s+(\d{4})\s+(\d{2}):(\d{2}):(\d{2})"
    return re.match(pattern, string)

def searchStringForShortDate_rx(string):
    # Regex pattern for short date format with month name
    # Example: "5 Oct 23 14:30:45"
    pattern = r"(\d{1,2})\s+([A-Za-z]{3})\s+(\d{2})\s+(\d{2}):(\d{2}):(\d{2})"
    return re.match(pattern, string)

def searchStringForISODate_rx(string):
    # Regex pattern for ISO date format
    # Example: "2023-10-05T14:30:45"
    pattern = r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})"
    return re.match(pattern, string)



def searchStringForEveryPossibleDateFormat_rx(string):
    # Try different date formats
    match = searchStringForYYYYMMdd_rx(string)
    if match:
        return match

    match = searchStringForDDMMYYYY_rx(string)
    if match:
        return match

    match = searchStringForDDMMYY_rx(string)
    if match:
        return match

    return None


# Test cases
test_string_variations = [
    "2023-10-05 14:30:45",
    "05/10/2023 14:30:45",
    "05.10.23 14:30:45",
    "2023/10/05 14-30-45",
    "05-10-2023 14.30.45",
    "05 10 23 14 30 45",
    "2023.10.05-14:30:45",
    "   2023 10 05 14 30 45",
    "05-10-23-14-30-45   ",
]


if __name__ == "__main__":

    for test_string in test_string_variations:
        dt = stringToDatetime(test_string)
        print(f"Input string: {test_string} => Parsed datetime: {dt}")
