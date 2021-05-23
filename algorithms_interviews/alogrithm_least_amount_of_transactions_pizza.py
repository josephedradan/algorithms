"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 5/22/2021

Purpose:
    Solve algorithm challenge given in a tiktok video

Details:

Description:

Notes:

Question:
    Friends go to Italy, you guys only eat pizza, pizza is bought using cash only, not everyone one has cash.
    If any friend does not have cash, another friend will pay for them (only 1 will do that).

    Create an algorithm to find out how much each person needs to pay everyone back to cover all the pizza for the trip
    using the fewest number of transactions.

IMPORTANT NOTES:

Explanation:

Reference:
    https://www.tiktok.com/@dohyunkim0297/video/6964838170320063749?_d=secCgYIASAHKAESMgowCUIfLd1VGmedxOJEqWSpeLdUj8lnyFoK%2BmyYHpjMZ6PbIHT%2FNvYV8cm0LokS5Ca%2FGgA%3D&language=en&preview_pb=0&sec_user_id=MS4wLjABAAAAPJLuTSIbY8g46DGFx-u1FVgT38I_BWT7XCvx7oB5m5A52ophuJBdh7zRlP0vtMtD&share_app_id=1233&share_item_id=6964838170320063749&share_link_id=F09EF8B7-5569-4CDB-92E1-F865C4AA099B&source=h5_m&timestamp=1621679285&tt_from=copy&u_code=deibje2575afb6&user_id=6876919040338936838&utm_campaign=client_share&utm_medium=ios&utm_source=copy&_r=1&is_copy_url=1&is_from_webapp=v1

"""
import math
import random
from collections import defaultdict
from itertools import permutations


def generate_data():
    """
    Given friends, generate data where a friend owes another friend with the amount they owe

    Example:
        (A, B) 10  # A owes B $10

    :return:
    """
    list_friend = ["A", "B", "C", "D", "E"]

    list_permutation = list(permutations(list_friend, 2))

    print("All possible permutations of Who owes Who")
    for i in list_permutation:
        print(i)
    print()

    list_how_much_0_owes_1_with_price = []

    for i in range(100):
        index_random = (random.randint(0, len(list_permutation) - 1))

        pair_random = list_permutation[index_random]

        list_how_much_0_owes_1_with_price.append((pair_random, random.randint(1, 100)))

    print("List of Who owes Who with the amount they owe")
    for pair_with_amount_owed in list_how_much_0_owes_1_with_price:
        print(pair_with_amount_owed)
    print()

    return list_how_much_0_owes_1_with_price, list_friend


def algorithm():
    """
    Algorithm to find the least amount of transactions

    IMPORTANT NOTES:
        THIS ALGORITHM IS NOT GENERALIZED

    Time Complexity:
        ~ 2 * n * (Time it takes to create a set) * 2 * (Time it takes to create a Dict)

        O(2n)

    :return:
    """
    list_how_much_0_owes_1_with_amount_owed, list_friend = generate_data()

    print("#" * 100)
    print("Algorithm")
    print("#" * 100)
    print()

    dict_k_pair_v_owed = defaultdict(int)

    # Algorithm part 1
    for i in list_how_much_0_owes_1_with_amount_owed:
        dict_k_pair_v_owed[i[0]] += i[1]

    # Print to show work
    print("Dict of Who owes Who (total amount owed)")
    for pair, amount_owed in dict_k_pair_v_owed.items():
        print(pair, amount_owed)
    print()

    dict_k_pair_v_owed_total = dict()

    set_frozenset_used = set()

    # Algorithm part 2
    for pair, amount_owed in dict_k_pair_v_owed.items():

        frozenset_pair = frozenset(pair)

        if frozenset_pair not in set_frozenset_used:
            set_frozenset_used.add(frozenset_pair)
            dict_k_pair_v_owed_total[pair] = amount_owed
            continue

        else:

            pair_reversed = tuple(reversed(pair))

            value_of_pair_reversed = dict_k_pair_v_owed_total.get(pair_reversed)

            if amount_owed > value_of_pair_reversed:
                dict_k_pair_v_owed_total.pop(pair_reversed)
                dict_k_pair_v_owed_total[pair] = amount_owed - value_of_pair_reversed

            else:
                dict_k_pair_v_owed_total[pair_reversed] = dict_k_pair_v_owed_total[pair_reversed] - amount_owed

    # Print to show solution
    print("How much money friend index 0 owes friend index 1")
    for pair, amount_owed in dict_k_pair_v_owed_total.items():
        print(pair, amount_owed)
    print()

    print("Proof that the Maximum amount transactions needed total is <= Combinations of size 2")
    print("Combination: {} CHOOSE {} = {}".format(len(list_friend), 2,
                                                  math.comb(len(list_friend), 2)))
    print("Size of the result of my algorithm {}".format(len(dict_k_pair_v_owed_total)))


if __name__ == '__main__':
    algorithm()
