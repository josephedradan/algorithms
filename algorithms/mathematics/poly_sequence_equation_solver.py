"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 12/28/2020

Purpose:
    Robert talked about a sequence equation solver and I thought it was easy so I made it...

Details:

Description:
    Solves the equation for the given sequence and assumes the x values list is relative to 0 and goes up though,
    you can explicitly make the x values list

Notes:
    This file uses matrices and numpy because it makes like easier...

IMPORTANT NOTES:

Explanation:
    Example:
        Given a sequence:
            [4, 14, 40, 88, 164]

        Find the differences between them and between them differences themselves as a list
            [10, 26, 48, 76]
            [16, 22, 28]
            [6, 6]
            [0]

        Select a degree based on the the list of differences with the same difference
            [6, 6]
            Degree == Row == Row index + 1 == 3

        Create the polynomial equation using degree 3
            (a)*(x)^3 + (b)*(x)^2 + (c)*(x)^1 + (d)*(x)^0 == y

        Solve for the coefficients by plugging in x values to equal the y values (y values are the in the sequence).
        x values are not stated so it is assumed that they start at 0 and to the length of the sequence.
        However, you can make your own x values list.

            Assuming that the x values list corresponds to the length of the sequence:
                [0, 1, 2, 3, 4]

                from

                [4, 14, 40, 88, 164]

            Now solve for the coefficients mathematically...

        Solve for the coefficients using a matrix instead:
            Recall the degree is 3 so the amount of rows in the matrix should be 3 + 1 == 4 because of
            coefficients a, b, c, d

            So

            [4, 14, 40, 88]

            based on

            [0, 1, 2, 3]

            Recall the equation:
                (a)*(x)^3 + (b)*(x)^2 + (c)*(x)^1 + (d)*(x)^0 == y

            Pre matrix:
                x = 0
                    a*(0)^3 + b*(0)^2 + c*(0)^1 + d*(0)^0 == 4
                x = 1
                    a*(1)^3 + b*(1)^2 + c*(1)^1 + d*(1)^0 == 14
                x = 2
                    a*(2)^3 + b*(2)^2 + c*(2)^1 + d*(2)^0 == 40
                x = 3
                    a*(3)^3 + b*(3)^2 + c*(3)^1 + d*(3)^0 == 88

            So the matrix representation is
                [[ 0  0  0  1]        [[a]        [[4]
                 [ 1  1  1  1]    .    [b]    =    [14]
                 [ 8  4  2  1]         [c]         [40]
                 [27  9  3  1]]        [d]]        [88]]

            Let represent the matrix in form: A . Z = B
            Now rearrange the matrix to form: A^-1 . B = Z
            Now solve for Z which will give you the values of the coefficients.

Reference:
    1st, 2nd and 3rd differences and Polynomials
        https://www.youtube.com/watch?v=PhcQvPITG3A
            Notes:
                Learning what differences are and how they relate to polynomials

    Determine Polynomial Equation From Table of Values Using Finite Difference
        https://www.youtube.com/watch?v=ORH3TwgvJgI
            Notes:
                How to find the differences and get create the polynomial equation

    What is a Coefficient Matrix, Augmented Matrix
        https://www.youtube.com/watch?v=BUSsrbMehPI
            Notes:
                Basically, we are trying to solve for a, b, c, d, ... instead of x if you watch this video.
                The below reference is a better example of what we are trying to do.

    Solving Linear Systems Using Matrices
        https://www.youtube.com/watch?v=C2QI3eeIiVc
            Notes:
                This is a better example of what we are trying to do.
                Basically, replace x, y, z, ... with a, b, c, ...

    Solve Linear Equations with Python
        https://www.youtube.com/watch?v=44pAWI7v5Zk
            Notes:
                How to solve linear equations in python using numpy

    Python 🐍 Solve Linear Equations
        https://www.youtube.com/watch?v=NO20jcoHH4I
            Notes:
                 The numpy functions to find the inverse matrix and do the dot product.
                 This is used to solve for the coefficients using a matrix
                    https://youtu.be/NO20jcoHH4I?t=167
"""
import math
from typing import List, Union

import numpy as np

EQUATION_FORMAT = "({:.2f})*({})^{} + "


def recursive_difference_solver(list_sequence: list, list_list_difference: List[List[int]] = None) -> List[List[int]]:
    """
    Find the finite differences

    :param list_sequence: list containing the sequence
    :param list_list_difference: list containing the differences
    :return: list_list_difference
    """

    # If there is no list_list_difference given then make one
    if list_list_difference is None:
        # List of differences
        list_list_difference = []

        # Append the given list_sequence to list_list_difference
        # list_list_difference.append(list_sequence)

    # If the current list_sequence is of size 1
    if len(list_sequence) == 1:
        # You can return nothing here as well!
        return list_list_difference

    # Make a temp difference list
    list_difference_temp = []

    # Loop through list_sequence comparing list_sequence[n] - list_sequence[n]
    for index in range(len(list_sequence) - 1):
        # Find the difference
        difference = list_sequence[index + 1] - list_sequence[index]

        # Append the difference to list_difference_temp
        list_difference_temp.append(difference)

    # Append list_difference_temp to list_list_difference
    list_list_difference.append(list_difference_temp)

    # Recursive call to find the other differences
    recursive_difference_solver(list_difference_temp, list_list_difference)

    # return the difference at end of the recursive call (eventually it will return to the caller)
    if len(list_list_difference[-1]) == 1:
        return list_list_difference


def find_row_index_with_same_values(list_list_difference: List[List]) -> int:
    """
    Find the row containing the similar values which determines the degree of the polynomial

    :param list_list_difference: list of differences
    :return: return the (index + 1) AKA the degree
    """
    for index, row in enumerate(list_list_difference):
        if len(set(row)) == 1:
            return index + 1


def get_polynomial_equation(degree: int, list_coefficient_values: Union[List, np.ndarray]) -> str:
    """
    Given the degree and the list_coefficient_values make the equation and return it as a string

    :param list_coefficient_values: the values of for the coefficients in the equation
    :param degree: the polynomial degree
    :return: return the equation
    """

    # Temp string of the polynomial
    equation_temp = ""

    """
    Loop through the degree and the coefficient value at the same time.
    Note that the degrees are reversed and that the reversed iterator is like a generator and can be used 1 time
    """
    for degree, coefficient_value in zip(reversed(range(0, degree + 1)), list_coefficient_values):
        equation_temp += EQUATION_FORMAT.format(coefficient_value, "x", degree)

    # Strip the space and the extra "+" at the end of the string
    equation_temp = equation_temp.strip().rstrip(" + ")

    return equation_temp


def get_x_values_matrix(degree: int, list_x_values: List[int] = None) -> List[List[int]]:
    """
    Get the matrix of the x values with their coefficients

    Notes:
        Ya i know that you can have any size list_x_values because the degree will be the limiter

    :param degree: degree of the polynomial
    :param list_x_values: list of x values that could be anything really...
    :return: matrix of the x values by their degree
    """

    # If you don't give a list_x_values then we'll just assume that it starts from 0 to the degree
    if list_x_values is None:
        list_x_values = list(range(degree + 1))

    # If the degree + 1 does not match the length of list_x_values
    if degree + 1 != len(list_x_values):
        print(
            "Degree + 1 and length of list_x_values do not match! x values: {}".format(str(list_x_values[degree + 1:])))
        # exit(1)

    # Temp Matrix
    matrix_temp = []

    # Note that reverse iterators get exhausting to make it into a list because reverse iterators are a 1 time use
    list_degrees_reversed = list(reversed(range(0, degree + 1)))

    # For value in list of x values
    for value in list_x_values:

        # Make a temp row
        row_temp = []

        # For degree in list of degrees revered
        for degree in list_degrees_reversed:
            # Append to row_temp the value^degree
            row_temp.append(value ** degree)

        # Add row_temp to the temp matrix
        matrix_temp.append(row_temp.copy())

    return matrix_temp


def check_if_solver_is_correct(equation_polynomial, matrix_column_coefficients, degree, list_x_values, list_sequence):
    """
    Check if sequence_equation_solver is correct

    :param equation_polynomial: The polynomial equation
    :param matrix_column_coefficients: column of coefficient values
    :param degree: degree of the polynomial
    :param list_x_values: list of x values for the given sequence
    :param list_sequence: sequence as a list
    :return:
    """
    list_degrees_reversed = list(reversed(range(degree + 1)))

    print("Polynomial Equation: {}".format(equation_polynomial))
    print("Checking if the values in list_sequence equal the Mathematical values...")
    print()
    for sequence_value, x_value in zip(list_sequence, list_x_values):

        # 1 liner arithmetic_expression_reduced_sum
        # arithmetic_expression_reduced_sum = sum([coefficient * (x_value ** degree) for coefficient, degree in
        #                                          zip(matrix_column_coefficients, list_degrees_reversed)])

        equation_temp = ""

        arithmetic_expression_reduced_sum = 0

        for coefficient, degree in zip(matrix_column_coefficients, list_degrees_reversed):
            equation_temp += EQUATION_FORMAT.format(coefficient, x_value, degree)

            arithmetic_expression_reduced_sum += coefficient * (x_value ** degree)

        # Strip the space and the extra "+" at the end of the string
        equation_temp = equation_temp.strip().rstrip(" + ")

        equation_temp += " = {}".format(arithmetic_expression_reduced_sum)
        print(equation_temp)
        print("Does Sequence value: {} == Arithmetic value: {} ?".format(sequence_value,
                                                                         arithmetic_expression_reduced_sum))
        print("Using math.isclose():", math.isclose(sequence_value, arithmetic_expression_reduced_sum))
        print("Using np.allclose():", np.allclose(sequence_value, arithmetic_expression_reduced_sum))

        print()


def sequence_equation_solver(list_sequence: List[int], list_x_values: List[int] = None):
    """
    Solve to find the sequence equation_polynomial

    :param list_sequence: List of the sequence
    :param list_x_values: list of x values
    :return: equation_polynomial
    """
    # Get the list of differences
    list_list_difference = recursive_difference_solver(list_sequence)

    print("List of differences:")
    for row in list_list_difference:
        print(row)
    print()

    row_index = find_row_index_with_same_values(list_list_difference)
    degree = row_index

    print("Find the row with the same difference value (row == degree):")
    print(row_index)
    print()

    # If you don't give a list_x_values then we'll just assume that it starts from 0 to the degree
    if list_x_values is None:
        list_x_values = list(range(degree + 1))

    # Create the x values matrix limited by the degree + 1
    matrix_x_values = get_x_values_matrix(degree, list_x_values[:degree + 1])

    print("Create the matrix of x values with their corresponding coefficient:")
    print(np.array(matrix_x_values))
    print()

    matrix_column_y = list_sequence[0:degree + 1]
    print("Create the Column matrix for the y values (Matches the size the degree + 1):")
    """
    Reference:
        Numpy print a 1d array as a column
            https://stackoverflow.com/questions/48724936/numpy-print-a-1d-array-as-a-column

    """
    print(np.array(matrix_column_y)[:, None])
    print()

    matrix_x_values_inverse = np.linalg.inv(matrix_x_values)
    print("Create the Inverse matrix of the x values:")
    print(matrix_x_values_inverse)
    print()

    matrix_column_coefficients = np.dot(matrix_x_values_inverse, matrix_column_y)
    print("The Dot product of the Inverse matrix of x values and the Column matrix for the y values, "
          "this gets the values of the coefficients:")
    print(matrix_column_coefficients)
    print()

    equation_polynomial = get_polynomial_equation(degree, matrix_column_coefficients)
    print("The Polynomial Equation:")
    print(equation_polynomial)
    print()

    return equation_polynomial, matrix_column_coefficients, degree, list_x_values, list_sequence


def test_example():
    # Example sequence
    list_sequence = [4, 14, 40, 88, 164]

    # This should be the length of the list as a list
    list_sequence_corresponding_x_values = list(range(len(list_sequence)))

    # Use this list to test any other values
    # list_sequence_corresponding_x_values = [-4, -2, 0, 2, 4]

    # Result of the solver
    result = sequence_equation_solver(list_sequence, list_sequence_corresponding_x_values)
    print("-" * 100)
    print()

    # Check if the solver is correct...
    check_if_solver_is_correct(*result)


if __name__ == '__main__':
    test_example()
