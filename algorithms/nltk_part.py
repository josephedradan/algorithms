"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 2/15/2021

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:
    FIXME: THERE ARE SOME SPECIAL WORDS IN GUTENBERG SO YOU CAN THREAD!!!!!!!!!

Explanation:

Reference:
    nltk words corpus does not contain “okay”?
        Note:
            Get all the words.
            manywords = words.words() + wordnet.words()  # Paritially correct

        Reference:
            https://stackoverflow.com/questions/44449284/nltk-words-corpus-does-not-contain-okay


    2. Accessing Text Corpora and Lexical Resources
        Notes:
            Project Gutenberg electronic text archive, which contains some 25,000 free electronic books

        Reference:
            https://www.nltk.org/book/ch02.html
"""
import concurrent
import itertools
import math
from collections import defaultdict
from typing import List, Dict, Set, Sequence, Tuple

from Levenshtein import StringMatcher
from josephs_resources.decorators import timer
from miniumum_edit_distance import min_edit_distance_fowers
from nltk.corpus import gutenberg as GUTENBERG
from nltk.corpus import wordnet as WORDNET
from nltk.corpus import words as WORDS


#
# print(len(set(words_gutenberg).union(words_wordnet).union(words_words)))
# print(len(words_all))
#
# sorted(dict_test)
# print(dict_test)
#
# for i in words_wordnet:
#     print(i)


# print(len(gutenberg.words()))
# print(len(words.words()))
# print()
#
# x = set(gutenberg.words())
# print(len(x))
# y = set(words.words())
# print(len(y))
# print()
# print(len(x.intersection(y)))
# print()
# print()
# print(len(wordnet.words()))
# print(len(wordnet_ic.words()))


def get_words() -> Sequence[str]:
    """
    Get words from nltk Corpora and put them all into 1 list

    :return:
    """
    words_gutenberg = GUTENBERG.words()  # Words come from the texts from the Gutenberg electronic text archive
    words_words = WORDS.words()  # Has a bunch of words
    words_wordnet = [word for word in WORDNET.words()]  # Contains words with underscores

    # Combine lists
    words_all = words_words + words_wordnet + words_gutenberg
    # words_all = words_words


    print(",sdfsdf", len(words_all))
    words_all = [i for i in words_words if i.isprintable()]
    print("AAA",len(words_all))



    return words_all


def get_dict_word_count(words: Sequence[str]) -> Dict[str, int]:
    dict_word_frequency = defaultdict(int)

    for word in words:
        dict_word_frequency[word] += 1

    return dict_word_frequency


def dict_to_tuple(dict_given: Dict[str, int]) -> List[Tuple[str, int]]:
    return [(word, count) for word, count in dict_given.items()]


def get_dict_word_frequency(dict_word_count: Dict[str, int], word_count_total: int) -> Dict[str, float]:
    dict_word_frequency = defaultdict(float)

    for word, count in dict_word_count.items():
        dict_word_frequency[word] = count / word_count_total

    return dict_word_frequency


def check_if_word_exists(word: str, set_words: Set[str]):
    if word in set_words:
        return True
    return False


def split_list(list_given, size):
    """

    Reference:
        How do you split a list into evenly sized chunks?
            https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks

    :param list_given:
    :param size:
    :return:
    """
    for i in range(0, len(list_given), size):
        yield list_given[i:i + size]


class WordExistenceChecker:

    @timer
    def __init__(self, words: Sequence[str]):
        self.words = words

        self.words_unique = set(self.words)

        self.words_amount = len(self.words)

        self.words_amount_unique = len(self.words_unique)

        self.dict_word_count = get_dict_word_count(self.words)

        self.dict_word_frequency = get_dict_word_frequency(self.dict_word_count, self.words_amount)

    @timer
    def __call__(self, word: str) -> bool:
        return word in self.words_unique

    @timer
    def check_if_word_exists(self, word: str) -> bool:
        if self.__call__(word):
            print("{} is a complete and correct word in English.".format(word))
        else:
            pass

    def get_min_distance_fowers(self, word: str, set_words: Set[str]) -> List[Tuple[str, int]]:
        list_tuple: List[Tuple[str, int]] = []

        for word_uni in set_words:
            tuple_temp = (word_uni,
                          min_edit_distance_fowers(word, word_uni)[2],
                          self.dict_word_frequency.get(word_uni))

            list_tuple.append(tuple_temp)

        return list_tuple

    def get_min_distance_ztane(self, word: str, set_words: Set[str]) -> List[Tuple[str, int]]:
        list_tuple: List[Tuple[str, int]] = []

        for word_unique in set_words:
            tuple_temp = (word_unique,
                          StringMatcher.distance(word, word_unique),
                          self.dict_word_frequency.get(word_unique))

            list_tuple.append(tuple_temp)

        return list_tuple

    @timer
    def handler(self, word, count_process=1):

        words_split_size = math.ceil(self.words_amount_unique / count_process)

        list_word = list(self.words_unique)

        list_set_word = [i for i in split_list(list_word, words_split_size)]

        if len(list_set_word) != count_process:
            print("Split size is wrong")
            exit(1)

        with concurrent.futures.ProcessPoolExecutor(max_workers=count_process) as executor:
            # Result of each process
            future_callables = []

            # Each list_state_initial gets it's own process...
            for i in range(count_process):
                future = executor.submit(self.get_min_distance_ztane, word, list_set_word[i])

                future_callables.append(future)

            # Add all the results of each process together
            list_tuple_all = list(
                itertools.chain(*[list_solution_partial.result() for list_solution_partial in
                                  concurrent.futures.as_completed(future_callables)]))

        return list_tuple_all


if __name__ == '__main__':
    words_all = get_words()

    word_existence_checker = WordExistenceChecker(words_all)

    # x = word_existence_checker.get_min_distance_fowers("boba")

    x = word_existence_checker.handler("boba")

    x.sort(key=lambda i: i[1])

    # for i in x:
    #     print(i)
