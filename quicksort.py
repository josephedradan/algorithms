"""
Date created: 7/22/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Contributors: 
    https://github.com/josephedradan
    
Reference:
    All Quicksort does is call this function - Partition!
        Notes:
        Reference:
            https://www.youtube.com/watch?v=iUXmmkftzzM

"""
import random
from typing import Callable
from typing import List
from typing import Tuple


def partition_intuitive(list_int: List[int], index_start: int, index_end: int, index_pivot: int):
    """

    Notes:
        Uses 2 lists to modify list_int

        Steps:
            1. Make 2 lists (list_small, list_large)
            2. Loop over list_int and add items to appropriate lists (list_small, list_large)
            3. Replace elements of list_int with list_small, element_pivot, list_large

    Reference:
        All Quicksort does is call this function - Partition!
            Reference:
                https://youtu.be/iUXmmkftzzM?t=301

    :param list_int:
    :param index_start:
    :param index_end:
    :param index_pivot:
    :return:
    """

    """
    Create two new lists
    """
    list_small = []
    list_large = []

    element_pivot = list_int[index_pivot]

    """
    Partition values into list_small and list_large according to pivot
    """

    for index_current in range(index_start, index_end):
        if list_int[index_current] == element_pivot:
            list_small.append(list_int[index_current])
        else:
            list_large.append(list_int[index_current])

    """
    Concatenate the arrays and the pivot
    """
    index_pivot_new = index_start + len(list_small)

    for index, element in enumerate(list_small):
        list_int[index] = element

    list_int[index_pivot_new] = element_pivot

    for index_current in range(index_pivot_new + 1, index_end):
        list_int[index_current] = list_large[index_current]

    return index_pivot_new, list_int


def partition_lomuto(list_int: List[int], index_start: int, index_end: int, index_pivot: int):
    """

    Notes:
        Uses in place swapping on list_int

        Steps:
            1. Swap element_pivot with element_end
            2. index_grow = index_start - 1
            3. Loop uing index over list_int upto last element
                IF list_int[index_current] <= element_pivot
                index_grow = index_grow + 1
                Swap elements at index_grow and index_current in list_int
            4. index_grow = index_grow + 1
                Swap elements at index_grow and index_end in list_int

    Time complexity:
        O(2n)

    Reference:
        All Quicksort does is call this function - Partition!
            Refernece:
                https://youtu.be/iUXmmkftzzM?t=401

    :param list_int:
    :param index_start:
    :param index_end:
    :param index_pivot:
    :return:
    """

    """
    "Hide" pivot at right side of array
    """
    list_int[index_end], list_int[index_pivot] = list_int[index_pivot], list_int[index_end]  # Swap items

    element_pivot = list_int[index_end]

    """
    "Grow" a left partition by swapping items <= the pivot to the left
    """
    index_grow = index_start - 1

    for index_current in range(index_start, index_end - 1):
        if list_int[index_current] <= element_pivot:
            index_grow = index_grow + 1
            list_int[index_grow], list_int[index_current] = list_int[index_current], list_int[index_grow]

    """
    Swap the pivot into the right place
    """
    index_grow += 1
    list_int[index_grow], list_int[index_end] = list_int[index_end], list_int[index_grow]
    index_pivot_new = index_grow

    return index_pivot_new, list_int


def partition_hoares_scheme_incorrect(list_int: List[int], index_start: int, index_end: int, index_pivot: int):
    """

    IMPORTANT NOTES:
        DO NOT USE THIS ALGORITHM

        THIS ALGORITHM CHANGES WHAT THE PIVOT IS WHICH WILL RESULT IN THE WRONG ANSWER

    Notes:
        Grow both partitions

        Steps:
            1. Get the index_middle via index_start and index_end and swap that element_middle with element_pivot
                via index_pivot
            2. Assign the index_pointer_left and index_pointer_right out of their bounds respectively
            3. While True:
                Do
                    index_pointer_left += 1
                while
                    element_index_pointer_left < element_pivot
                Do
                    index_pointer_right -= 1
                while
                    element_index_pointer_right > element_pivot

                if index_pointer_left >= index_pointer_right:
                    return index_pointer_right, list_int

                Swap element_pointer_left with element_pointer_right
    Time complexity:
        O(n)

    :param list_int:
    :param index_start:
    :param index_end:
    :param index_pivot:
    :return:
    """

    """
    Swap pivot into middle of list
    """
    index_middle = (index_start + index_end) // 2

    # Swap element pivot and element middle
    list_int[index_pivot], list_int[index_middle] = list_int[index_middle], list_int[index_pivot]
    element_pivot = list_int[index_middle]

    index_pointer_left = index_start - 1
    index_pointer_right = index_end + 1

    """
    Grow left and right partitions until pointers cross
    """
    while True:
        # Do while loop (Search for the condition to be false)
        index_pointer_left += 1
        while index_pointer_left < len(list_int) and list_int[index_pointer_left] < element_pivot:
            index_pointer_left += 1

        # Do while loop (Search for the condition to be false)
        index_pointer_right -= 1
        while index_pointer_right >= 0 and list_int[index_pointer_right] > element_pivot:
            index_pointer_right -= 1

        if index_pointer_left >= index_pointer_right:
            return index_pointer_right, list_int

        list_int[index_pointer_left], list_int[index_pointer_right] = (list_int[index_pointer_right],
                                                                       list_int[index_pointer_left])


def partition_hoares_scheme_correct(list_int: List[int], index_start: int, index_end: int, index_pivot: int):
    """
    Corrected hoare's scheme method

    Notes:
        Steps:
            1.

    Time complexity:
        O(n)

    Notes:

        Steps:
            1. Swap element_pivot with element_start
            2. Assign the index_pointer_left to be index_start and index_pointer_right out of their bounds
            3. While True:
                Do
                    index_pointer_left += 1
                while
                    element_index_pointer_left < element_pivot
                Do
                    index_pointer_right -= 1
                while
                    element_index_pointer_right > element_pivot

                if index_pointer_left >= index_pointer_right:
                    Swap element_start with element_right
                    return index_pointer_right, list_int

                Swap element_pointer_left with element_pointer_right

    :param list_int:
    :param index_start:
    :param index_end:
    :param index_pivot:
    :return:
    """
    """
    Swap pivot into middle of array
    """

    # Swap element pivot and element start
    list_int[index_pivot], list_int[index_start] = list_int[index_start], list_int[index_pivot]
    element_pivot = list_int[index_start]
    index_pointer_left = index_start
    index_pointer_right = index_end + 1

    """
    "Grow" left and right partitions until pointers cross
    
    Notes:
        This is similar to the incorrect version but with an additional operation
    """
    while True:

        # Do while loop (Search for the condition to be false)
        index_pointer_left += 1
        while index_pointer_left < len(list_int) and list_int[index_pointer_left] < element_pivot:
            index_pointer_left += 1

        # Do while loop (Search for the condition to be false)
        index_pointer_right -= 1
        while index_pointer_right >= 0 and list_int[index_pointer_right] > element_pivot:
            index_pointer_right -= 1

        if index_pointer_left >= index_pointer_right:
            # Swap
            list_int[index_start], list_int[index_pointer_right] = list_int[index_pointer_right], list_int[index_start]

            return index_pointer_right, list_int

        list_int[index_pointer_left], list_int[index_pointer_right] = (list_int[index_pointer_right],
                                                                       list_int[index_pointer_left])


TYPE_CALLABLE_PARTITION = Callable[[List[int], int, int, int], Tuple[int, List[int]]]


def quick_sort(list_int: List[int],
               index_start: int,
               index_end: int,
               partition_function: TYPE_CALLABLE_PARTITION) -> List[int]:
    """
    Notes:
        Remember that CORRECT quicksort function DOES NOT make new memory and does inplace sorting

    :param list_int:
    :param index_start:
    :param index_end:
    :param partition_function:
    :return:
    """

    if index_start >= index_end:
        return list_int

    # Select random pivot
    index_pivot = random.randint(index_start, index_end)
    index_pivot_new, list_int = partition_function(list_int, index_start, index_end, index_pivot)

    list_int = quick_sort(list_int, index_start, index_pivot_new - 1, partition_function)
    list_int = quick_sort(list_int, index_pivot_new + 1, index_end, partition_function)

    return list_int


# @decorator_code_test
def _test_quicksort_intuitive():
    list_int = [3, 1, 5, 2, 4, 10, 11, 123, -342, 5, 23, 1, 2, 4, 2]

    print(quick_sort(list_int, 0, len(list_int) - 1, partition_hoares_scheme_correct))


if __name__ == '__main__':
    # run_callables()

    _test_quicksort_intuitive()
