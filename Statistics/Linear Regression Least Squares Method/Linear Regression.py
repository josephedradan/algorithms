"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 8/26/2020

Purpose:
    Calculate Linear Regression using Least Squares

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

TODO:
    FUZZER WITH AN ACTUAL linear regression function such as idk...

Reference:
    Linear Regression Using Least Squares Method - Line of Best Fit Equation
        https://www.youtube.com/watch?v=P8hT5nDai6A

"""


def linear_regression(x_list: list, y_list: list) -> (float, float):
    """
    Cannot handle floating point errors

    :param x_list:
    :param y_list:
    :return:
    """

    # Sum of the lists
    x_total_sum = sum(x_list)
    y_total_sum = sum(y_list)

    # Summation of x * y
    # x_total_times_y_total = sum([x * y for x, y in zip(x_list, y_list)])
    x_total_times_y_total = sum(map(lambda x, y: x * y, x_list, y_list))

    # Summation of x^2
    # x_total_squared = sum([x ** 2 for x in x_list])
    x_total_squared = sum(map(lambda x: x ** 2, x_list))

    # Length of x_list
    x_len = len(x_list)

    # ((nΣ(xy)) - (Σx * Σy)) / ((nΣ(x^2)) - (Σx)^2)
    _numerator = ((x_len * x_total_times_y_total) - (x_total_sum * y_total_sum))
    _denominator = ((x_len * x_total_squared) - x_total_sum ** 2)

    slope = _numerator / _denominator

    # The b value
    # (Σy - slope * Σx) / n
    y_intercept = (y_total_sum - slope * x_total_sum) / x_len

    return y_intercept, slope


if __name__ == '__main__':
    y = [1.5, 3.8, 6.7, 9.0, 11.2, 13.6, 16]
    x = [i + 1 for i in range(len(y))]

    b, m = linear_regression(x, y)

    print("y_intercept", b)
    print("slope", m)

