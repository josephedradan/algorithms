"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 4/22/2021

Purpose:
    Using hashes to solve the N Queens problem

Details:

Description:

Notes:

Time Complexity:
    If n == length of row and m == length of column

        ~ Time Complexity:
            O((n*m) * (p) * (1 + 1 + 1 + 1))
        Notes
            1. n*m = traverse grid
            2. p = successful queen placement
            3. 1 = check if hash of column index in set column index
            4. 1 = check if hash of row index in set row index
            5. 1 = check if (x, y)'s bot to top b value in set bot to top b value
            6. 1 = check if (x, y)'s tot to bop b value in set tot to bop b value

            Does not include the solutions lists

Space Complexity:
    If n == length of row and m == length of column

        Space Complexity:
            O(n*m + a + b + c + d)

            Where a, b, c, d are less than n*m

        Notes:
            1. n*m = the grid
            2. a = set column index
            2. b = set row index
            2. c = set bot to top b value
            2. d = set tot to bop b value

            Does not include the solutions lists

IMPORTANT NOTES:

Explanation:

Reference:

"""
from typing import List, Set, Union, Tuple


def validator(x: int, y: int,
              set_column_used: Union[Set[int], None],
              set_row_used: Union[Set[int], None],
              set_b_initial_bot_top: Union[Set[int], None],
              set_b_initial_top_bot: Union[Set[int], None]):
    """
    Check if the placement of a queen is possible at the given x and y values based on the sets that describe the
    placement of other queens and their threatening positions.

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

    :param x:
    :param y:
    :param set_column_used:
    :param set_row_used:
    :param set_b_initial_bot_top:
    :param set_b_initial_top_bot:
    :return:
    """

    # Check if column index has a queen
    if x in set_column_used:
        return False

    # Check if row index has a queen
    if y in set_row_used:
        return False

    """
    Using two y = mx + b equations to represent the diagonals where a queen can attack from, if we rearrange the 
    equations in terms of b, we can represent an entire diagonal because the b value is a vertical shifter of the
    diagonal. Given the x and y values, the b value that results from the rearrangement will give us a constant
    value that represents the entire diagonal. 
    
    Basically, if we solve for b in b = y - mx, we get a constant value, this constant value will be the same across an
    entire diagonal. This means that if we are given an x and y position and we solve for a b value for either diagonal 
    and that b value is found in its corresponding set (set_b_initial_bot_top or set_b_initial_top_bot), we know that
    we cannot place a queen at x, y because a queen is attacking this diagonal.
    
    """
    b_initial_bot_top = (y - (-1 * x))
    b_initial_top_bot = (y - (1 * x))

    # Check if b value for diagonal bot to top is in set_b_initial_bot_top
    if b_initial_bot_top in set_b_initial_bot_top:
        return False

    # Check if b value for diagonal top to bot is in set_b_initial_top_bot
    if b_initial_top_bot in set_b_initial_top_bot:
        return False

    # Can place queen at x,y
    return True


def dfs_n_queens_hash(board: List[List[int]],
                      width: int,
                      height: int,
                      queens_on_board: int = None,
                      set_index_column_used: Union[Set[int], None] = None,
                      set_index_row_used: Union[Set[int], None] = None,
                      set_b_initial_bot_top: Union[Set[int], None] = None,
                      set_b_initial_top_bot: Union[Set[int], None] = None,
                      list_solutions: Union[List[List[List[List[int]]]], None] = None,
                      list_solutions_unique: Union[List[Set[Tuple[Tuple[int]]]], None] = None):
    """
    List of solutions
        list_solutions[list_solution[solution[row[int]]]]

    list_solutions_unique
        list_solutions_unique[set_solution_unique[tuple_solution[tuple_row[int]]]]

    Recursive call to find all possible queen positions where queens don't threaten each other

    :param board:
    :param width:
    :param height:
    :param queens_on_board:
    :param set_index_column_used:
    :param set_index_row_used:
    :param set_b_initial_bot_top:
    :param set_b_initial_top_bot:
    :param list_solutions:
    :param list_solutions_unique:
    :return:
    """

    # Allows for multiple calls of this function by resetting default arguments (not part of algorithm)
    if queens_on_board is None:
        queens_on_board = 0
        set_index_column_used = set()
        set_index_row_used = set()
        set_b_initial_bot_top = set()
        set_b_initial_top_bot = set()
        list_solutions = []
        list_solutions_unique = []

    # Loop over board
    for y in range(height):
        for x in range(width):

            # If you reach the end of the board
            if x == width - 1 and y == height - 1:
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

            # Check if placing a queen a given x, y will not put the queen in check
            if validator(x, y, set_index_column_used, set_index_row_used, set_b_initial_bot_top, set_b_initial_top_bot):
                """
                Using two y = mx + b equations to represent the diagonals where a queen can attack from, if we 
                rearrange the equations in terms of b, we can represent an entire diagonal because the b value is 
                a vertical shifter of the diagonal. Given the x and y values, the b value that results from the 
                rearrangement will give us a constant value that represents the entire diagonal. 

                Basically, if we solve for b in b = y - mx, we get a constant value, this constant value will be the 
                same across an entire diagonal. This means that if we are given an x and y position and we solve 
                for a b value for either diagonal and that b value is found in its corresponding set 
                (set_b_initial_bot_top or set_b_initial_top_bot), we know that we cannot place a queen at x, y 
                because a queen is attacking this diagonal.

                """
                b_initial_bot_top = (y - (-1 * x))
                b_initial_top_bot = (y - (1 * x))

                # Place queen
                board[y][x] = 1
                queens_on_board += 1

                # Add information about the placed queen to the sets
                set_index_column_used.add(x)
                set_index_row_used.add(y)
                set_b_initial_top_bot.add(b_initial_top_bot)
                set_b_initial_bot_top.add(b_initial_bot_top)

                # Recursive call with the new queen
                dfs_n_queens_hash(board, width, height, queens_on_board,
                                  set_index_column_used,
                                  set_index_row_used,
                                  set_b_initial_bot_top,
                                  set_b_initial_top_bot,
                                  list_solutions,
                                  list_solutions_unique)

                # Remove information about the placed queen to the sets
                set_b_initial_bot_top.remove(b_initial_bot_top)
                set_b_initial_top_bot.remove(b_initial_top_bot)
                set_index_row_used.remove(y)
                set_index_column_used.remove(x)

                # Remove queen
                queens_on_board -= 1
                board[y][x] = 0

    return list_solutions, list_solutions_unique


def check_if_diagonal_will_have_same_b_value():
    """
    A simple print of a np array to show that each diagonal has the same b value
    to check if a queen is attacking that diagonal.

    :return:
    """
    matrix_1 = [[i for i in range(10)] for j in range(10)]
    matrix_2 = [[i for i in range(10)] for j in range(10)]

    for row in range(10):
        for col in range(10):
            b_initial_bot_top = (row - (-1 * col))
            b_initial_top_bot = (row - (1 * col))

            matrix_1[row][col] = b_initial_bot_top
            matrix_2[row][col] = b_initial_top_bot

    import numpy as np

    print(np.array(matrix_1))
    print()
    print(np.array(matrix_2))


if __name__ == '__main__':

    # check_if_diagonal_will_have_same_b_value()

    # Change this to change size
    size_grid_given = 4

    # Board
    board_given = [[0 for _ in range(size_grid_given)] for i in range(size_grid_given)]

    # Call to get solutions
    list_solutions, list_solutions_unique = dfs_n_queens_hash(board_given, size_grid_given, size_grid_given)

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
