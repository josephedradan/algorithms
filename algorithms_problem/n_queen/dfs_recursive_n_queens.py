"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 4/22/2021

Purpose:
    Solve the N Queens problem based on SFSU CSC 510's lecture on 4/22/2021

Details:

Description:

Notes:
    I do not recommend making a bigger grid, it will take a long time...

    For a diagonal checker, don't check for slope to be the same because that requires a loop.

Time Complexity:
    If n == length of row and m == length of column

        ~ Time Complexity:
            O((n*m) * (p) * (n + m + m))
        Notes
            1. n*m = traverse grid
            2. p = successful queen placement
            3. n = check column (traverse through row)
            4. m = check row (traverse through columns)
            5. m = check diagonals (traverse through columns)

            Does not include the solutions lists

Space Complexity:
    If n == length of row and m == length of column

        ~ Space Complexity:
            O(n*m)

        Notes:
            1. n*m = the grid

            Does not include the solutions lists

IMPORTANT NOTES:

Explanation:

Reference:

"""
from typing import List, Union, Set, Tuple

FORMAT_PRINT = "{:<12}{:<12}{}{:<12}{:<12}"


def is_column_safe(board: List[List[int]], x: int) -> bool:
    """
    Loop over rows, lock down column (x) and check if board_given[row][x] == 1
    If board_given[row][x] == 1 then you can't place anything in that position

    :param board:
    :param x:
    :return:
    """
    for row in range(size_grid_given):
        if board[row][x] == 1:
            return False
    return True


def is_row_safe(board: List[List[int]], y: int) -> bool:
    """
    Loop over columns, lock down row (y) and check if board_given[y][column] == 1
    If board_given[y][column] == 1 then you can't place anything in that position

    :param board:
    :param y:
    :return:
    """
    for column in range(size_grid_given):
        if board[y][column] == 1:
            return False
    return True


def are_diagonals_safe(board: List[List[int]], y_initial: int, x_initial: int, size: int) -> bool:
    """
    Loop over columns and check if it's valid to place a queen at (x_initial, y_initial)

    Notes:
        Board is inverted so read the below to understand:
            top means absolute top (relative to you viewing the grid)
            bot means absolute bottom (relative to you viewing the grid)

            Basically, everytime you think of the grid, think of it inverted over the x axis

        Use equation:
            y = mx + b

            b value (b = y - mx)
                from bottom to top
                    b_initial_bot_top = (y_initial - (-(1/1) * x_initial))
                from top to bottom
                    b_initial_top_bot = (y_initial - ((1/1) * x_initial))

            Function to get row (y) based on column (x) using (y = mx + b)
                from bottom to top
                    func_get_row_bot_top = (-(1/1)* x) + b_initial_bot_top

                from top to bottom
                    func_get_row_top_bot = ((1/1)* x) + b_initial_top_bot

    :param board:
    :param y_initial:
    :param x_initial:
    :param size:
    :return:
    """
    # b value in y = mx + b
    b_initial_bot_top = (y_initial - (-1 * x_initial))
    b_initial_top_bot = (y_initial - (1 * x_initial))

    # print("{:<15}{}".format(f"y_initial:{y_initial}", f"x_initial:{x_initial}"))
    # print(FORMAT_PRINT.format("row b->t", "col", " " * 5, "row t->b", "col"))

    """
    Functions to calculate row based on b value and column (x_0), also does not follow PEP 8 with lambdas
    
    Negative values that result from the below functions will wrap around the row.
    Positive values that result from the below functions that are greater than the size of the row will
    crash. Conditions must be in place to prevent this.
    """
    func_get_row_bot_top = lambda x_0: (-1 * x_0) + b_initial_bot_top
    func_get_row_top_bot = lambda x_0: (1 * x_0) + b_initial_top_bot

    for column in range(len(board)):
        # print(FORMAT_PRINT.format(func_get_row_bot_top(column),
        #                           column,
        #                           " " * 5,
        #                           func_get_row_top_bot(column),
        #                           column))

        value_row_y_1 = func_get_row_bot_top(column)

        if 0 <= value_row_y_1 < size and board[value_row_y_1][column] == 1:
            # print()
            return False

        value_row_y_2 = func_get_row_top_bot(column)

        if 0 <= value_row_y_2 < size and board[value_row_y_2][column] == 1:
            # print()

            return False

    # print()
    return True


def validator(board: List[List[int]], size: int, x: int, y: int) -> bool:
    """
    Do all the board validations for queen placement in one function

    :param board:
    :param size:
    :param x:
    :param y:
    :return:
    """
    if not is_row_safe(board, y):
        return False
    elif not is_column_safe(board, x):
        return False
    elif not are_diagonals_safe(board, y, x, size):
        return False
    return True


def dfs_n_queens(board: List[List[int]],
                 size: int,
                 queens_on_board: Union[int, None] = None,
                 list_solutions: Union[List[List[List[List[int]]]], None] = None,
                 list_solutions_unique: Union[List[Set[Tuple[Tuple[int]]]], None] = None):
    """
    List of solutions
        list_solutions[list_solution[solution[row[int]]]]

    list_solutions_unique
        list_solutions_unique[set_solution_unique[tuple_solution[tuple_row[int]]]]

    Recursive call to find all possible queen positions where queens don't threaten each other

    The reason why I pass the size, is because you could modify this function to support
    any grid dimensions such as 4x10, 3x32, etc...

    Notes:
        Not optimized

    :param board:
    :param size:
    :param queens_on_board:
    :param list_solutions:
    :param list_solutions_unique:
    :return:
    """

    # Allows for multiple calls of this function by resetting default arguments (not part of algorithm)
    if list_solutions is None:
        queens_on_board = 0
        list_solutions = []
        list_solutions_unique = []

    # Loop through board
    for y in range(size_grid_given):
        for x in range(size_grid_given):

            # If you reach the end of the board
            if x == size - 1 and y == size - 1:
                if queens_on_board > len(list_solutions) - 1:

                    # Add more sets and lists based on the amount of queens on the board
                    for i in range(queens_on_board + 1 - len(list_solutions)):
                        list_solutions.append([])
                        list_solutions_unique.append(set())

                # Copy solution to corresponding index queens_on_board
                list_solutions[queens_on_board].append([row.copy() for row in board])

                """
                Copy Unique solution to corresponding index queens_on_board 
                (Use tuple because they are hashable and because () is a generator so you need to explicitly call tuple)
                """
                list_solutions_unique[queens_on_board].add(tuple((tuple(row.copy()) for row in board)))

            # Check if valid position to place queen
            if validator(board, size, x, y):
                # Place queen
                board[y][x] = 1
                queens_on_board += 1

                # Recursive call with the new queen
                dfs_n_queens(board, size, queens_on_board, list_solutions, list_solutions_unique)

                # Remove queen
                queens_on_board -= 1
                board[y][x] = 0

    return list_solutions, list_solutions_unique


if __name__ == '__main__':

    # Change this to change size
    size_grid_given = 4

    # Board
    board_given = [[0 for _ in range(size_grid_given)] for i in range(size_grid_given)]

    # Call to get solutions
    list_solutions, list_solutions_unique = dfs_n_queens(board_given, size_grid_given)

    # Print all possible Queen positions where queens don't threaten each other
    print("All possible Queen positions where queens don't threaten each other for grid size {} "
          "(Will print everything regardless of uniques)".format(size_grid_given))

    print("Number of solutions total:", len([i for i in list_solutions for j in i]))
    for i, e in enumerate(list_solutions):
        print("Number of solutions for {} Queens: {}".format(i, len(e)))

    print()
    for i, solutions in enumerate(list_solutions):
        for solution in solutions:
            print("Amount of Queens:", i)
            for row in solution:
                print(row)
            print()

    print("\n{}".format(100 * "#"))

    # Print all possible Unique Queen positions where queens don't threaten each other
    print("All possible Unique Queen positions where queens don't threaten each "
          "other for grid size {}".format(size_grid_given))

    print("Number of Unique solutions:", len([i for i in list_solutions_unique for j in i]))
    for i, e in enumerate(list_solutions_unique):
        print("Number of Unique solutions for {} Queens: {}".format(i, len(e)))

    print()
    for i, solutions in enumerate(list_solutions_unique):
        for solution in solutions:
            print("Amount of Queens:", i)
            for row in solution:
                print(row)
            print()
