"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 2/24/2024

Purpose:

Details:

Description:

Notes:
    BFS to add numbers to a grid in clockwise spiral cycle manner.
    Adding to the grid DOES NOT take in account invalid grid positions
    as valid positions to place numbers.

IMPORTANT NOTES:

Explanation:

Reference:

"""
from queue import Queue
from typing import Generator
from typing import List
from typing import Set
from typing import Tuple
from typing import Union

import numpy as np

Grid = List[List[Union[None, int]]]  # Technically not mathematically a matrix
Position = Tuple[int, int]

# This cycle is clockwise starting from the top right (Up Right)
LIST_CYCLE_POISTION_OFFSET: List[Position] = [
    (1, -1),  # Up Right
    (1, 0),  # Right
    (1, 1),  # Down Right
    (0, 1),  # Down
    (-1, 1),  # Down Left
    (-1, 0),  # Left
    (-1, -1),  # Up Left
    (0, -1),  # Up
]


def get_grid(x: int, y: int) -> Grid:
    return [[None for _ in range(x)] for _ in range(y)]


def generator_add_cycle_position_offset(position: Position) -> Generator[Position, None, None]:
    for position_shift in LIST_CYCLE_POISTION_OFFSET:
        yield (
            position[0] + position_shift[0],
            position[1] + position_shift[1]
        )


def bfs_spiral_add_number_to_grid(grid: Grid, position_start: Position) -> None:
    try:
        grid[position_start[1]][position_start[0]]
    except Exception as e:
        return

    queue_: Queue[Position] = Queue()
    queue_.put(position_start)

    # Comma is needed here to prevent adding items of the tuple
    set_position_traveled: Set[Position] = set((position_start,))  # noqa

    # The first inner most spiral starts to the right while all the rest starts at the top right
    _bool_condition_inner_spiral_first = True

    counter = 0

    while not queue_.empty():

        # Everything popped is assumed to exist in the grid, so you don't need a try
        position_popped = queue_.get()

        counter += 1
        grid[position_popped[1]][position_popped[0]] = counter

        for position_new in generator_add_cycle_position_offset(position_popped):
            try:

                """
                The below condition:
                    1. Imply that the grid index exists (short circuit exit)
                    2. Allow for any number because we check for None (Recall 0 is false).                
                """
                if grid[position_new[1]][position_new[0]] is None:
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
    grid = get_grid(10, 20)

    position_start: Tuple[int, int] = (5, 5)

    bfs_spiral_add_number_to_grid(grid, position_start)

    print_grid(grid)


def print_grid(grid: Grid) -> None:
    print(np.array(grid))

    #
    # for i in grid:
    #     print(i)


if __name__ == '__main__':
    main()
