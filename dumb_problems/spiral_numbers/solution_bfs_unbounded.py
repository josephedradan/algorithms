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

    Adding to the grid DOES take in account invalid grid positions
    as valid positions to place numbers.

IMPORTANT NOTES:

Explanation:

Reference:

"""
from queue import Queue
from typing import Set
from typing import Tuple

from common import Grid
from common import LIST_CYCLE_POSITION_SHIFT
from common import Position
from common import get_grid
from common import print_grid

from solution_bfs_bounded import get_generator_add_cycle_position_shift_relative_to_position_relative


def bfs_spiral_add_numbers_to_grid_unbounded(grid: Grid,
                                             number_of_valid_positions_on_grid: int,
                                             position_start: Position,
                                             _list_cycle_position_shift=LIST_CYCLE_POSITION_SHIFT  # NOQA
                                             ):
    """
    This BFS takes in account cells that are not included in the grid and will assign the correct values
    to the existing grid cells based on both existing and non existing cells in the grid.

    :param grid:
    :param number_of_valid_positions_on_grid:
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
    set_position_traveled: Set[Position] = set((position_start,))  # noqa

    # The first inner most spiral starts to the right while all the rest starts at the top right
    _bool_condition_inner_spiral_first = True

    counter = 0

    _count_valid_positions_traversed = 0

    while _count_valid_positions_traversed < number_of_valid_positions_on_grid:

        position_popped = queue_.get()

        counter += 1

        try:
            # Prevent negative indexing
            if position_popped[0] < 0 or position_popped[1] < 0:
                raise Exception

            # Assign value ot assumed valid grid position
            grid[position_popped[1]][position_popped[0]] = counter
            _count_valid_positions_traversed += 1

        except Exception as e:
            pass

        for position_new in generator_add_cycle_position_shift_relative_to_position_relative(position_popped,
                                                                                             position_start):

            if position_new not in set_position_traveled:
                queue_.put(position_new)
                set_position_traveled.add(position_new)

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
    number_of_valid_positions_on_grid = x * y

    position_start: Tuple[int, int] = (5, 5)

    bfs_spiral_add_numbers_to_grid_unbounded(grid, number_of_valid_positions_on_grid, position_start)

    print_grid(grid)


if __name__ == '__main__':
    main()
