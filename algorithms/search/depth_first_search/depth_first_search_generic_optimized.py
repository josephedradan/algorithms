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
from typing import List


# from josephs_resources.decorators.v1.callable_called_count import print_callable_called_count, callable_called_count
# from josephs_resources.decorators.v2.timer import timer


# @timer
def get_list_dfs_traversal(list_given: list) -> List[list]:
    """
    Given a list, finds all combinations and their permutations

    :param list_given: list given
    :return: list of a list of solutions
    """

    # List containing lists which are solutions
    list_list_shared_solutions = []  # type: List[list]

    # A Temp list that can potentially be a solution
    list_temp_shared_generic_solution = []  # type: list

    # Recursive DFS call
    _get_list_dfs_traversal_helper(list_temp_shared_generic_solution, list_given, list_list_shared_solutions)

    return list_list_shared_solutions


# @callable_called_count
def _get_list_dfs_traversal_helper(list_temp_shared_generic_solution: list,
                                   list_remaining_items: list,
                                   list_list_shared_solutions: list) -> None:
    """
    Recursive DFS function to find all combinations and their permutations

    Total iterations (Permutation formula):
        Less than
        Summation from r = 1 to n of (n!)/((n-r)!)
            where   r = sample size                         == len(list_remaining_items)
                    n = number of objects                   == len(list_remaining_items)
                    (n!)/((n-r)!) = permutation formula

    :param list_temp_shared_generic_solution: Temporary List of the current permutation (temp List is shared)
    :param list_remaining_items: List of remaining items that need to be added to list_temp_shared_generic_solution
    :param list_list_shared_solutions: List of a lists that are to solutions
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

        # Add a copy of list_temp_shared_generic_solution to the list_list_shared_solutions
        list_list_shared_solutions.append(list_temp_shared_generic_solution.copy())

        # Don't recursive call if list_remaining_items_new is empty because you loop for no reason with a range(0)
        if list_remaining_items_new:
            # Recursive call into this function
            _get_list_dfs_traversal_helper(list_temp_shared_generic_solution,
                                           list_remaining_items_new,
                                           list_list_shared_solutions)

        # Pop from list_temp_permutation for a new permutation
        list_temp_shared_generic_solution.pop()


def test_example():
    solution = get_list_dfs_traversal([1, 2, 3, 4, 5])
    for i in solution: print(i)
    print(len(solution))
    # print_callable_called_count()
    """
    Callable: get_list_dfs_traversal                  
    Callable ran in 0.0 Sec
    [1]
    [1, 2]
    [1, 2, 3]
    [1, 2, 3, 4]
    [1, 2, 3, 4, 5]
    [1, 2, 3, 5]
    [1, 2, 3, 5, 4]
    [1, 2, 4]
    [1, 2, 4, 3]
    [1, 2, 4, 3, 5]
    [1, 2, 4, 5]
    [1, 2, 4, 5, 3]
    [1, 2, 5]
    [1, 2, 5, 3]
    [1, 2, 5, 3, 4]
    [1, 2, 5, 4]
    [1, 2, 5, 4, 3]
    [1, 3]
    [1, 3, 2]
    [1, 3, 2, 4]
    [1, 3, 2, 4, 5]
    [1, 3, 2, 5]
    [1, 3, 2, 5, 4]
    [1, 3, 4]
    [1, 3, 4, 2]
    [1, 3, 4, 2, 5]
    [1, 3, 4, 5]
    [1, 3, 4, 5, 2]
    [1, 3, 5]
    [1, 3, 5, 2]
    [1, 3, 5, 2, 4]
    [1, 3, 5, 4]
    [1, 3, 5, 4, 2]
    [1, 4]
    [1, 4, 2]
    [1, 4, 2, 3]
    [1, 4, 2, 3, 5]
    [1, 4, 2, 5]
    [1, 4, 2, 5, 3]
    [1, 4, 3]
    [1, 4, 3, 2]
    [1, 4, 3, 2, 5]
    [1, 4, 3, 5]
    [1, 4, 3, 5, 2]
    [1, 4, 5]
    [1, 4, 5, 2]
    [1, 4, 5, 2, 3]
    [1, 4, 5, 3]
    [1, 4, 5, 3, 2]
    [1, 5]
    [1, 5, 2]
    [1, 5, 2, 3]
    [1, 5, 2, 3, 4]
    [1, 5, 2, 4]
    [1, 5, 2, 4, 3]
    [1, 5, 3]
    [1, 5, 3, 2]
    [1, 5, 3, 2, 4]
    [1, 5, 3, 4]
    [1, 5, 3, 4, 2]
    [1, 5, 4]
    [1, 5, 4, 2]
    [1, 5, 4, 2, 3]
    [1, 5, 4, 3]
    [1, 5, 4, 3, 2]
    [2]
    [2, 1]
    [2, 1, 3]
    [2, 1, 3, 4]
    [2, 1, 3, 4, 5]
    [2, 1, 3, 5]
    [2, 1, 3, 5, 4]
    [2, 1, 4]
    [2, 1, 4, 3]
    [2, 1, 4, 3, 5]
    [2, 1, 4, 5]
    [2, 1, 4, 5, 3]
    [2, 1, 5]
    [2, 1, 5, 3]
    [2, 1, 5, 3, 4]
    [2, 1, 5, 4]
    [2, 1, 5, 4, 3]
    [2, 3]
    [2, 3, 1]
    [2, 3, 1, 4]
    [2, 3, 1, 4, 5]
    [2, 3, 1, 5]
    [2, 3, 1, 5, 4]
    [2, 3, 4]
    [2, 3, 4, 1]
    [2, 3, 4, 1, 5]
    [2, 3, 4, 5]
    [2, 3, 4, 5, 1]
    [2, 3, 5]
    [2, 3, 5, 1]
    [2, 3, 5, 1, 4]
    [2, 3, 5, 4]
    [2, 3, 5, 4, 1]
    [2, 4]
    [2, 4, 1]
    [2, 4, 1, 3]
    [2, 4, 1, 3, 5]
    [2, 4, 1, 5]
    [2, 4, 1, 5, 3]
    [2, 4, 3]
    [2, 4, 3, 1]
    [2, 4, 3, 1, 5]
    [2, 4, 3, 5]
    [2, 4, 3, 5, 1]
    [2, 4, 5]
    [2, 4, 5, 1]
    [2, 4, 5, 1, 3]
    [2, 4, 5, 3]
    [2, 4, 5, 3, 1]
    [2, 5]
    [2, 5, 1]
    [2, 5, 1, 3]
    [2, 5, 1, 3, 4]
    [2, 5, 1, 4]
    [2, 5, 1, 4, 3]
    [2, 5, 3]
    [2, 5, 3, 1]
    [2, 5, 3, 1, 4]
    [2, 5, 3, 4]
    [2, 5, 3, 4, 1]
    [2, 5, 4]
    [2, 5, 4, 1]
    [2, 5, 4, 1, 3]
    [2, 5, 4, 3]
    [2, 5, 4, 3, 1]
    [3]
    [3, 1]
    [3, 1, 2]
    [3, 1, 2, 4]
    [3, 1, 2, 4, 5]
    [3, 1, 2, 5]
    [3, 1, 2, 5, 4]
    [3, 1, 4]
    [3, 1, 4, 2]
    [3, 1, 4, 2, 5]
    [3, 1, 4, 5]
    [3, 1, 4, 5, 2]
    [3, 1, 5]
    [3, 1, 5, 2]
    [3, 1, 5, 2, 4]
    [3, 1, 5, 4]
    [3, 1, 5, 4, 2]
    [3, 2]
    [3, 2, 1]
    [3, 2, 1, 4]
    [3, 2, 1, 4, 5]
    [3, 2, 1, 5]
    [3, 2, 1, 5, 4]
    [3, 2, 4]
    [3, 2, 4, 1]
    [3, 2, 4, 1, 5]
    [3, 2, 4, 5]
    [3, 2, 4, 5, 1]
    [3, 2, 5]
    [3, 2, 5, 1]
    [3, 2, 5, 1, 4]
    [3, 2, 5, 4]
    [3, 2, 5, 4, 1]
    [3, 4]
    [3, 4, 1]
    [3, 4, 1, 2]
    [3, 4, 1, 2, 5]
    [3, 4, 1, 5]
    [3, 4, 1, 5, 2]
    [3, 4, 2]
    [3, 4, 2, 1]
    [3, 4, 2, 1, 5]
    [3, 4, 2, 5]
    [3, 4, 2, 5, 1]
    [3, 4, 5]
    [3, 4, 5, 1]
    [3, 4, 5, 1, 2]
    [3, 4, 5, 2]
    [3, 4, 5, 2, 1]
    [3, 5]
    [3, 5, 1]
    [3, 5, 1, 2]
    [3, 5, 1, 2, 4]
    [3, 5, 1, 4]
    [3, 5, 1, 4, 2]
    [3, 5, 2]
    [3, 5, 2, 1]
    [3, 5, 2, 1, 4]
    [3, 5, 2, 4]
    [3, 5, 2, 4, 1]
    [3, 5, 4]
    [3, 5, 4, 1]
    [3, 5, 4, 1, 2]
    [3, 5, 4, 2]
    [3, 5, 4, 2, 1]
    [4]
    [4, 1]
    [4, 1, 2]
    [4, 1, 2, 3]
    [4, 1, 2, 3, 5]
    [4, 1, 2, 5]
    [4, 1, 2, 5, 3]
    [4, 1, 3]
    [4, 1, 3, 2]
    [4, 1, 3, 2, 5]
    [4, 1, 3, 5]
    [4, 1, 3, 5, 2]
    [4, 1, 5]
    [4, 1, 5, 2]
    [4, 1, 5, 2, 3]
    [4, 1, 5, 3]
    [4, 1, 5, 3, 2]
    [4, 2]
    [4, 2, 1]
    [4, 2, 1, 3]
    [4, 2, 1, 3, 5]
    [4, 2, 1, 5]
    [4, 2, 1, 5, 3]
    [4, 2, 3]
    [4, 2, 3, 1]
    [4, 2, 3, 1, 5]
    [4, 2, 3, 5]
    [4, 2, 3, 5, 1]
    [4, 2, 5]
    [4, 2, 5, 1]
    [4, 2, 5, 1, 3]
    [4, 2, 5, 3]
    [4, 2, 5, 3, 1]
    [4, 3]
    [4, 3, 1]
    [4, 3, 1, 2]
    [4, 3, 1, 2, 5]
    [4, 3, 1, 5]
    [4, 3, 1, 5, 2]
    [4, 3, 2]
    [4, 3, 2, 1]
    [4, 3, 2, 1, 5]
    [4, 3, 2, 5]
    [4, 3, 2, 5, 1]
    [4, 3, 5]
    [4, 3, 5, 1]
    [4, 3, 5, 1, 2]
    [4, 3, 5, 2]
    [4, 3, 5, 2, 1]
    [4, 5]
    [4, 5, 1]
    [4, 5, 1, 2]
    [4, 5, 1, 2, 3]
    [4, 5, 1, 3]
    [4, 5, 1, 3, 2]
    [4, 5, 2]
    [4, 5, 2, 1]
    [4, 5, 2, 1, 3]
    [4, 5, 2, 3]
    [4, 5, 2, 3, 1]
    [4, 5, 3]
    [4, 5, 3, 1]
    [4, 5, 3, 1, 2]
    [4, 5, 3, 2]
    [4, 5, 3, 2, 1]
    [5]
    [5, 1]
    [5, 1, 2]
    [5, 1, 2, 3]
    [5, 1, 2, 3, 4]
    [5, 1, 2, 4]
    [5, 1, 2, 4, 3]
    [5, 1, 3]
    [5, 1, 3, 2]
    [5, 1, 3, 2, 4]
    [5, 1, 3, 4]
    [5, 1, 3, 4, 2]
    [5, 1, 4]
    [5, 1, 4, 2]
    [5, 1, 4, 2, 3]
    [5, 1, 4, 3]
    [5, 1, 4, 3, 2]
    [5, 2]
    [5, 2, 1]
    [5, 2, 1, 3]
    [5, 2, 1, 3, 4]
    [5, 2, 1, 4]
    [5, 2, 1, 4, 3]
    [5, 2, 3]
    [5, 2, 3, 1]
    [5, 2, 3, 1, 4]
    [5, 2, 3, 4]
    [5, 2, 3, 4, 1]
    [5, 2, 4]
    [5, 2, 4, 1]
    [5, 2, 4, 1, 3]
    [5, 2, 4, 3]
    [5, 2, 4, 3, 1]
    [5, 3]
    [5, 3, 1]
    [5, 3, 1, 2]
    [5, 3, 1, 2, 4]
    [5, 3, 1, 4]
    [5, 3, 1, 4, 2]
    [5, 3, 2]
    [5, 3, 2, 1]
    [5, 3, 2, 1, 4]
    [5, 3, 2, 4]
    [5, 3, 2, 4, 1]
    [5, 3, 4]
    [5, 3, 4, 1]
    [5, 3, 4, 1, 2]
    [5, 3, 4, 2]
    [5, 3, 4, 2, 1]
    [5, 4]
    [5, 4, 1]
    [5, 4, 1, 2]
    [5, 4, 1, 2, 3]
    [5, 4, 1, 3]
    [5, 4, 1, 3, 2]
    [5, 4, 2]
    [5, 4, 2, 1]
    [5, 4, 2, 1, 3]
    [5, 4, 2, 3]
    [5, 4, 2, 3, 1]
    [5, 4, 3]
    [5, 4, 3, 1]
    [5, 4, 3, 1, 2]
    [5, 4, 3, 2]
    [5, 4, 3, 2, 1]
    325
    Callable: _get_list_dfs_traversal_helper
    Callable Call Count: 206
    """


if __name__ == '__main__':
    test_example()
