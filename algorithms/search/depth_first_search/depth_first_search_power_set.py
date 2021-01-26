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

Explanation:

Time Complexity:

Reference:

"""
from typing import Set, FrozenSet, List


# from josephs_resources.decorators._old.callable_called_count import print_callable_called_count, callable_called_count
# from josephs_resources.decorators.timer import timer


# @timer
def get_power_set(list_given: list) -> List[set]:
    """
    Given a list, find the power set of it which is basically all the combinations for all
    sizes from 0 to length of list_given

    :param list_given: list given
    :return: list of a list of solutions
    """

    # Set containing frozensets which are solutions
    set_frozenset_shared_solutions = set()  # type: Set[FrozenSet]

    # A Temp list that can potentially be a solution
    list_temp_shared_generic_solution = []  # type: list

    # Recursive DFS call
    _get_power_set_helper(list_temp_shared_generic_solution, list_given, set_frozenset_shared_solutions)

    # Convert frozen set with a tuple
    list_sets = [set(i) for i in set_frozenset_shared_solutions]

    # Add the empty set
    list_sets.append(set())

    # Sort the list
    list_sets.sort()

    return list_sets


# @callable_called_count
def _get_power_set_helper(list_temp_shared_generic_solution: list,
                          list_remaining_items: list,
                          set_frozenset_shared_solutions: set) -> None:
    """
    Recursive DFS to get all permutations of a List, but making them unique via frozenset which is a combination

    Notes: The amount of iterations should be - 1 because empty set is not involved

    Total iterations (Permutation formula):
        Less than (Due to not Recursive calling for an empty list_remaining_items)
        Summation from r = 0 to n of (n!)/((n-r)!)
            where   r = sample size                         == len(list_remaining_items)
                    n = number of objects                   == len(list_remaining_items)
                    (n!)/((n-r)!) = permutation formula

    Power Set iterations:
        Greater than
        Summation from r = 0 to n of (n!)/(r!(n-r)!) ==
        2^(len(list_remaining_items))
            where   r = sample size                         == len(list_remaining_items)
                    n = number of objects                   == len(list_remaining_items)
                    (n!)/(r!(n-r)!) = combination formula

    :param list_temp_shared_generic_solution: Temporary List of the current permutation (temp List is shared)
    :param list_remaining_items: List of remaining items that need to be added to list_temp_shared_generic_solution
    :param set_frozenset_shared_solutions: Set of a frozensets that are to solutions
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

        # Add a frozenset (immutable) which is hashable in a set (mutable)
        set_frozenset_shared_solutions.add(frozenset(list_temp_shared_generic_solution))

        # Don't recursive call if list_remaining_items_new is empty because you loop for no reason with a range(0)
        if list_remaining_items_new:
            # Recursive call into this function
            _get_power_set_helper(list_temp_shared_generic_solution,
                                  list_remaining_items_new,
                                  set_frozenset_shared_solutions)

        # Pop from list_temp_permutation for a new permutation
        list_temp_shared_generic_solution.pop()


def test_example():
    solution = get_power_set([1, 2, 3, 4, 5])
    for i in solution: print(i)
    print(len(solution))
    # print_callable_called_count()
    """
    Callable: get_power_set                           
    Callable ran in 0.001001119613647461 Sec
    set()
    {1, 3, 5}
    {1, 4}
    {2}
    {3}
    {2, 3}
    {4}
    {3, 4}
    {2, 4}
    {2, 3, 4}
    {4, 5}
    {1}
    {5}
    {3, 5}
    {2, 3, 5}
    {3, 4, 5}
    {1, 3}
    {1, 2, 3}
    {1, 3, 4}
    {1, 5}
    {1, 4, 5}
    {1, 2}
    {2, 5}
    {2, 4, 5}
    {1, 2, 4, 5}
    {2, 3, 4, 5}
    {1, 2, 5}
    {1, 2, 4}
    {1, 2, 3, 4}
    {1, 3, 4, 5}
    {1, 2, 3, 5}
    {1, 2, 3, 4, 5}
    32
    Callable: _get_power_set_helper
    Callable Call Count: 206
    """


if __name__ == '__main__':
    test_example()
