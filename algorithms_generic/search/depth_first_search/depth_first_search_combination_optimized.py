"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 3/23/2020

Purpose:
    The most generic DFS algorithm capable of being modified to Fit your needs.
    It is also optimized.

Details:

Description:

Notes:
    Optimized based on the Depth First Search Power Set

IMPORTANT NOTES:
    Use itertools.combinations() instead

Explanation:

Time Complexity:

Reference:

"""
from typing import Set, FrozenSet, List


# from joseph_library.decorators._old.callable_called_count import print_callable_called_count, callable_called_count
# from joseph_library.decorators.timer import timer


# @timer
def get_combination(list_given: list, choose_number: int) -> List[set]:
    """
    Given a list, find the combinations

    :param list_given: list given
    :param choose_number: the size of the combination
    :return: list of a list of solutions
    """

    # Set containing frozensets that are the solutions
    dict_frozenset_shared_solutions = set()  # type: Set[FrozenSet]

    # Set containing frozensets that is a temp set
    dict_frozenset_shared_frozensets_temp = set()  # type: Set[FrozenSet]

    # A Temp list that can potentially be a solution
    list_temp_shared_generic_solution = []  # type: list

    # Recursive DFS call
    _get_combination_helper(list_temp_shared_generic_solution,
                            list_given,
                            dict_frozenset_shared_frozensets_temp,
                            dict_frozenset_shared_solutions,
                            choose_number)

    # Convert frozen set with a tuple
    list_sets = [set(i) for i in dict_frozenset_shared_solutions]

    return list_sets


# @callable_called_count
def _get_combination_helper(list_temp_shared_generic_solution: list,
                            list_remaining_items: list,
                            set_frozenset_shared_frozensets_temp: set,
                            set_frozenset_shared_solutions: set,
                            choose_number: int) -> None:
    """
    Recursive DFS to get permutations of a List with a length of 3 and making them unique via frozenset which is a
    combination.

    Combination iterations (Same amount of iterations as the Power Set iterations but with 2 dicts to prevent
    permutations):
        Summation from r = 1 to n of (n!)/(r!(n-r)!) ==
        2^(len(list_remaining_items)) -1
            where   r = sample size                         == choose_number
                    n = number of objects                   == len(list_remaining_items)
                    (n!)/(r!(n-r)!) = combination formula

    :param list_temp_shared_generic_solution: Temporary List of the current permutation (temp List is shared)
    :param list_remaining_items: List of remaining items that need to be added to list_temp_shared_generic_solution
    :param set_frozenset_shared_frozensets_temp: Set temp of frozensets to prevent unnecessary permutations
    :param set_frozenset_shared_solutions: Set of the frozensets that are solutions
    :param choose_number: the size of the combination
    :return: None
    """

    # Loop through the length of list_remaining_items
    for i in range(len(list_remaining_items)):

        # Add the indexed item into the temp List
        list_temp_shared_generic_solution.append(list_remaining_items[i])

        # Create a copy of list_remaining_items
        list_remaining_items_new = list_remaining_items.copy()

        # Pop off the item with the index number
        list_remaining_items_new.pop(i)

        # Make a frozen set of the list_temp_shared_generic_solution
        frozenset_temp = frozenset(list_temp_shared_generic_solution)

        # If frozenset_temp is not in set_frozenset_shared_frozensets_temp
        if frozenset_temp not in set_frozenset_shared_frozensets_temp:

            # Add the frozenset_temp to set_frozenset_shared_frozensets_temp
            set_frozenset_shared_frozensets_temp.add(frozenset_temp)

            """
            If the len of list_temp_shared_generic_solution is the same of the choose number then that is a combination
            """
            if len(list_temp_shared_generic_solution) == choose_number:
                # Add the frozenset to the solution dict
                set_frozenset_shared_solutions.add(frozenset_temp)

                # Skip the recursive call
                list_temp_shared_generic_solution.pop()
                continue

        # If the key does exist in dict_frozenset_shared_frozensets_temp
        else:

            # Skip the recursive call
            list_temp_shared_generic_solution.pop()
            continue

        # Don't recursive call if list_remaining_items_new is empty because you loop for no reason with a range(0)
        if list_remaining_items_new:
            # Recursive call into this function
            _get_combination_helper(list_temp_shared_generic_solution,
                                    list_remaining_items_new,
                                    set_frozenset_shared_frozensets_temp,
                                    set_frozenset_shared_solutions,
                                    choose_number)

        # Pop from list_temp_permutation for a new permutation
        list_temp_shared_generic_solution.pop()


def test_example():
    solution = get_combination([1, 2, 3, 4, 5], 1)
    for i in solution: print(i)
    print(len(solution))
    # print_callable_called_count()
    print()

    """
    Callable: get_combination                         
    Callable ran in 0.0 Sec
    {2}
    {3}
    {1}
    {5}
    {4}
    5
    Callable: _get_combination_helper
    Callable Call Count: 1
    """

    solution = get_combination([1, 2, 3, 4, 5], 2)
    for i in solution: print(i)
    print(len(solution))
    # print_callable_called_count()
    print()

    """
    Callable: get_combination                         
    Callable ran in 0.0 Sec
    {3, 4}
    {1, 4}
    {2, 3}
    {1, 2}
    {4, 5}
    {2, 5}
    {2, 4}
    {1, 5}
    {3, 5}
    {1, 3}
    10
    Callable: _get_combination_helper
    Callable Call Count: 7
    """

    solution = get_combination([1, 2, 3, 4, 5], 3)
    for i in solution: print(i)
    print(len(solution))
    # print_callable_called_count()
    print()

    """
    Callable: get_combination                         
    Callable ran in 0.0 Sec
    {1, 3, 5}
    {2, 3, 4}
    {1, 2, 4}
    {2, 4, 5}
    {1, 2, 5}
    {2, 3, 5}
    {1, 4, 5}
    {3, 4, 5}
    {1, 2, 3}
    {1, 3, 4}
    10
    Callable: _get_combination_helper
    Callable Call Count: 23
    """

    solution = get_combination([1, 2, 3, 4, 5], 4)
    for i in solution: print(i)
    print(len(solution))
    # print_callable_called_count()
    print()

    """
    Callable: get_combination                         
    Callable ran in 0.0 Sec
    {1, 3, 4, 5}
    {1, 2, 3, 5}
    {2, 3, 4, 5}
    {1, 2, 3, 4}
    {1, 2, 4, 5}
    5
    Callable: _get_combination_helper
    Callable Call Count: 49
    """
    solution = get_combination([1, 2, 3, 4, 5], 5)
    for i in solution: print(i)
    print(len(solution))
    # print_callable_called_count()
    print()

    """
    Callable: get_combination                         
    Callable ran in 0.0 Sec
    {1, 2, 3, 4, 5}
    1
    Callable: _get_combination_helper
    Callable Call Count: 80
    """


if __name__ == '__main__':
    test_example()
