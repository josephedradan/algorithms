"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 8/11/2021

Purpose:
    Find all tic tac toe winning/draw grid positions and the grids that lead up to that solution grid.

Details:

Description:

Notes:

IMPORTANT NOTES:
    HIGH MEMORY USAGE Over 2gb

Explanation:

Reference:
    Tic Tac Toe Only Has 255168 Possible Moves
        Reference:
            https://www.thomas-herring.com/tic-tac-toe/2019/2/6/tic-tac-toe-only-has-255168-possible-moves

    What is the number of possible ways to win a 3*3 game of tic tac toe?
        Notes:
            "There are 255168 possible game of Tic-tac-toe excluding symmetry.
            The first player wins 131184 of these,
            the second player wins 77904 games and the remaining 46080 are drawn"
        Reference:
            https://www.quora.com/What-is-the-number-of-possible-ways-to-win-a-3*3-game-of-tic-tac-toe

"""
from collections import defaultdict
from typing import Sequence, List, Union, Tuple, Set, Dict

AMOUNT_POSITION = 3


def get_grid_new(size):
    return [[0 for _ in range(size)] for _ in range(size)]


def check_win(grid: Sequence[Sequence[int]], player_number_selected: int) -> bool:
    valid_horizontal = _check_horizontal(grid, player_number_selected)

    # if valid_horizontal:
    #     print(f"Player {player_number_selected} Won by a Horizontal")

    valid_vertical = _check_vertical(grid, player_number_selected)
    # if valid_vertical:
    #     print(f"Player {player_number_selected} Won by a Vertical")

    valid_diagonal = _check_diagonal(grid, player_number_selected)
    # if valid_diagonal:
    #     print(f"Player {player_number_selected} Won by a Diagonal")

    return any((valid_horizontal, valid_vertical, valid_diagonal))


def _check_horizontal(grid: Sequence[Sequence[int]], value_given: int) -> bool:
    """

    Notes:
        Assuming grid is the same size for row/col

    :param grid:
    :param value_given:
    :return:
    """
    # Check horizontal
    for row in grid:
        list_row = []

        for value_position in row:
            if value_position != value_given:
                list_row.append(False)
            else:
                list_row.append(True)

        if all(list_row):
            return True
    return False


def _check_vertical(grid: Sequence[Sequence[int]], value_given: int) -> bool:
    """

    Notes:
        Assuming grid is the same size for row/col

    :param grid:
    :param value_given:
    :return:
    """

    # Check Vertical
    for index_1 in range(len(grid)):
        list_col = []

        for index_2 in range(len(grid[index_1])):
            value_position = grid[index_2][index_1]

            if value_position != value_given:
                list_col.append(False)
            else:
                list_col.append(True)

        if all(list_col):
            return True
    return False


def _check_diagonal(grid: Sequence[Sequence[int]], value_given: int) -> bool:
    """

    Notes:
        Assuming grid is the same size for row/col

    TODO: Ugly solution
    :param grid:
    :param value_given:
    :return:
    """
    list_top_bot = []

    list_bot_top = []

    # Check diagonal
    for index_1 in range(len(grid)):
        value_position_1 = grid[index_1][index_1]
        value_position_2 = grid[len(grid) - 1 - index_1][index_1]

        if value_position_1 == value_given:
            list_top_bot.append(True)
        else:
            list_top_bot.append(False)

        if value_position_2 == value_given:
            list_bot_top.append(True)
        else:
            list_bot_top.append(False)

    return all(list_top_bot) or all(list_bot_top)


def dfs_tic_tac_toe_all_paths_to_solution(
        grid_given: List[List[int]],
        list_player_number: List[int],
        amount_grid_position: int = Union[None, int],
        index_player_number_selected: Union[None, int] = None,
        set_position_visited: Union[None, Set[Tuple[int, int]]] = None,
        list_grid_path: Union[None, List[Sequence[Sequence[int]]]] = None,
        dict_k_player_number_v_list_grid: Union[None, Dict[Union[int, str], List[Sequence[Sequence[int]]]]] = None,
        dict_k_player_number_v_list_list_grid_path: Union[
            None, Dict[Union[int, str], List[List[Sequence[Sequence[int]]]]]] = None):
    """
    DFS to find all possible tic tac toe board states (grid states) and board states (grid states) to achieve those
    final board states

    Notes:
        Assume Player 0 is empty grid space.
        A Draw is considered a solution.

    IMPORTANT NOTES:
        SUPER MEMORY INTENSIVE PAST GRID SIZE = 3 (~2gb), GRID SIZE 4 (>7gb)

    :param grid_given:
    :param list_player_number:
    :param amount_grid_position:
    :param index_player_number_selected:
    :param set_position_visited:
    :param list_grid_path:
    :param dict_k_player_number_v_list_grid:
    :param dict_k_player_number_v_list_list_grid_path:
    :return:
    """
    if dict_k_player_number_v_list_list_grid_path is None:

        # Select first player it list of players
        index_player_number_selected = 0

        # Set of positions visited
        set_position_visited = set()

        # Amount of possible positions in the grid (Allows for strange grids)
        amount_grid_position = 0

        for index_row, e_1 in enumerate(grid_given):
            for index_col, e_2 in enumerate(grid_given[index_row]):
                amount_grid_position += 1

        # Path to solution
        list_grid_path = []

        # Dict of player number and all grid wins (all grid draws if key is "Draw")
        dict_k_player_number_v_list_grid = defaultdict(list)

        # Dict of the player and their list of list list of grids that lead to a solution
        dict_k_player_number_v_list_list_grid_path = defaultdict(list)

    # Loop over grid
    for index_row, e_1 in enumerate(grid_given):
        for index_col, e_2 in enumerate(grid_given[index_row]):

            # Current position
            position_new = (index_row, index_col)

            # Skip posiition already visited
            if position_new in set_position_visited:
                continue

            # Add position to set visited
            set_position_visited.add(position_new)

            # Temp var of the original value at the position
            value_position_original = grid_given[index_row][index_col]

            # Select a player
            player_number_selected = list_player_number[index_player_number_selected]

            # Place player number at grid position
            grid_given[index_row][index_col] = player_number_selected

            # Add modification to grid to list of grids (path to solution)
            list_grid_path.append(tuple(tuple(i) for i in grid_given))

            # print(numpy.array(grid_given))
            # print()

            # Check if player can win
            condition_player_win = False

            # Check if Player number (player) has won
            if player_number_selected != 0:
                condition_player_win = check_win(grid_given, player_number_selected)

            # If player has won, copy list of grids (path to a solution)
            if condition_player_win:

                dict_k_player_number_v_list_list_grid_path[player_number_selected].append(list_grid_path.copy())

                dict_k_player_number_v_list_grid[player_number_selected].append(tuple(tuple(i) for i in grid_given))
                # print(numpy.array(grid_given))
                # print()

            else:

                # Select new player (This condition check allows for more than 2 players0
                if index_player_number_selected < len(list_player_number) - 1:
                    index_player_number_selected_new = index_player_number_selected + 1

                # Reset player turn back to first player if there are no more players to select
                else:
                    index_player_number_selected_new = 0

                # Check if all grid positions have been occupied (The grid results in a draw)
                if len(set_position_visited) == amount_grid_position:
                    dict_k_player_number_v_list_list_grid_path["Draw"].append((list_grid_path.copy()))

                    dict_k_player_number_v_list_grid["Draw"].append(tuple(tuple(i) for i in grid_given))

                # Recursive call
                else:
                    dfs_tic_tac_toe_all_paths_to_solution(grid_given,
                                                          list_player_number,
                                                          amount_grid_position,
                                                          index_player_number_selected_new,
                                                          set_position_visited.copy(),
                                                          list_grid_path,
                                                          dict_k_player_number_v_list_grid,
                                                          dict_k_player_number_v_list_list_grid_path
                                                          )

            # RESTORE VARIABLES TO ORIGINAL STATE

            # Pop the most recently added grid to list of grids (Path to solution)
            list_grid_path.pop()

            # Restore grid value at position
            grid_given[index_row][index_col] = value_position_original

            # Remove position from set of visited positions
            set_position_visited.remove(position_new)

    return dict_k_player_number_v_list_grid, dict_k_player_number_v_list_list_grid_path


def main():
    grid_size = 3

    # Copy an empty grid
    grid = get_grid_new(grid_size)

    # List of players
    list_player = [1,
                   2,
                   # 3,
                   # 4
                   ]

    """
    Dict of the player/"Draw" and their list of grids that are wins (list of grids to a draw if the key is "Draw")
    Dict of the player/"Draw and their list of list of grids to a win (list of list of grids to a draw if the key 
    is "Draw")
    """
    (dict_k_player_number_v_list_grid,
     dict_k_player_number_v_list_solution) = dfs_tic_tac_toe_all_paths_to_solution(grid, list_player)

    print(f"Grid size: {grid_size}")
    print(f"Amount of all possible solutions: {sum([len(i) for i in dict_k_player_number_v_list_solution.values()])}")
    print("=" * 50, end="\n\n")

    for player_number, list_list_grid_path in dict_k_player_number_v_list_solution.items():
        print(f"Player: {player_number}")
        print(f"Amount of solutions: {len(list_list_grid_path)}")
        # for list_grid_path in list_list_grid_path:
        #     grid_win = list_grid_path[-1]
        #     print(numpy.array(grid_win))
        #     print()
        print()


if __name__ == '__main__':
    main()

# Brute force until a solution is found, the solution is always the same.
'''
def dfs_tic_tac_toe_all_paths_to_solution(grid_given: List[List[int]],
                                       list_player_number: List[int],
                                       index_player_number_selected: Union[None, int] = None,
                                       grid_position_start: Union[None, Tuple[int, int]] = None,
                                       list_grid_win: Union[None, List[List[List[int]]]] = None):
    """
    Assume Player 0 is empty grid space

    """
    if list_grid_win is None:
        list_grid_win = []

        # _list_player_number_temp = list_player_number.copy()
        # _list_player_number_temp.append(0)
        # list_player_number = list(set(_list_player_number_temp))
        # list_player_number.sort()

        index_player_number_selected = list_player_number[0]

        # Strictly 2 dimensional
        grid_position_start = (0, 0)

    # print(grid_position_start)

    index_row = grid_position_start[0]
    index_col = grid_position_start[1]

    # Select player
    for player_number_selected in list_player_number:

        value_position_original = grid_given[index_row][index_col]

        # Place number
        grid_given[index_row][index_col] = player_number_selected

        # Default value
        condition_player_win = False

        # Check Player win Only when there is a valid player
        if player_number_selected != 0:
            condition_player_win = check_win(grid_given, player_number_selected)

        # If player has won, copy grid
        if condition_player_win:
            list_grid_win.append([i.copy() for i in grid_given])

            print(numpy.array(grid_given))
            print()
        else:


            if index_col < len(grid_given[grid_position_start[0]]) -1:
                index_row_new = index_row
                index_col_new = index_col + 1
            else:
                index_row_new = index_row + 1
                index_col_new = 0

            # DFS only when valid selection
            if index_row_new < len(grid_given):
                dfs_tic_tac_toe_all_paths_to_solution(grid_given,
                                                   list_player_number,
                                                   player_number_selected,
                                                   (index_row_new, index_col_new),
                                                   list_grid_win)

        # RESTORE

        # Restore grid
        grid_given[index_row][index_col] = value_position_original

    return list_grid_win

'''

# Brute force, select empty grid number 0 or player number (does not work as intended)
'''
def dfs_tic_tac_toe_all_paths_to_solution(grid_given: List[List[int]],
                                       list_player_number: List[int],
                                       index_player_number_selected: Union[None, int] = None,
                                       grid_position_start: Union[None, Tuple[int, int]] = None,
                                       list_grid_win: Union[None, List[List[List[int]]]] = None):
    """
    Assume Player 0 is empty grid space

    """
    if list_grid_win is None:
        list_grid_win = []

        # _list_player_number_temp = list_player_number.copy()
        # _list_player_number_temp.append(0)
        # list_player_number = list(set(_list_player_number_temp))
        # list_player_number.sort()

        index_player_number_selected = 0

        # Strictly 2 dimensional
        grid_position_start = (0, 0)

    # print(grid_position_start)

    index_row = grid_position_start[0]
    index_col = grid_position_start[1]



    for player_number_selected in (list_player_number[index_player_number_selected], 0):

        value_position_original = grid_given[index_row][index_col]

        # Place number
        grid_given[index_row][index_col] = player_number_selected

        print(numpy.array(grid_given))
        print()

        # Default value
        condition_player_win = False

        # Check Player win Only when there is a valid player
        if player_number_selected != 0:
            condition_player_win = check_win(grid_given, player_number_selected)

        # If player has won, copy grid
        if condition_player_win:
            list_grid_win.append([i.copy() for i in grid_given])

            # print(numpy.array(grid_given))
            # print()


        else:

            if player_number_selected != 0:
                if index_player_number_selected < len(list_player_number) -1:
                    index_player_number_selected += 1
                else:
                    index_player_number_selected = 0

            if index_col < len(grid_given[grid_position_start[0]]) - 1:
                index_row_new = index_row
                index_col_new = index_col + 1
            else:
                index_row_new = index_row + 1
                index_col_new = 0

            # DFS only when valid selection
            if index_row_new < len(grid_given) :


                dfs_tic_tac_toe_all_paths_to_solution(grid_given,
                                                   list_player_number,
                                                   index_player_number_selected,
                                                   (index_row_new, index_col_new),
                                                   list_grid_win)

        # RESTORE

        # Restore grid
        grid_given[index_row][index_col] = value_position_original

    return list_grid_win
    
'''
