"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 3/16/2021

Purpose:
    Find the top n amount of items in a given list

Details:
    Time complexity: O(n*m)

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Reference:

"""


import random

start = 0
end = 1000

random.seed(2)

list_ints_random = [random.randint(start,end) for i in range(1000)]

print(list_ints_random)

top_amount = 1000

list_top = [None] * top_amount


for i in list_ints_random:
    for index_j, j in enumerate(list_top):
        if j is None:
            list_top[index_j] = i
            break
        elif i > j:
            for index in range(len(list_top) - 1, index_j, -1):
                list_top[index] = list_top[index-1]
            list_top[index_j] = i
            break

print(list_top)
list_ints_random.sort(reverse=True)
print(list_ints_random)