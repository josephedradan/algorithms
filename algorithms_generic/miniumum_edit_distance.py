"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 2/15/2021

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Reference:
    Minimum Edit Distance Algorithm in Python in 2020 (EXPLAINED)
        Notes:
            Using Rylan Fowers' minimum edit distance algo

        Reference:
            https://www.youtube.com/watch?v=AY2DZ4a9gyk
"""

import numpy as np
import pandas as pd


def min_edit_distance_fowers(source, target):
    list_source_char = [c for c in source]
    list_target_char = [c for c in target]

    # Make np_array
    np_array = np.zeros((len(source), len(target)))

    # Target is 0th row
    np_array[0] = [c for c in range(len(target))]

    # Source is the 0th col ([index_row_all, index_column])
    np_array[:, 0] = [c for c in range(len(source))]

    """
    Solve the [1,1] location if necessary
    
    If the char at index 1 of both target and source are different the amount of edits needed to achieve the target
    string is the min of the top and left indices values around the [1,1]
    
    """

    try:
        # if target[1] != source[1]:
        #     np_array[1, 1] = 2

        # For item index in row, start on index 1 (Target is the row)
        for i in range(1, len(target)):

            # for item index in col, start on index 1 (Source is the column)
            for j in range(1, len(source)):

                # If the respective chars from i and j for the source and target are NOT the same
                if target[i] != source[j]:

                    """
                    Change the value at the given position given i and j
                    
                    Note that i and j are switched 
                    
                    """
                    np_array[j, i] = min(np_array[j - 1, i], np_array[j, i - 1]) + 1

                # If the respective chars from i and j for the source and target are the same
                else:
                    np_array[j, i] = np_array[j - 1, i - 1]

    except Exception as e:
        print(e)
        print("S:{:<20} T:{:<20} j{:<5} i:{:<5} ".format(source, target, j, i))

    # Make pandas DF of the np array
    data_frame = pd.DataFrame(np_array, columns=list_target_char, index=list_source_char)

    return np_array, data_frame, np_array[-1, -1]


if __name__ == '__main__':
    print(min_edit_distance_fowers("joseph", "edradan")[0])
    print(min_edit_distance_fowers("joseph", "edradan")[1])
    print(min_edit_distance_fowers("joseph", "edradan")[2])
    print()

    print(min_edit_distance_fowers("#joseph", "#joe")[0])
    print(min_edit_distance_fowers("#joseph", "#joe")[1])
    print(min_edit_distance_fowers("#joseph", "#joe")[2])
    print()

    print(min_edit_distance_fowers("$BCDE", "#DE")[0])
    print(min_edit_distance_fowers("$BCDE", "#DE")[1])
    print(min_edit_distance_fowers("$BCDE", "#DE")[2])
    print()
