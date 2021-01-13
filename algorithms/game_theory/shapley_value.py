"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 10/23/19

Purpose:
    Test Cooperative Game Theory with Shapley value
    Shapely Value - A method of dividing up gains or costs among players according to the value of their individual contributions

Details:

Description:
    You want you know how much you should distribute to an individual based on how much they have contributed

Notes:

IMPORTANT NOTES:
    You are basically doing the power set minus the empty set so (2^n - 1) inputs to find the solution
    where n = number of people contributing

Explanation:

Time Complexity:

Help:
    Formula for finding all combinations (remember they are sets) given a length

    nCr = n!/( (n-r)!*r!)

    n = number of shit you got yo
    r = size you want, aka the restraint

Reference:
    Information:
        https://youtu.be/MHS-htjGgSY?t=299

    Example:
        https://www.youtube.com/watch?v=w9O0fkfMkx0
        https://youtu.be/w9O0fkfMkx0?t=106  # Solution
"""

from typing import List
from typing import NewType
import itertools


class PermutationPairing:

    def __init__(self, list_permutation: list):
        self.list_permutation = list_permutation

        self.set_permutation = set(self.list_permutation)

        self.marginal_contribution_pseudo = [None for _ in range(len(self.set_permutation))]

        self.marginal_contribution = [0 for _ in range(len(self.set_permutation))]

    def solve_marginal_contribution(self, dict_permutation_relative_position: dict):
        """
        Calculates the List self.marginal_contribution

        :param dict_permutation_relative_position: a dict with the positioning of the
        :return:
        """
        for index_list_permutation, item in enumerate(self.list_permutation):
            index_placement = dict_permutation_relative_position.get(item, None)

            if index_list_permutation == 0:
                self.marginal_contribution[index_placement] = self.marginal_contribution_pseudo[index_placement]
            else:
                total = sum(self.marginal_contribution)

                difference = self.marginal_contribution_pseudo[index_placement] - total

                self.marginal_contribution[index_placement] = difference

    def __str__(self):
        return "{} {} {}".format(self.list_permutation, self.marginal_contribution_pseudo,
                                 self.marginal_contribution)


class ShapleyValue:
    def __init__(self, dict_contributions):

        # Dict of contributions per set
        self.dict_tuple_of_item_contribution = dict_contributions

        # List form of Dict of contributions per set
        self.list_set_of_item_contribution = []

        # List of PermutationPairing objects
        self.list_of_PermutationPairing: PermutationPairing = []

        # List of the first permutation to use as a relative position
        self.list_permutation_relative_position = None

        # dict of the first permutation to use as a relative position
        self.dict_permutation_relative_position = None

        # dict of what amount each contributor should get back aka the Shapley Value
        self.dict_contribution_per_each_contributor = {}

    def run(self):
        list_of_singles = get_dict_of_single_sets(self.dict_tuple_of_item_contribution)

        # FIXME: SHITTY WAY TO CHECK IF THE GIVEN IS PROPER
        if len(list_of_singles) == 0:
            print("No, you fucked this shit up, fix it")
            exit(1)

        self.list_set_of_item_contribution = get_list_of_list_of_set_value_from_dict(
            self.dict_tuple_of_item_contribution)

        # list_permutations = get_permutations(list_of_singles)  # Original way
        list_permutations = list(itertools.permutations(list_of_singles))  # Alternative method

        # print(list_permutations)

        # Creates permutation pairing objects
        self._create_permutation_pairing(list_permutations)

        # Relative positions for the marginal contributions
        self.list_permutation_relative_position = self.list_of_PermutationPairing[0].list_permutation

        # Relative positions for the marginal contributions
        self.dict_permutation_relative_position = list_to_dict_key_object_value_index(
            self.list_permutation_relative_position)

        self._calculate_marginal_contribution()

        # for i in self.list_of_PermutationPairing:
        #     print(i)

        self._calculate_average_contribution_for_each_single()

        # print(self.dict_contribution_per_each_contributor)

    def _create_permutation_pairing(self, list_permutations: list):
        for permutation in list_permutations:
            self.list_of_PermutationPairing.append(PermutationPairing(permutation))

    # little delta super script G sub script pi
    def _calculate_marginal_contribution(self):
        """
        Calculate the marginal contribution
        :return: None
        """
        # Forcing annotate type
        # https://stackoverflow.com/questions/41641449/how-do-i-annotate-types-in-a-for-loop
        # permutation_pairing: PermutationPairing
        for permutation_pairing in self.list_of_PermutationPairing:  # type: PermutationPairing

            # Temp List that will be a set
            list_current_combination_temp = []

            # loop through current permutation
            for item in permutation_pairing.list_permutation:
                list_current_combination_temp.append(item)

                # The set to use as a key for list_set_of_item_contribution to find the corresponding value
                set_contribution_current = set(list_current_combination_temp)

                # Get the value associated with the corresponding contribution
                tuple_contribution_value = self._get_value_from_list_set_of_item_contribution(set_contribution_current)

                # Get the index of the current item of the current permutation
                index = self.dict_permutation_relative_position.get(item, None)

                # Place the value of the set contribution in the appropriate index of marginal_contribution_pseudo
                permutation_pairing.marginal_contribution_pseudo[index] = tuple_contribution_value

            # Calculate the marginal contribution for each permutation pairing
            permutation_pairing.solve_marginal_contribution(self.dict_permutation_relative_position)

            # Clear the temp List for the next permutation
            list_current_combination_temp.clear()

            print(permutation_pairing)

    def _calculate_average_contribution_for_each_single(self):

        total_amount_of_permutation_pairings = len(self.list_of_PermutationPairing)

        for contributor in self.list_permutation_relative_position:
            index = self.dict_permutation_relative_position.get(contributor, None)

            total_sum = 0

            for permutation_pairing in self.list_of_PermutationPairing:  # type: PermutationPairing
                total_sum = total_sum + permutation_pairing.marginal_contribution[index]

            average = float(total_sum / total_amount_of_permutation_pairings)

            self.dict_contribution_per_each_contributor[contributor] = average

    def _get_value_from_list_set_of_item_contribution(self, set_given: set):
        for set_contribution in self.list_set_of_item_contribution:
            if set_given == set_contribution[0]:
                return set_contribution[1]

        return None

    def _place_value_to_corresponding_relative_position(self, value, dict_format: dict, list_to_add_to: list):
        index = dict_format.get(self, None)
        list_to_add_to[index] = value

    def print_shapley_value(self):
        [print("Individual: {:30} Contribution: {}".format(key, value)) for key, value in
         self.dict_contribution_per_each_contributor.items()]


def get_dict_of_single_sets(dict_player_individual_contributions_given: dict) -> list:
    list_result = []

    for key in dict_player_individual_contributions_given:
        if len(key) == 1:
            list_result.append(key)

    return list_result


def get_permutations(list_given: list) -> List[list]:
    """
    Custom made permutation finder

    Alternative is to use
        list(itertools.permutations(iter_given))

    :param list_given: given iterable
    :return: List of all the permutations of that List
    """

    # List of all possible permutations
    list_permutations = []

    # Run the solver
    _get_permutations_helper([], list_given, list_permutations)

    # Return list of permutations
    return list_permutations


def _get_permutations_helper(list_temp_permutation: list, list_remaining_items: list, list_permutations: list) -> list:
    """
    Slow... but not very slow on bigger sizes
    Recursive DFS of all permutations of a List

    :param list_temp_permutation: temporary List of the current permutation (temp List is shared)
    :param list_remaining_items: List of remaining items that need to be added to list_temp
    :param list_permutations: List of all the permutations of a given List (permutations List is shared)
    :return:
    """

    # Loop through the remaining List
    for i in range(len(list_remaining_items)):

        # Add the indexed item into the temp List
        list_temp_permutation.append(list_remaining_items[i])

        """
        Create a new list that has removed the indexed item from list_remaining_items 

        Example:
            [beginning : exclusive i] + [i + 1 : end] == [beginning : exclusive i] + [exclusive i : end]
        """
        list_remaining_items_new = list_remaining_items[:i] + list_remaining_items[i + 1:]

        # If list_remaining_items is empty then add a copy of the list_temp_permutation into the list_permutations
        if not list_remaining_items_new:
            list_permutations.append(list_temp_permutation.copy())

        # Don't recursive call if list_remaining_items_new is empty because len(list_remaining_items) is empty
        if list_remaining_items_new:
            # Recursive call into this function
            _get_permutations_helper(list_temp_permutation, list_remaining_items_new, list_permutations)

        # Pop from list_temp_permutation for a new permutation
        list_temp_permutation.pop()


def get_list_of_list_of_set_value_from_dict(dict_given: dict) -> list:
    """
    Key must be iter

    :param dict_given: a dict but the key is a tuple
    :return: List of a List and in the inner List contains a set of the key of the dict and the value of the dict
    """
    list_result = []

    for key, value in dict_given.items():
        list_temp = [set(key), value]
        list_result.append(list_temp)

    return list_result


def list_to_dict_key_object_value_index(list_given: list) -> dict:
    """
    :param list_given: given List
    :return: dictionary using the key as the object in the List and the value as the index
    """
    dict_result = {}

    for index, item in enumerate(list_given):
        dict_result[item] = index

    return dict_result

    # One-liner version
    # return {item: index for index, item in enumerate(list_given)}


# FIXME: Not used
def get_list_of_singles_from_list_of_tuple(iter_given: iter) -> list:
    """
    Get List of items if iterable item is iterable

    :param iter_given: iterable of iterable
    :return: List of one item tuples
    """
    list_result = []

    for item in iter_given:
        if isinstance(item, tuple) and len(item) == 1:
            list_result.append(item[0])

    return list_result


# FIXME: Not used
def _combination_finder(number: int) -> int:
    return (2 ** number) - 1


# FIXME: Not used
def get_dict_of_tuples_from_list_of_tuples(list_given: list) -> dict:
    dict_result = {}

    for tuple_item in list_given:
        dict_result[tuple_item] = [None for _ in range(len(tuple_item))]

    return dict_result


# FIXME: Not used, similar is used somewhere else...
def get_list_list_permutation_marginal_contribution(list_list_given: list) -> list:
    list_result = []

    for list_permutation in list_list_given:
        # FIXME: Slow as in why not just calculate the size of the List once than every time.
        list_temp = [list_permutation, [None for _ in range(len(list_permutation))]]
        list_result.append(list_temp)

    return list_result


# FIXME: Not used
def get_list_of_tuples(list_given: list) -> list:
    """
    :param list_given: List containing List
    :return: List containing tuple
    """
    list_result = []

    for list_item in list_given:
        list_result.append(tuple(list_item))

    return list_result


# FIXME: Not used
def size_checker(iter_given: iter) -> int:
    counter = 0

    for i in iter_given:
        try:
            if len(i) == 1:
                counter = counter + 1
        except TypeError as e:
            print(e)

    return counter


# FIXME: Not Used
def get_dict_contributions_formatter_value_to_set(dict_list: dict) -> dict:
    dict_return = {}
    for key, value in dict_list.items():
        dict_return[key] = set(value)

    return dict_return


# FIXME: Should i use?
def get_dict_contributions_formatter_key_to_tuple(dict_contributions_given: dict) -> dict:
    """
    Formats given dict by making the key a tuple

    :param dict_contributions_given: dict that you want to have it's keys made into a tuple
    :return: new formatted dict
    """

    dict_result = {}

    for key, value in dict_contributions_given.items():
        dict_result[tuple(key)] = value

    return dict_result


if __name__ == '__main__':
    def test_1():
        print("Vincent Knight")
        print('"Cooperative Games and the Shapley value" Example')
        dict_contributions = {("A"): 80,
                              ("B"): 56,
                              ("C"): 70,
                              ("A", "B"): 80,
                              ("A", "C"): 85,
                              ("B", "C"): 72,
                              ("A", "B", "C"): 90
                              }

        # dict_contributions = get_dict_contributions_formatter_value_to_set(dict_contributions)  # DON"T TOUCH
        # dict_contributions = get_dict_contributions_formatter_key_to_tuple(dict_contributions)  # DON"T TOUCH

        shapley_value_object = ShapleyValue(dict_contributions)
        shapley_value_object.run()
        shapley_value_object.print_shapley_value()


    test_1()
    print()


    def test_2():
        print("SciShow")
        print('"Game Theory: The Science of Decision-Making" Example')

        dict_contributions_2 = {("A"): 10,
                                ("B"): 20,
                                ("A", "B"): 40,
                                }

        shapley_value_object = ShapleyValue(dict_contributions_2)
        shapley_value_object.run()
        shapley_value_object.print_shapley_value()


    print()
    test_2()


    def test_3():
        print("Custom Example")
        dict_contributions = {("A"): 80,
                              ("B"): 56,
                              ("C"): 70,
                              ("D"): 64,
                              ("A", "B"): 80,
                              ("A", "C"): 85,
                              ("A", "D"): 78,
                              ("B", "C"): 72,
                              ("B", "D"): 89,
                              ("C", "D"): 83,
                              ("A", "B", "C"): 90,
                              ("A", "B", "D"): 91,
                              ("A", "C", "D"): 89,
                              ("B", "C", "D"): 93,
                              ("A", "B", "C", "D"): 100,
                              }

        shapley_value_object = ShapleyValue(dict_contributions)
        shapley_value_object.run()
        shapley_value_object.print_shapley_value()


    print()
    test_3()
