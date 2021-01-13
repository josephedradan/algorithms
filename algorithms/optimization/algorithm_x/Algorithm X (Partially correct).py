"""
3/10/20

Purpose:
    Test my implementation of Algorithm X

Notes:
    Partially correct algorithm

Reference:
    https://www.wikiwand.com/en/Knuth%27s_Algorithm_X

"""
from typing import List, Set, Dict

X = {1, 2, 3, 4, 5, 6, 7}

Y = {
    1: {'A', 'B'},
    2: {'E', 'F'},
    3: {'D', 'E'},
    4: {'A', 'B', 'C'},
    5: {'C', 'D'},
    6: {'D', 'E'},
    7: {'A', 'C', 'E', 'F'}}  # type: Dict[int, Set]


def test(collection: Dict[int, Set[str]], solution: list):
    collection_transformed = transform_collection(collection)  # type: Dict[str, Set[int]]

    smallest = smallest_amount_of_ones(collection)

    collection_letter_numbers_new = collection_transformed.copy()

    if not collection:
        return solution

    for key_number, value_letters in collection.items():
        if len(value_letters) == smallest:
            for value_letter in value_letters:
                temp_set_numbers = collection_transformed[value_letter]  # set of numbers

                temp_set_letters = set()
                for number in temp_set_numbers:
                    for letter in collection[number]:
                        temp_set_letters.add(letter)

                for letter in temp_set_letters:
                    del collection_letter_numbers_new[letter]

                solution.append(value_letter)

                answer = test(transform_collection(collection_letter_numbers_new),
                              solution.copy())

                return answer


def smallest_amount_of_ones(dict_given: dict) -> int:
    smallest = None

    for key, value in dict_given.items():
        if smallest is None:
            smallest = len(value)

        temp = len(value)
        if temp < smallest:
            smallest = temp

    return smallest


def transform_collection(collection: Dict) -> Dict:
    temp = {}  # type: Dict[str, Set]

    for key, value in collection.items():
        for row_name in value:
            if temp.get(row_name, False) is False:
                temp[row_name] = set()
            temp[row_name].add(key)

    return temp


Z = transform_collection(Y)

if __name__ == '__main__':
    # print(smallest_amount_of_ones(Y))
    # print(transform_collection(transform_collection(Y)))

    print(test(Y, []))
