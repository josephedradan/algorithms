"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 3/10/2020

Purpose:
    Test my implementation of Algorithm X

Details:

Description:

Notes:
    For Collection Y containing Subsets of X Find Collection Z that contains Subsets of X from Collection Y that
    are partitions of X

IMPORTANT NOTES:
    It's confusing, so just read the wiki

    Also make V2
Explanation:

Reference:
    Knuth's Algorithm X
        https://www.wikiwand.com/en/Knuth%27s_Algorithm_X

    Algorithm X in 30 lines!
        https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html

"""
from pprint import pprint

from josephs_resources.decorators.v1.callgraph_simple import callgraph, create_callgraph
from typing import Set, Dict
import sys


def _dict_printer(dict_given: dict):
    [print("{} : {}".format(key, value)) for key, value in dict_given.items()]


def _algorithem_x_printer(dict_number_letters, dict_letter_numbers, set_given, list_solution):
    print("Collection Y")
    _dict_printer(dict_number_letters)
    print()
    print("Tranformation")
    _dict_printer(dict_letter_numbers)
    print()
    print("Set X")
    print(set_given)
    print()
    print("List Solution")
    print(list_solution)
    print("-" * 100)


@callgraph
def algorithm_x_recursive(dict_number_letters: Dict[int, Set[str]], set_given: set, list_solution: list):
    """
    For given set X and collection of subsets Y, this algorithm finds subcollection Y* that are the partitions of X
    meaning that all elements of X are in the subcollection Y*


    :param dict_number_letters: Connections from set_given to set_y
    :param set_given: set_x
    :param list_solution: List containing subsets via letters from the transformation of set_x
    :return: list_solution
    """

    # Transform the dict from dict key value to dict value key
    dict_letter_numbers = transform_dict(dict_number_letters)  # type: Dict[str, Set[int]]

    # Algorithm X printer
    _algorithem_x_printer(dict_number_letters, dict_letter_numbers, set_given, list_solution)

    # Smallest number of elements per column of set_given
    smallest_number_of_elements_per_set_given = smallest_amount_of_ones(dict_number_letters, set_given)

    # If smallest number is 0 then return that their is no solution given specific Path
    if smallest_number_of_elements_per_set_given == 0:
        return None

    # If dict_number_letters is empty then return the partitions
    if not dict_number_letters:
        return list_solution

    # For number and set(letters) in dict
    for key_number, value_letters in dict_number_letters.items():

        # If len of set(letters) == smallest_number_of_elements_per_set_given
        if len(value_letters) == smallest_number_of_elements_per_set_given:

            # For letter in letters
            for value_letter in value_letters:

                # Make a copy of the solution List
                solution_copy = list_solution.copy()

                # Add current letter (value_letter) to solution List
                solution_copy.append(value_letter)

                # Make copy of dict of letter numbers
                dict_letter_numbers_copy = dict_letter_numbers.copy()

                # temp set of numbers given a letter
                temp_set_numbers = dict_letter_numbers[value_letter]

                # Make a copy of the set_given
                set_copy = set_given.copy()

                # Modify the set_copy
                set_copy = set_copy.difference(temp_set_numbers)

                # Make a set of letters based on the numbers from the current letter
                temp_set_letters = set()
                for number in temp_set_numbers:
                    for letter in dict_number_letters[number]:
                        temp_set_letters.add(letter)

                # For letter in set of letters based on the numbers from the current letter
                for letter in temp_set_letters:
                    # Remove the letters from a copy of the dict_letter_numbers_copy
                    del dict_letter_numbers_copy[letter]  # Remaining D {3,5,6}

                # Transform dict_letter_numbers_copy to a dict_number_letter_temp_of_copy
                dict_number_letter_temp_of_copy = transform_dict(dict_letter_numbers_copy)

                # Recursively call this function given the new copies
                answer = algorithm_x_recursive(dict_number_letter_temp_of_copy,
                                               set_copy,
                                               solution_copy)

                # If answer is None then pass this iteration
                if answer is None:
                    continue
                # If the answer is not None then return the the solution List
                return answer

    return None  # Explicit Return rather than Implicit if all else fails


@callgraph
def smallest_amount_of_ones(dict_number_letters: Dict[int, Set[str]], set_given: Set[int]) -> int:
    """
    Given a dict of numbers Key and sets Value with

    FIXME: THIS IS UGLY, I DON'T LIKE sys.maxsize

    :param dict_number_letters: Subset
    :param set_given: Set
    :return:
    """

    # Max int
    smallest = sys.maxsize

    # For number in the set
    for number in set_given:

        # Value of the given number
        temp = dict_number_letters.get(number, 0)

        # If temp is a set
        if isinstance(temp, set):
            temp = len(temp)

        # If temp is a number, used when the set is empty and the fallback is 0
        if temp < smallest:
            smallest = temp

    return smallest


@callgraph
def transform_dict(dict_given: Dict) -> Dict:
    """
    Transform the dict from Key Value to Value Key

    :param dict_given: a dict given
    :return: dict
    """

    # New Dict
    dict_new = {}  # type: Dict[str, Set]

    # For key value pair
    for key, value in dict_given.items():

        # For set in value
        for row_name in value:

            # If key does not exist, then add it.
            if dict_new.get(row_name, False) is False:
                dict_new[row_name] = set()

            # Add key to given dict_new key
            dict_new[row_name].add(key)

    return dict_new


# Random thingy??
# Z = transform_dict(SET_Y)

if __name__ == '__main__':
    # print(smallest_amount_of_ones(Y))
    # print(transform_collection(transform_collection(Y)))

    SET_X = {1, 2, 3, 4, 5, 6, 7}

    SET_Y = {
        1: {'A', 'B'},
        2: {'E', 'F'},
        3: {'D', 'E'},
        4: {'A', 'B', 'C'},
        5: {'C', 'D'},
        6: {'D', 'E'},
        7: {'A', 'C', 'E', 'F'}}  # type: Dict[int, Set]

    solution = algorithm_x_recursive(SET_Y, SET_X, [])
    print("Solution")
    print(solution)

    # Export the functions calls as a SVG the call graph
    # create_callgraph()
