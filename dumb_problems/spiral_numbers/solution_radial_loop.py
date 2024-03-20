"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 3/19/2024

Purpose:

Details:

Description:

Notes:
    It's just looping around the given position and placing the correct numbers.
    This is the easiest solution.
IMPORTANT NOTES:

Explanation:

Reference:

"""
from typing import List
from typing import Tuple

from common import Grid
from common import Position
from common import get_grid
from common import print_grid


def place_number(grid: Grid,
                 position_current: Position,
                 value: int,
                 ) -> int:
    """
    Places the given value at the given position in the given grid.

    :param grid:
    :param position_current:
    :param value:
    :return:
    """
    try:
        # This is to prevent negative indexing
        if position_current[0] < 0 or position_current[1] < 0:
            raise Exception

        # Place value in the grid based on a position that may or may not exist
        grid[position_current[1]][position_current[0]] = value

    except Exception as e:
        return 0

    return 1


def radial_loop_add_numbers_to_grid(grid: Grid,
                                    number_of_valid_positions_on_grid: int,
                                    position_start: Position,
                                    bounded: bool = True,
                                    ):
    """
    The radial looping solution to the problem.

    Notes:
        You loop around postion_start and take in account the

    :param grid:
    :param number_of_valid_positions_on_grid:
    :param position_start:
    :param bounded:
    :return:
    """

    length_ring_side = 0

    value_current = 1

    position_current: List[int] = [*position_start]

    _count_valid_positions_traversed = 0

    #####

    # Initial value of the starting value.
    is_valid = place_number(grid, position_current, value_current)

    _count_valid_positions_traversed += is_valid
    value_current += is_valid

    while _count_valid_positions_traversed < number_of_valid_positions_on_grid:

        length_ring_side += 1

        # Go Right
        for i in range(length_ring_side):
            position_current[0] += 1
            is_valid = place_number(grid, position_current, value_current)
            _count_valid_positions_traversed += is_valid
            value_current += is_valid if bounded else 1

        # Go Down
        for i in range(length_ring_side):
            position_current[1] += 1
            is_valid = place_number(grid, position_current, value_current)
            _count_valid_positions_traversed += is_valid
            value_current += is_valid if bounded else 1

        length_ring_side += 1

        # Go Left
        for i in range(length_ring_side):
            position_current[0] -= 1
            is_valid = place_number(grid, position_current, value_current)
            _count_valid_positions_traversed += is_valid
            value_current += is_valid if bounded else 1

        # Go Up
        for i in range(length_ring_side):
            position_current[1] -= 1
            is_valid = place_number(grid, position_current, value_current)
            _count_valid_positions_traversed += is_valid
            value_current += is_valid if bounded else 1


def main_bounded() -> None:
    x = 10
    y = 20
    grid = get_grid(x, y)
    number_of_valid_positions_on_grid = x * y

    position_start: Tuple[int, int] = (5, 5)

    radial_loop_add_numbers_to_grid(grid, number_of_valid_positions_on_grid, position_start, bounded=True)

    print_grid(grid)


def main_unbounded():
    x = 10
    y = 20
    grid = get_grid(x, y)
    number_of_valid_positions_on_grid = x * y

    position_start: Tuple[int, int] = (5, 5)

    radial_loop_add_numbers_to_grid(grid, number_of_valid_positions_on_grid, position_start, bounded=False)

    print_grid(grid)


if __name__ == '__main__':
    main_bounded()
    print()
    main_unbounded()
