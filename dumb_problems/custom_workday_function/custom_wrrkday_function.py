"""
Date created: 03/08/2025
    
Purpose:
    
Details:
    
Description:
    
Notes:
   Implement a Custom Workday Function

        Objective: Write a function that calculates the date after a given number of working days (X), starting from a specified date. The function should exclude weekends (Saturday and Sunday) and any holidays provided as input.
        Requirements

            Input Parameters:

                start_date: The starting date (e.g., "2025-03-05").

                days: An integer representing the number of working days to add (can be positive or negative).

                holidays: A list of dates (e.g., ["2025-03-10", "2025-03-17"]) that should be excluded as non-working days.

            Output:

                Return the resulting date after adding the specified number of working days, excluding weekends and holidays.

            Rules:

                Weekends (Saturday and Sunday) are always non-working days.

                Holidays provided in the list should also be excluded from the calculation.

                If days is negative, calculate backward in time while respecting weekends and holidays. 
IMPORTANT NOTES:
    
Explanation:
    
Tags:
    
Contributors: 
    https://github.com/josephedradan
    
Reference:
    
"""
import re
import time
from collections import deque
from datetime import datetime, timedelta
from functools import wraps
from traceback import print_tb
from typing import Callable
from xml.etree.ElementTree import QName


def decorator_timer(_callable: Callable):

    @wraps(_callable)
    def wrapper(*args, **kwargs):
        time_start = time.perf_counter()
        result = _callable(*args, **kwargs)
        time_end = time.perf_counter()
        print(f" --- Runtime: {time_end - time_start}")
        return result

    return wrapper


@decorator_timer
def workday(start_date: str, days: int, holidays: list) -> datetime:
    """
    Calculates the Next available Workday starting from the variable "start_date" and skipping the amount of 
    days from the variable "days" and the variable "holidays".
        A Workday is a Weekday that is also not a Holiday from the variable "holidays".

    Notes:
        Time Complexity:
            O(n)
                Where n is the amount of days which includes Weekdays, Weekends, and Holidays
        
        Space Complexity:
            O(m*c)
                Where m is the size of the variable holidays
                Where c is an approximate constant for hashing                

        What this Algorithm does and uses:
            This algorithm does a While Loop over the days until the next available Workday is met.

            This algorithm uses:
                1. 1 While loop over the amount of days to skip
                    These days includes
                        weekdays
                        weekends
                        holidays
                2. Set (hash) over the the holidays
                3. 1 While loop to find the correct Workday

    Args:
        start_date (str): Starting day
        days (int): Weekdays to skip, these days do not include Weekends
        holidays (list): 

    Returns:
        datetime: _description_
    """
    datetime__date_current = datetime.fromisoformat(start_date)

    # Base Case for 0 Days given
    if days == 0:
        return datetime__date_current

    counter = abs(days)

    _set_datetime_holiday = set(datetime.fromisoformat(
        _date_holiday) for _date_holiday in holidays)

    # Loop based on the days decrementing until -1 because counter == 0 is still a day to skip
    while counter >= 0:
        datetime_date__date_next = (
            datetime__date_current +
            timedelta(days=1 if days >= 0 else -1)
        )

        # Check if current date is Saturday or Sunday
        if datetime__date_current.weekday() == 5 or datetime__date_current.weekday() == 6:
            datetime__date_current = datetime_date__date_next
            continue

        # _temp_escape = False
        # for _date_holiday in holidays:
        #     if _temp_escape == True:
        #         break
        #     if datetime__date_today == datetime.fromisoformat(_date_holiday):
        #         _temp_escape = True
        #         break

        # if _temp_escape:
        #     datetime__date_today = datetime_date__date_next
        #     continue

        # Check if current date is a holiday
        if datetime__date_current in _set_datetime_holiday:
            datetime__date_current = datetime_date__date_next
            continue

        counter -= 1
        datetime__date_current = datetime_date__date_next
        # print(counter)

    # Checking for a valid day to end on that is not a holiday or weekend (This is an Edge case)
    while True:
        datetime_date__date_next = (
            datetime__date_current +
            timedelta(days=1 if days >= 0 else -1)
        )

        # Check if current date is Saturday or Sunday
        if datetime__date_current.weekday() == 5 or datetime__date_current.weekday() == 6:
            datetime__date_current = datetime_date__date_next
            continue

        # Check if current date is a holiday
        if datetime__date_current in _set_datetime_holiday:
            datetime__date_current = datetime_date__date_next
            continue

        break

    return datetime__date_current


@decorator_timer
def workday_fast(start_date: str, amount_of_weekdays_to_skip: int, list_date_exclude: list) -> datetime:
    """
    Calculates the next available Workday after skipping amount_of_weekdays_to_skip and dates in list_date_exclude
        A Workday is a Weekday that is not a Weekend nor a Date to Exclude.
        A Date to Exclude is a Non Workday which can include Holidays.

    Notes:
        Time Complexity:
            O(1)
                If you think that the list of dates to exclude (list_date_exclude) would be considered negligible.
            O(m)
                Where m is the size of list of dates to exclude (list_date_exclude).
                If you think that the list of dates to exclude (list_date_exclude) is significant.

        Space Complexity:
            O(m)
                Where m is the size of list of dates to exclude (list_date_exclude).
                This algorithm only affects the order of the elements in list_date_exclude.

        What this Algorithm does and uses:
            This algorithm uses a mathematical and logical approach to calculate the next available Workday
            by calculating the total amount of Days to skip.
            The trick with this algorithm is that it treats Dates to Exclude that are Weekdays as additional
            Amount of Weekdays to skip.

            Note that Days to skip includes:
                Weekdays to skip
                Weekends to skip 
                Dates to exclude
                Days to skip that are caused by skipping Weekends and skipping Dates to exclude

            This algorithm uses:
                1. Math for figuring out dates 
                2. Logic for figuring out dates (This means that this solution is not a Pure math approach)
                3. 1 Loop over list_date_exclude executed once (Even through there is a recursive call)
                4. 1 Sorting call over list_date_exclude
                5. 1 Recursive call executed once 


    Args:
        start_date (str): _description_
        amount_of_weekdays_to_skip (int): _description_
        list_date_exclude (list): _description_

    Returns:
        datetime: The datetime object that represents 
    """    

    INDEX_WEEKDAY_MONDAY = 0

    amount_of_weekdays_to_skip_since_week_current_date_monday = 0

    print(f"{amount_of_weekdays_to_skip=}")

    datetime__date_current = datetime.fromisoformat(start_date)

    # Base Case for 0 Days given
    if amount_of_weekdays_to_skip == 0:
        return datetime__date_current

    """
    # ----- AMOUNT OF DAYS BETWEEN WEEK CURRENT DATE MONDAY AND DATE CURRENT
    Notes:
        Amount of days between the current week's Monday and the Current Date
        In other words it's the Difference between Monday and the Current Date

        The reason why we start on Monday:
            1. You can know how many days there are until a weekend happens (4 day from Monday or 5 days including Monday)
            2. There is a Floor Division trick when 
            
    """

    # .weekday() == 6 is Sunday, .weekday() == 5 is Saturday, .weekday() == 4 is Friday, ...
    amount_of_days_between_week_current_date_monday_and_date_current = (
        INDEX_WEEKDAY_MONDAY - datetime__date_current.weekday()
    )

    print(f"{amount_of_days_between_week_current_date_monday_and_date_current=}")

    """
    # ----- AMOUNT OF WEEKDAYS SINCE WEEK CURRENT DATE MONDAY
    Notes:
        Basically, instead of starting on Current Date we offset it to start
        on Current Week's Monday. This will make Math and logic easier
        since We know exactly when Saturday and Sunday will happen.
        It will allow us to create an equation to solve for how many
        Weekends (Saturdays and Sundays) have passed Given that we only
        skip Weekdays (Monday to Friday) 

    """

    amount_of_weekdays_to_skip_since_week_current_date_monday += (
        amount_of_weekdays_to_skip +
        (-1 * amount_of_days_between_week_current_date_monday_and_date_current)
    )

    print(f"{amount_of_weekdays_to_skip_since_week_current_date_monday=}")

    """
    # AMOUNT OF WEEKEND DAYS IN AMOUNT OF WEEKENDS PER AMOUNT OF WEEKDAYS TO SKIP SINCE WEEK CURRENT DATE MONDAY
    Notes:
        Go to the function docstring of the function call to under stand this

    """
    amount_of_weekend_days_in_amount_of_weekends_per_amount_of_weekdays_to_skip_since_week_current_date_monday = _get_amount_of_weekend_days_given_amount_of_weekdays_to_skip(
        amount_of_weekdays_to_skip_since_week_current_date_monday
    )

    """
    # ----- AMOUNT OF DAYS TO SKIP SINCE WEEK CURRENT DATE MONDAY
    Notes:
        (Amount of Days to skip since Current Week's Monday) = (
            (Amount of Weekdays to skip since Current Week's Monday) +
            (Amount of Weekend Days that have passed since Current Week's Monday)
        )
    """
    amount_of_days_to_skip_since_week_current_date_monday = (
        amount_of_weekdays_to_skip_since_week_current_date_monday +
        amount_of_weekend_days_in_amount_of_weekends_per_amount_of_weekdays_to_skip_since_week_current_date_monday

    )
    print(f"{amount_of_days_to_skip_since_week_current_date_monday=}")

    """
    # ----- HANDLING DATES TO EXCLUDE
    Notes:
        Now we have to deal with date to exclude which may include holidays.
        This portion of the code includes long portions of logic to figure out how
        these Dates to Exclude interact with (Amount of Days to skip since Current Week's Monday)

        Basically, Dates to Exclude that are Weekdays can we treated as Weekdays to skip because
        there is no distinction between a Weekday to Skip and a Weekday that is a Date to Exclude.
        

    """

    amount_of_weekdays_where_a_date_exclude_is_on_a_weekday_since_week_current_date_monday = 0

    """
    Dates to exclude must be sorted in ascending order to guarantee sequential dates. 
    The dates needs to be sequential because future Dates to Exclude affect other future Dates to Exclude
    as well as the last date to be skipped.
    """
    list_date_exclude_sorted = sorted(
        (
            datetime.fromisoformat(_date_exclude) for _date_exclude in list_date_exclude
        ),
        reverse=False if amount_of_weekdays_to_skip >= 0 else True  # Reverse the sort if we are calculating dates that haver already passed
    )
    print(f"{list_date_exclude_sorted=}")

    # Note that this loop is only ran once because on the recursive call list_date_exclude_sorted is empty
    for _datetime__date_exclude in list_date_exclude_sorted:
        _int_datetime_date_exclude_weekday = _datetime__date_exclude.weekday()

        # Skip Exclude Date that is Saturday or Sunday
        if _int_datetime_date_exclude_weekday == 5 or _int_datetime_date_exclude_weekday == 6:
            continue

        """
        # Temporary amount of weekdays to skip since the Current Week's Monday
        Notes:
            This variable is temporary because the variable
                amount_of_weekdays_where_a_date_exclude_is_on_a_weekday_since_week_current_date_monday
            may change due to the loop iteration 
        """
        _amount_of_weekdays_to_skip_since_week_current_date_monday__temp = (
            amount_of_weekdays_to_skip +
            (-1 * amount_of_days_between_week_current_date_monday_and_date_current) +
            # We must take in account the the value below because we account them as additional Weekdays to Skip
            amount_of_weekdays_where_a_date_exclude_is_on_a_weekday_since_week_current_date_monday
        )

        """
        # Temporary amount of Weekend Days to skip since the Current Week's Monday
        Notes:
            This variable is temporary because the variable
                amount_of_weekdays_where_a_date_exclude_is_on_a_weekday_since_week_current_date_monday
            may change due to the loop iteration
        """
        _amount_of_weekend_days_in_amount_of_weekends_per_amount_of_weekdays_to_skip_since_week_current_date_monday__temp = _get_amount_of_weekend_days_given_amount_of_weekdays_to_skip(
            _amount_of_weekdays_to_skip_since_week_current_date_monday__temp
        )
        """
        # Temporary amount of Days to skip since the Current Week's Monday
        Notes:
            This variable is temporary because the variable
                _amount_of_weekend_days_in_amount_of_weekends_per_amount_of_weekdays_to_skip_since_week_current_date_monday__temp
            may change due to the loop iteration
        """
        _amount_of_days_to_skip_since_week_current_date_monday__temp = (
            _amount_of_weekdays_to_skip_since_week_current_date_monday__temp +
            _amount_of_weekend_days_in_amount_of_weekends_per_amount_of_weekdays_to_skip_since_week_current_date_monday__temp
        )
        """
        # Temporary amount of Days to skip
        Notes:
            This variable is temporary because the variable
                _amount_of_days_to_skip_since_week_current_date_monday__temp
            may change due to the loop iteration
        """
        _amount_of_days_to_skip__temp = (
            _amount_of_days_to_skip_since_week_current_date_monday__temp +
            amount_of_days_between_week_current_date_monday_and_date_current +
            # The below is the Final Day skip because we have to skip the last workday
            (1 if amount_of_weekdays_to_skip >= 0 else -1)
        )

        # This date is the assumed last date because we don't know if it really will be the last day
        _datetime__date_last_assumed__temp = (
            datetime__date_current +
            timedelta(days=_amount_of_days_to_skip__temp)
        )

        # Corrected assumed last date (Basically we correct the date to a Weekday if it was a Weekend)
        _datetime__date_last_assumed_corrected__temp, amount_of_days_to_shift = _get_datetime__shift_weekend_to_weekday___and___offset(
            _datetime__date_last_assumed__temp,
            amount_of_weekdays_to_skip
        )

        print(_amount_of_days_to_skip__temp, _datetime__date_exclude,
              _datetime__date_last_assumed_corrected__temp, datetime__date_current)

        # If Amount of weekdays to skip goes forward in time
        if amount_of_weekdays_to_skip >= 0:

            # Skip Exclude Date that is less than the current date
            if _datetime__date_exclude < datetime__date_current:
                continue

            # If Exclude Date is less than or equal to the Date Last Assumed
            if _datetime__date_exclude <= _datetime__date_last_assumed_corrected__temp:
                amount_of_weekdays_where_a_date_exclude_is_on_a_weekday_since_week_current_date_monday += 1
                continue

        # If Amount of weekdays to skip goes backwards in time
        elif amount_of_weekdays_to_skip < 0:
            # Skip Exclude Date that is greater than the current date
            if _datetime__date_exclude > datetime__date_current:
                continue

            # If Exclude Date is greater than or equal to the Date Last Assumed
            if _datetime__date_exclude >= _datetime__date_last_assumed_corrected__temp:
                amount_of_weekdays_where_a_date_exclude_is_on_a_weekday_since_week_current_date_monday -= 1
                continue

    print(f"{amount_of_weekdays_where_a_date_exclude_is_on_a_weekday_since_week_current_date_monday=}")

    """
    # ----- AMOUNT OF WEEKDAYS TO SKIP CORRECTED
    Notes:
        This is the total amount of weekdays to skip which includes the given amount of weekdays to skip
        plus the Exclude Dates that are on weekdays that will happen. 
    """
    amount_of_weekdays_to_skip_corrected = (
        amount_of_weekdays_to_skip +
        amount_of_weekdays_where_a_date_exclude_is_on_a_weekday_since_week_current_date_monday
    )
    print(f"{amount_of_weekdays_to_skip_corrected=}")

    if list_date_exclude:

        """
        Notes:
            We do a recursive call here because we treat Dates to Exclude that are Weekdays
            as Weekdays to Skip because they are essentially they are the something.

            Notice that the last argument to the function call is an Empty list because
            we do not need to work on Dates to Exclude because they are already handled
            in this function call.
        """

        print("###### RESURIVE CALL #####")
        return workday_fast(
            start_date,
            amount_of_weekdays_to_skip_corrected,
            []
        )

    """
    # ---------- Note that below code is never called if the above function call and return is called ----------
    Notes:
        Basically, only the recursive call executes the below call, the caller function that called the 
        recursive call will not execute the code below. 

    """
    """
    # ----- AMOUNT OF DAYS TO SKIP CORRECTED
    Notes:
        This is the final amount of Days to skip from the given Current Date to the Final date.
        Though, this amount does not take in account if the last day is a Weekend so we need to correct
        for that.

            Basically, If the last date is a Weekend, we don't work on Weekends so we need to shift the date
            to the nearest Weekend that is a Workday.
    """
    amount_of_days_to_skip_corrected = (
        amount_of_days_to_skip_since_week_current_date_monday +
        amount_of_days_between_week_current_date_monday_and_date_current +
        amount_of_weekdays_where_a_date_exclude_is_on_a_weekday_since_week_current_date_monday +
        # The below is the Final Day skip because we have to skip the last workday
        (1 if amount_of_weekdays_to_skip >= 0 else -1)
    )

    print(f"{amount_of_days_to_skip_corrected=}")

    # This is the assumed last date, because we don't know if it's a Weekend or a Weekday
    datetime__date_last_assumed = (
        datetime__date_current +
        timedelta(days=amount_of_days_to_skip_corrected)
    )

    # The last date corrected to be a Weekday if it wasn't already
    datetime__date_last_corrected, amount_of_days_to_shift = _get_datetime__shift_weekend_to_weekday___and___offset(
        datetime__date_last_assumed,
        amount_of_days_to_skip_corrected
    )

    return datetime__date_last_corrected


def _get_datetime__shift_weekend_to_weekday___and___offset(datetime__weekend_assummed: datetime, int_jump_direction: int) -> datetime:
    """
    Returns a datetime that is a Weekday by shifting the date 
    to either a Friday or Monday depending on if int_jump_direction is Negative or Positive respectively

    Args:
        datetime__weekend (datetime.datetime): A Datetime that is assumed to be a Weekend 
        int_jump_direction (int): Negative and Positive Integer value that determines shifting direction
    Returns:    
        datetime: Shifted datetime if necessary
    """
    datetime__date_weekday = datetime__weekend_assummed

    amount_of_days_to_shift = 0

    # If the datetime is Saturday or Sunday
    if datetime__date_weekday.weekday() > 4:

        # Shifting the datetime forward in time
        if int_jump_direction >= 0:

            # Example: (7 - 5) = 2 -> Saturday skipping 2 Days to get to Monday
            amount_of_days_to_shift = 7 - datetime__date_weekday.weekday()

            datetime__date_weekday = (
                datetime__weekend_assummed +
                # Using .weekday() to get the day shift
                timedelta(days=amount_of_days_to_shift)
            )

        # Shifting the datetime backward in time
        elif int_jump_direction < 0:

            # Example: -1 * (3 - (7 - 5)) = -1 -> Saturday skipping -1 Day to get to Friday
            amount_of_days_to_shift = (
                (-1 * (3 - (7 - datetime__date_weekday.weekday())))
            )

            datetime__date_weekday = (
                datetime__weekend_assummed +
                timedelta(
                    days=amount_of_days_to_shift)

            )
    return datetime__date_weekday, amount_of_days_to_shift


def _get_amount_of_weekend_days_given_amount_of_weekdays_to_skip(amount_of_weekdays_to_skip_since_week_current_date_monday: int) -> int:
    """
    # ----- AMOUNT OF WEEKENDS PER AMOUNT OF WEEKDAYS TO SKIP SINCE WEEK CURRENT DATE MONDAY
    Notes:
        Basically, we are solving for how many Weekends have passed starting on Current Week's
        Monday. We Divide by 5 because we have access to Weekdays and not days. Eventually we will use 
        this value to calculate how many Weekend days have passed and thus we can use that value
        to calculate how many Days since Current Week's Monday we need to skip.

        Why we divide and floor (Floor Division) by 5:
            Since we are dealing with Weekdays AND we start on Monday, we know when the Weekend will start
            which is every 5 days starting on and including Monday. This means that we can divide the amount of weekdays to skip by 5
            to know how many weekends have passed.

            There is a beautiful trick when flooring a number that is less than 0.
            The trick is that if the result is negative then that value floored will become
            the nearest whole integer that is furthest away from 0. 
                The floor function rounds down to the largest integer less than or equal to the
                result.
            This is different from rounding which rounds to the nearest whole integer that its close to.

            Why Floor Division trick is important:
                Since we start on Monday then the immediate 2 days before Monday is the Weekend.
                If we are skipping days going backwards, then the result of the Floor Division is Negative.
                Because the result is Negative it will be rounded down to the nearest whole integer
                which implies that we immediately take in account the amount of weekends that have passed.

                Example:
                    Amount of weekdays to skip since Monday = -1 Day
                    Amount of weekends that have passed = (-1 Day)/5 = -1 Weekend
                    Amount of weekend days that have passed = (-1 Weekend) * 2 = -2 Weekend Days

                    Since we don't care about Weekend days because they are never Weekdays, then
                    we can ignore them and immediately skip them to the nearest Weekday which
                    is Friday of the previous week.

    """
    amount_of_weekends_per_amount_of_weekdays_to_skip_since_week_current_date_monday = (
        amount_of_weekdays_to_skip_since_week_current_date_monday // 5
    )

    # print(f"{amount_of_weekends_per_amount_of_weekdays_to_skip_since_week_current_date_monday=} ")

    """
    # ----- AMOUNT OF WEEKEND DAYS IN AMOUNT OF WEEKENDS PER AMOUNT OF WEEKDAYS TO SKIP SINCE WEEK CURRENT DATE MONDAY
    Notes:
        (Amount of Weekend Days that have passed since Current Week's Monday) = (
            (Amount of Weekends that have passed) * 2
        )
    """
    amount_of_weekend_days_in_amount_of_weekends_per_amount_of_weekdays_to_skip_since_week_current_date_monday = (
        amount_of_weekends_per_amount_of_weekdays_to_skip_since_week_current_date_monday * 2
    )

    # print(f"{amount_of_weekend_days_in_amount_of_weekends_per_amount_of_weekdays_to_skip_since_week_current_date_monday=}")

    return amount_of_weekend_days_in_amount_of_weekends_per_amount_of_weekdays_to_skip_since_week_current_date_monday


def main():
    # Example Staring Day
    start_date = "2025-03-05"

    # Base Holidays
    holidays = ["2025-03-17", "2025-03-10"]

    # Harder Holidays  # Note that the holidays list is now not sorted
    holidays.extend((
        "2025-03-27", "2025-03-28", "2025-03-21", "2025-03-26", "2025-03-24",
    ))

    # Past Holidays  # Note that the holidays list is now not sorted
    holidays.extend(("2025-02-25", "2025-02-26",))

    # Full Weekday Holidays  # Note that the holidays list is now not sorted
    holidays.extend((
        "2025-04-07", "2025-04-08", "2025-04-09", "2025-04-10", "2025-04-11",
    ))

    # Past Full Weekday Holidays  # Note that the holidays list is now not sorted
    holidays.extend((
        "2025-02-10", "2025-02-11", "2025-02-12", "2025-02-13", "2025-02-14",
    ))

    for days in range(-40, 40):

        print("{} {} {}\n".format("#"*25, f"{days}", "#"*25))

        # Call the workday function
        result_1 = workday(start_date, days, holidays)

        # Print the result
        print(f"Start Date: {start_date}")
        print(f"Weekdays to Add EXLUDING HOLIDAYS: {days}")
        print(f"Holidays: {holidays}")
        print(f"Resulting Date: {result_1}")
        print()

        result_2 = workday_fast(start_date, days, holidays)

        # Print the result
        print(f"Start Date: {start_date}")
        print(f"Weekdays to Add EXLUDING HOLIDAYS: {days}")
        print(f"Holidays: {holidays}")
        print(f"Resulting Date: {result_2}")
        print()

        print(f"RESULTS ARE THE SAME: {result_1 == result_2}")
        if result_1 != result_2:
            exit("RESULTS ARE DIFFERENT, FIXME JOSEPH")


if __name__ == "__main__":
    main()
