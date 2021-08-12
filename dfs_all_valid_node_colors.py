"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 4/27/2021

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Reference:

"""
from collections import defaultdict
from typing import Dict, Set, List, Union

from python_code_recorder.code_recorder import CodeRecorder

algorithm_recorder = CodeRecorder()

counter = 0


@algorithm_recorder.decorator_wrapper_callable
def dfs_all_valid_node_colors(dict_node_nodes: Dict[int, Set],
                              node_current: int,
                              list_color: List[str],
                              dict_node_color: Union[Dict[int, str], None] = None,
                              dict_node_node_traveled: Union[Dict[int, Set], None] = None,
                              set_node_traveled: Union[Set[int], None] = None,
                              ):
    """
    Recursive call to find all valid node colors based on the adjacent nodes.

    :param dict_node_nodes:
    :param node_current:
    :param list_color:
    :param dict_node_color:
    :param dict_node_node_traveled:
    :param set_node_traveled:
    :return:
    """
    if dict_node_color is None:
        dict_node_color = {}
        dict_node_node_traveled = defaultdict(set)
        # dict_node_node_traveled = dict_node_nodes.copy()
        set_node_traveled = set()

    # Select color
    for color in list_color:
        """
        Check if an adjacent node has the same color (Should prevent current node from having the same color 
        as an adjacent node. 
        """
        if does_adjacent_have_this_color(color, node_current, dict_node_nodes, dict_node_color):
            continue

        # Assign current color to current node
        dict_node_color[node_current] = color

        # print(node_current, "\t", dict_node_color)

        if len(dict_node_color) == len(dict_node_nodes):
            print(dict_node_color)
            # print(sorted(dict_node_color.items()))
            # return  # If you return, you will cut off a branch while it's still searching
            pass

        # For every adjacent node the current node has
        for node_adjacent in dict_node_nodes[node_current]:
            # print(str(set_node_traveled))
            # print(node_adjacent, dict_node_color.get(node_adjacent, None))

            """
            If the adjacent node has not been traversed
            """
            if node_adjacent not in set_node_traveled:
                global counter
                counter += 1

                # Add node to be marked as traversed
                set_node_traveled.add(node_adjacent)

                dfs_all_valid_node_colors(dict_node_nodes, node_adjacent, list_color,
                                          dict_node_color, dict_node_node_traveled, set_node_traveled)

                # Remove node from being marked as traversed
                set_node_traveled.remove(node_adjacent)

            # Testing, requires visuals to understand

            # ??? counter == 796571 (dict_node_node_traveled = dict_connections.copy(), LIST_COLORS = ["R", "B", "G"])
            # if node_adjacent in dict_node_node_traveled[node_current]:
            #     global counter
            #     counter += 1
            #
            #     dict_node_node_traveled[node_current].remove(node_adjacent)
            #     dfs_all_valid_node_colors(dict_node_nodes, node_adjacent, list_color,
            #               dict_node_color, dict_node_node_traveled, set_node_traveled)
            #     dict_node_node_traveled[node_current].add(node_adjacent)

            # ??? counter == 153699 (dict_node_node_traveled = defaultdict(set), LIST_COLORS = ["R", "B", "G"])
            # if node_adjacent not in dict_node_node_traveled[node_current]:
            #     global counter
            #     counter += 1
            #
            #     dict_node_node_traveled[node_current].add(node_adjacent)
            #     dfs_all_valid_node_colors(dict_node_nodes, node_adjacent, list_color,
            #               dict_node_color, dict_node_node_traveled, set_node_traveled)
            #     dict_node_node_traveled[node_current].remove(node_adjacent)

        dict_node_color.pop(node_current, None)


def does_adjacent_have_this_color(color, node_current, dict_node_nodes, dict_node_color):
    """
    Loop over a node's adjacent nodes and check their color to see if their color matches
    the given color.

    :param color:
    :param node_current:
    :param dict_node_nodes:
    :param dict_node_color:
    :return:
    """
    # Look at adjacent node and check their color
    for node_adjacent in dict_node_nodes[node_current]:

        # If adjacent node's color == color given
        if dict_node_color.get(node_adjacent) == color:
            return True
    return False


def main():
    dict_connections: Dict[int, set] = {1: {2, 3},
                                        2: {1, },
                                        3: {1, 4, 5},
                                        4: {3, 5},
                                        5: {4, 3}}

    list_colors = ["R", "B", "G", "Y"]
    # list_colors = ["R", "B", "G"]

    dfs_all_valid_node_colors(dict_connections, 1, list_colors)
    print(counter)

    # algorithm_recorder.scope_recorder_printer.print_call_order_event_simple()


if __name__ == '__main__':
    main()
