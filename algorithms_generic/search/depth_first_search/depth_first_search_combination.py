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

    # Set containing frozensets which are solutions
    set_frozenset_shared_solutions = set()  # type: Set[FrozenSet]

    # A Temp list that can potentially be a solution
    list_temp_shared_generic_solution = []  # type: list

    # Recursive DFS call
    _get_combination_helper(list_temp_shared_generic_solution, list_given, set_frozenset_shared_solutions,
                            choose_number)

    # Convert frozen set with a tuple
    list_sets = [set(i) for i in set_frozenset_shared_solutions]

    return list_sets


# @callable_called_count
def _get_combination_helper(list_temp_shared_generic_solution: list,
                            list_remaining_items: list,
                            set_frozenset_shared_solutions: set,
                            choose_number: int) -> None:
    """
    Recursive DFS to get permutations of a List with a length of 3 and making them unique via frozenset which is a
    combination.

    Approximate iterations if choose_number == len(list_remaining_items) (Permutation formula):
        Less than (Due to not Recursive calling for an empty list_remaining_items)
        Summation from r = 1 to n of (n!)/((n-r)!)
            where   r = sample size                         == len(list_remaining_items)
                    n = number of objects                   == len(list_remaining_items)
                    (n!)/((n-r)!) = permutation formula

    Combination iterations (same amount of iterations as the Power Set iterations but with a limit):
        Greater than
        Summation from r = 1 to n of (n!)/(r!(n-r)!)
            where   r = sample size                         == choose_number
                    n = number of objects                   == len(list_remaining_items)
                    (n!)/(r!(n-r)!) = combination formula

    :param list_temp_shared_generic_solution: Temporary List of the current permutation (temp List is shared)
    :param list_remaining_items: List of remaining items that need to be added to list_temp_shared_generic_solution
    :param set_frozenset_shared_solutions: Set of a frozensets that are to solutions
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

        # If the len of list_temp_shared_generic_solution is the same of the choose number then that is the combination
        if len(list_temp_shared_generic_solution) == choose_number:
            """
            Add a frozenset (immutable) which is hashable in a set (mutable)
            IMPORTANT NOTE: If set_frozenset_shared_solutions was OUTSIDE and BEFORE this if statement,
            you would have a Power set with a limiter where the limiter is the choose_number
            """
            set_frozenset_shared_solutions.add(frozenset(list_temp_shared_generic_solution))

            """
            Optimized skip to not iterate past the choose_number by bypassing the recursive call.
            Pop the last element in the list_temp_shared_generic_solution, this should be the
            substitution for the last list_temp_shared_generic_solution.pop() at the end of this loop.
            """
            list_temp_shared_generic_solution.pop()

            # Will skip the recursive call and list_temp_shared_generic_solution.pop()
            continue

        # Don't recursive call if list_remaining_items_new is empty because you loop for no reason with a range(0)
        if list_remaining_items_new:
            # Recursive call into this function
            _get_combination_helper(list_temp_shared_generic_solution,
                                    list_remaining_items_new,
                                    set_frozenset_shared_solutions,
                                    choose_number)

        # Pop from list_temp_permutation for a new permutation
        list_temp_shared_generic_solution.pop()


def test_example():
    """
    Remember that Call Count HAS NOT BEEN RESET AFTER EACH RUN.
    NOTICES THIS ON THE LAST Call Count
        Call Count: 325

        Look at this:
            Approximate iterations if choose_number == len(list_remaining_items) (Permutation formula):
            Summation from r = 1 to n of (n!)/((n-r)!) where n = 5
            == 325

        IT MATCHES... except for the empty set...

    """

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
    Callable Call Count: 33
    """

    solution = get_combination([1, 2, 3, 4, 5], 4)
    for i in solution: print(i)
    print(len(solution))
    # print_callable_called_count()
    print()
    """
    Callable: get_combination                         
    Callable ran in 0.001001596450805664 Sec
    {1, 3, 4, 5}
    {1, 2, 3, 5}
    {2, 3, 4, 5}
    {1, 2, 3, 4}
    {1, 2, 4, 5}
    5
    Callable: _get_combination_helper
    Callable Call Count: 119

    """
    solution = get_combination([1, 2, 3, 4, 5], 5)
    for i in solution: print(i)
    print(len(solution))
    # print_callable_called_count
    print()
    """
    Callable: get_combination                         
    Callable ran in 0.0 Sec
    {1, 2, 3, 4, 5}
    1
    Callable: _get_combination_helper
    Callable Call Count: 325
    """


if __name__ == '__main__':
    test_example()
