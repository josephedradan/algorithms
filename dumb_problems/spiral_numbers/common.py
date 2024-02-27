"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 2/26/2024

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Reference:

"""
import sys
from typing import List
from typing import Tuple
from typing import TypeAlias
from typing import Union

import numpy as np

np.set_printoptions(threshold=sys.maxsize)
np.set_printoptions(linewidth=sys.maxsize)

Grid: TypeAlias = List[List[Union[None, int]]]  # Not Mathematically a matrix
Position: TypeAlias = Tuple[int, int]

# This cycle is clockwise starting from the top right (Up Right)
LIST_CYCLE_POSITION_SHIFT: List[Position] = [
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
    return [[0 for _ in range(x)] for _ in range(y)]


def print_grid(grid: Grid) -> None:
    print(np.array(grid))
