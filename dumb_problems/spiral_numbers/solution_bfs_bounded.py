"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 2/24/2024

Purpose:

Details:

Description:

Notes:
    BFS to add numbers to a grid in a clockwise spiral cycle manner.
    The way in which items are added to the queue in the BFS is based on
    the difference between the initial cell's position (where the spiral starts)
    to the current cell's position, we'll call this the difference position.
    The signs of the difference position's components (negative, 0, positive),
    determines where iteration starts in the clockwise cycle.
    Iteration over the clockwise cycle adds the surrounding elements to the BFS queue.
    The clockwise cycle is hard coded to start from the top right.

    Adding to the grid DOES NOT take in account invalid grid positions
    as valid positions to place numbers.

IMPORTANT NOTES:

Explanation:

Reference:

"""
from queue import Queue
from typing import Callable
from typing import Generator
from typing import List
from typing import Set
from typing import Tuple

from common import Grid
from common import LIST_CYCLE_POSITION_SHIFT
from common import Position
from common import get_grid
from common import print_grid


def generator_add_cycle_position_shift(position: Position,
                                       offset: int = 0,
                                       _list_cycle_position_shift: List[Position] = LIST_CYCLE_POSITION_SHIFT  # NOQA
                                       ) -> Generator[Position, None, None]:
    """
    A generator that will return the correct shifted position based on order of elements in
    _list_cycle_position_shift

    JOSEPH NOTES:
        An alternative to iterating through _list_cycle_position_shift is making the list in to deque.
        Then with the deque, call .rotate(offset) and then iterative over that deque.
        However, you need to reset the deque to it's original form via .rotate(-offset)
        It's a dumb solution, but it is fun to think about.

    :param position:
    :param offset:
    :param _list_cycle_position_shift:
    :return:
    """

    for index in range(len(_list_cycle_position_shift)):
        index_shifted = (index + offset) % len(_list_cycle_position_shift)

        position_shift = _list_cycle_position_shift[index_shifted]

        yield (
            position[0] + position_shift[0],
            position[1] + position_shift[1]
        )


def get_generator_add_cycle_position_shift_relative_to_position_relative(
        list_cycle_position_shift: List[Position]) -> Callable[[Position, Position], Generator[Position, None, None]]:
    """
    Get a custom generator_add_cycle_position_shift that is based on order of elements in list_cycle_position_shift.

    This is needed because

    Notes:
        Both the lexical body of this function (the variables in this function) and the inner function (the defined
        function in this function) make up a closure when the inner function is returned.

    :param list_cycle_position_shift:
    :return:
    """

    # Dictionary to get the correct index_offset based on position_shift fast
    dict_k_position_shift_v_index_offset = {
        position_shift: index for index, position_shift in enumerate(list_cycle_position_shift)
    }

    def _generator_add_cycle_position_shift_relative_to_position_relative(
            position: Position,
            position_relative: Position) -> Generator[Position, None, None]:
        position_distance = (
            position[0] - position_relative[0],
            position[1] - position_relative[1]
        )

        # Branchless sign trick to convert position_distance to position_shift where valid values are (-1, 0, 1)
        sign_x = (position_distance[1] > 0) - (position_distance[1] < 0)
        sign_y = (position_distance[0] > 0) - (position_distance[0] < 0)

        position_shift = (sign_x, sign_y)

        index_offset = dict_k_position_shift_v_index_offset.get(position_shift, 0)

        return generator_add_cycle_position_shift(
            position,
            index_offset,
            list_cycle_position_shift
        )

    return _generator_add_cycle_position_shift_relative_to_position_relative


def bfs_spiral_add_numbers_to_grid_bounded(grid: Grid,
                                           position_start: Position,
                                           _list_cycle_position_shift=LIST_CYCLE_POSITION_SHIFT  # NOQA
                                           ) -> None:
    """
    BFS expand to add the surrounding items to a queue in specific way.
    The order in which items are added to the queue are based on a given position to position_start.

    :param grid:
    :param position_start:
    :param _list_cycle_position_shift:
    :return:
    """
    try:
        grid[position_start[1]][position_start[0]]
    except Exception as e:
        return

    # Get a generator that gets the correct offset based on _list_cycle_position_shift when given a position_target
    generator_add_cycle_position_shift_relative_to_position_relative = (
        get_generator_add_cycle_position_shift_relative_to_position_relative(_list_cycle_position_shift)
    )

    queue_: Queue[Position] = Queue()
    queue_.put(position_start)

    # Comma is needed here to prevent adding items of the tuple
    set_position_traveled: Set[Position] = set((position_start,))  # NOQA

    # The first inner most spiral starts to the right while all the rest starts at the top right
    _bool_condition_inner_spiral_first = True

    counter = 0

    while not queue_.empty():

        # Everything popped is assumed to exist in the grid, so you don't need a try
        position_popped = queue_.get()

        counter += 1
        grid[position_popped[1]][position_popped[0]] = counter

        for position_new in generator_add_cycle_position_shift_relative_to_position_relative(position_popped,
                                                                                             position_start):
            try:

                """
                The below condition:
                    1. Imply that the grid index exists (short circuit exit)
                    2. Check if integer                
                """
                if isinstance(grid[position_new[1]][position_new[0]], int):

                    # Prevent negative indexing
                    if position_new[0] < 0 or position_new[1] < 0:
                        continue

                    if position_new not in set_position_traveled:
                        queue_.put(position_new)
                        set_position_traveled.add(position_new)

            except Exception as e:
                pass

        if _bool_condition_inner_spiral_first:
            """
            By popping the first item in the queue and adding it to the end makes the first element in the queue
            the position to the right of the first element in the grid and the last element in the grid is the 
            top right. 
            """
            queue_.put(queue_.get())
            _bool_condition_inner_spiral_first = False


def main() -> None:
    x = 10
    y = 20
    grid = get_grid(x, y)

    position_start: Tuple[int, int] = (5, 5)

    bfs_spiral_add_numbers_to_grid_bounded(grid, position_start)

    print_grid(grid)


if __name__ == '__main__':
    main()
