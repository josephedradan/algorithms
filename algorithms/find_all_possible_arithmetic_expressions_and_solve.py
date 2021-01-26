"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 1/13/2021

Purpose:
    Given a list of numbers and a list of operators, Make all possible permutations of the combinations of numbers and
    operators. Then use all possible permutations of the combinations of numbers and operators to find all possible
    ways to evaluate each arithmetic expression.

    Basically, find all permutations of operands and operators and all the ways that each permutation can be
    evaluated and then find each ones corresponding result.

Details:

Description:

Notes:
    Was meant to solve the problem posed in the video titled "Can you solve this puzzle. Make 24 from 6 4 3 and 1."
    (https://www.youtube.com/watch?v=Jnf18uqZRyw)

    Rules:
        You have 4 numbers: 1, 3, 4, and 6 and you have the 4 basic mathematical operators. You have to use all of the
        numbers and some of operators to reach the target of 24.

IMPORTANT NOTES:

Explanation:

    get_dict_key_result_value_set_arithmetic_expression(list_of_numbers, list_of_operators):

        list_of_permutations_numbers = Permutate list_of_numbers

        If treat_list_operators_as_allowed_to_use is True:
            list_of_permutations_operators = Combination with replacement of list_of_operators

        Else If treat_list_operators_as_allowed_to_use is False:
            list_of_permutations_operators = Permutate list_of_operators

        # Big function call here
        list_list_item_mathematical =
            *Interweave Every list_of_permutations_numbers with Every list_of_permutations_operators

        # Create a dict with default value as a set
        dict_result_arithmetic_expression = defaultdict(set)

        For every list_item_mathematical in list_list_item_mathematical:
            list_arithmetic_expression =
                *DFS permutate to get every Arithmetic Expression of the current list_item_mathematical

            For every arithmetic_expression in list_arithmetic_expression:

                # The Key of the dict is the solved result of the arithmetic_expression and the Value is the
                # corresponding arithmetic_expression

                dict_result_arithmetic_expression[arithmetic_expression.get_result()].add(arithmetic_expression)

        return dict_result_arithmetic_expression

Reference:
    Python number base class OR how to determine a value is a number
        https://stackoverflow.com/questions/44756406/python-number-base-class-or-how-to-determine-a-value-is-a-number

    How do I type hint a method with the type of the enclosing class?
        https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class
            Notes:
                from __future__ import annotations
"""

from __future__ import annotations

from collections import defaultdict
from itertools import permutations, combinations_with_replacement, chain
from numbers import Real
from typing import Union, Set, Dict


class ArithmeticExpression:
    """
    Arithmetic Expression that returns a value

    """

    def __init__(self,
                 operand_lhs: Union[Real, ArithmeticExpression],
                 operand_rhs: Union[Real, ArithmeticExpression],
                 operator: str):

        # Operands
        self.operand_lhs = operand_lhs
        self.operand_rhs = operand_rhs

        # Operators
        self.operator = operator

    def __add__(self, other: Union[Real, ArithmeticExpression]) -> ArithmeticExpression:
        return ArithmeticExpression(self, other, "+")

    def __sub__(self, other: Union[Real, ArithmeticExpression]) -> ArithmeticExpression:
        return ArithmeticExpression(self, other, "-")

    def __mul__(self, other: Union[Real, ArithmeticExpression]) -> ArithmeticExpression:
        return ArithmeticExpression(self, other, "*")

    def __truediv__(self, other: Union[Real, ArithmeticExpression]) -> ArithmeticExpression:
        return ArithmeticExpression(self, other, "/")

    def __floordiv__(self, other: Union[Real, ArithmeticExpression]) -> ArithmeticExpression:
        return ArithmeticExpression(self, other, "//")

    def __pow__(self, power: Union[Real, ArithmeticExpression], modulo=None) -> ArithmeticExpression:
        return ArithmeticExpression(self, power, "**")

    def __mod__(self, other: Union[Real, ArithmeticExpression]) -> ArithmeticExpression:
        return ArithmeticExpression(self, other, "%")

    def __str__(self) -> str:
        return "({}{}{})".format(self.operand_lhs, self.operator, self.operand_rhs)

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> str:
        return hash(self.__str__())

    def get_result(self) -> Union[Real, ArithmeticExpression]:
        """
        Returns the result of the Arithmetic Expression

        :return: a number
        """
        if isinstance(self.operand_lhs, ArithmeticExpression):
            lhs: Union[Real, ArithmeticExpression] = self.operand_lhs.get_result()
        else:
            lhs = self.operand_lhs

        if isinstance(self.operand_rhs, ArithmeticExpression):
            rhs: Union[Real, ArithmeticExpression] = self.operand_rhs.get_result()
        else:
            rhs = self.operand_rhs

        return simplify_expression(lhs, rhs, self.operator)

    def __copy__(self) -> Union[Real, ArithmeticExpression]:
        """
        Returns a copy of the current expression.

        Not used

        :return: ArithmeticExpression object
        """
        if isinstance(self.operand_lhs, ArithmeticExpression):
            lhs: Union[Real, ArithmeticExpression] = self.operand_lhs.__copy__()
        else:
            lhs = self.operand_lhs

        if isinstance(self.operand_rhs, ArithmeticExpression):
            rhs: Union[Real, ArithmeticExpression] = self.operand_rhs.__copy__()
        else:
            rhs = self.operand_rhs

        return ArithmeticExpression(lhs, rhs, self.operator)


def get_list_permutation(list_given: list) -> list:
    """
    Return a list permutations of from list_given

    :param list_given: a list given
    :return: list of permutations
    """
    return list(permutations(list_given))


def get_list_combination_with_replacement(list_given: Union[list, set], size) -> list:
    """
    Return a list combinations with replacement from list_given

    :param list_given: a list given
    :return: list of combinations with replacement
    """
    return list(combinations_with_replacement(list_given, size))


def get_list_list_item_mathematical_permutate_operators(list_permutation_operands, list_permutation_operators):
    """
    For every list that is a permutation of operands, interweave every list that is a permutation of operators
    within it.


    Example:
        [1, 2, 3, 4]

        [+, -, *]
        [+, *, -]
        [-, +, *]
        [-, *, +]
        [*, +, -]
        [*, -, +]

    Result:
        [1, +, 2, -, 3, *, 4]
        [1, +, 2, *, 3, -, 4]
        ...
        [1, *, 2, -, 3, +, 4]


    :param list_permutation_operands: list containing a list of operands
    :param list_permutation_operators: list containing a list of operators
    :return: List containing list of alternating operands and operators
    """

    # List containing lists where the inner lists contain mathematical items (operands and operators)
    list_list_item_mathematical = []

    # Loop through list_permutation_operands
    for permutation_operands in list_permutation_operands:
        # print(permutation_operands)

        # Loop through list_permutation_operators
        for permutation_operators in list_permutation_operators:
            # print("\t", permutation_operators)

            # Make a list containing mathematical items
            list_item_mathematical = []

            # Loop through permutation_operands getting the operands and its indices
            for index, operand in enumerate(permutation_operands):

                # Add operand to list_item_mathematical
                list_item_mathematical.append(operand)

                # If the index of the operand is the last one
                if index == len(permutation_operands) - 1:
                    # print("\t\t", list_item_mathematical)

                    # Add a copy of list_item_mathematical into list_list_item_mathematical
                    list_list_item_mathematical.append(list_item_mathematical.copy())

                    break

                # Add operator to list_item_mathematical
                list_item_mathematical.append(permutation_operators[index])

    # Return list of list of item mathematical
    return list_list_item_mathematical


def simplify_list_item_mathematical(list_item_mathematical: list) -> Real:
    """
    Apply mathematical operations on the operands and reduce to 1 value

    Not Used

    :param list_item_mathematical: list of mathematical items
    :return: value
    """

    # Current value
    value = None

    # Current Operator
    operator_current = None

    # If operator is used already
    operator_used = None

    # Loop through every item in list_item_mathematical
    for item in list_item_mathematical:

        # Check if item is a string which should be an operator
        if isinstance(item, str):
            operator_current = item
            operator_used = False

        # If not a string then it's a number
        else:
            # If value is None initially
            if value is None:
                value = item

            # Do math of with the operand and the operator if the current operator is not used
            if operator_used is False:
                value = simplify_expression(value, item, operator_current)
                operator_used = True

    # Return value
    return value


def dfs_permutations_expression_arithmetic_priority(list_item_mathematical, list_arithmetic_expression=None):
    """
    Given a list of mathematical items, find all permutations of the order in which each arithmetic expression,
    a combination of 2 operands and 1 operator, will be evaluated first. Each arithmetic expression created via dfs
    method.

    Notes:
        list_item_mathematical MUST NOT BE A GENERATOR

    Example:
        1 + 2 * 3

    Result:
        ((1 + 2) * 3)
        (1 + (2 * 3))

    # Doctest function call
    >>> dfs_permutations_expression_arithmetic_priority([1, "+", 2, "*", 3])
    [((1+2)*3), (1+(2*3))]

    :param list_item_mathematical: list of mathematical items
    :param list_arithmetic_expression: list of arithmetic expresssions
    :return:
    """

    # Reset variables for reuse of the function
    if list_arithmetic_expression is None:
        list_arithmetic_expression = []

    # Loop through mathematical items in list_item_mathematical
    for index, item in enumerate(list_item_mathematical):

        # If item is a string then it's probably an operator
        if isinstance(item, str):

            # Assume item is an operator
            operator = item

            # lhs and rhs operands
            lhs = list_item_mathematical[index - 1]
            rhs = list_item_mathematical[index + 1]

            # Create a list similar to list_item_mathematical but also hosts a new object called ArithmeticExpression
            list_list_item_mathematical_with_expression_arithmetic = []

            # Loop through mathematical items in list_item_mathematical again
            for index_2, item_2 in enumerate(list_item_mathematical):

                # If index_2 is in [index - 1, index, index + 1]
                if index_2 in [index - 1, index, index + 1]:

                    # If index_2 and index match
                    if index_2 == index:
                        """
                        Create and add the ArithmeticExpression to 
                        list_list_item_mathematical_with_expression_arithmetic
                        """
                        list_list_item_mathematical_with_expression_arithmetic.append(
                            ArithmeticExpression(lhs, rhs, operator))

                    # *Continue only when we pass the three indices where the middle index == index_2
                    continue

                """
                *Add the mathematical item to list_list_item_mathematical_with_expression_arithmetic assuming that
                we have have passed or not have not reached the 3 mathematical items that will turn into a mathematical
                item. 
                """
                list_list_item_mathematical_with_expression_arithmetic.append(item_2)

            # If the size of list_list_item_mathematical_with_expression_arithmetic is 1
            if len(list_list_item_mathematical_with_expression_arithmetic) == 1:
                # print((list_list_item_mathematical_with_expression_arithmetic[0]))

                """
                Add the first object in list_list_item_mathematical_with_expression_arithmetic to 
                list_arithmetic_expression
                
                This means that the item is just 1 Arithmetic Expression object
                """
                list_arithmetic_expression.append(list_list_item_mathematical_with_expression_arithmetic[0])

            # Recursive Call ONLY when there is not 1 item in the list_list_item_mathematical_with_expression_arithmetic
            else:
                dfs_permutations_expression_arithmetic_priority(list_list_item_mathematical_with_expression_arithmetic,
                                                                list_arithmetic_expression)

    return list_arithmetic_expression


def simplify_expression(operand_lhs: Real, operand_rhs: Real, operator: str) -> Real:
    """
    Given lhs operand, rhs operand, and operator, simplify the expression

    Don't use the dict way because it has to check the operands immediately regardless of key being called or not

    WARNING:
        Don't use the dict way because it has to check the operands immediately regardless of key being called or not

    :param operand_lhs: lhs operand
    :param operand_rhs: rhs operand
    :param operator: operator
    :return: result of the expression
    """
    # key = {"+": operand_lhs + operand_rhs,
    #        "-": operand_lhs - operand_rhs,
    #        "*": operand_lhs * operand_rhs,
    #        "/": operand_lhs / operand_rhs
    #        }
    # return key.get(operator)

    # Result is currently None
    result = None

    # Get the result of the operation
    try:
        if operator == "+":
            result = operand_lhs + operand_rhs
        elif operator == "-":
            result = operand_lhs - operand_rhs
        elif operator == "*":
            result = operand_lhs * operand_rhs
        elif operator == "/":
            result = operand_lhs / operand_rhs
        elif operator == "//":
            result = operand_lhs // operand_rhs
        elif operator == "**":
            result = operand_lhs ** operand_rhs
        elif operator == "%":
            result = operand_lhs % operand_rhs

    except ZeroDivisionError as e:
        # print("Cannot do {} / {} ".format(operand_lhs, operand_rhs))
        pass

    except OverflowError as e:
        # print("Result it too big!")
        pass

    except TypeError as e:
        # print("Mathematical operation can be be done with operands {} and {}".format(operand_lhs, operand_rhs))
        pass

    except Exception as e:
        print(e)

    # Return the result
    return result


def get_dict_key_result_value_set_arithmetic_expression(
        list_operands, list_operators,
        treat_list_operators_as_allowed_to_use=False) -> Dict[Real, Set[ArithmeticExpression]]:
    """
    Given a list of operands and a list of operators, find all possible permutations of these mathematical items, then
    solve.

    :param list_operands: list of operands
    :param list_operators: list of operators
    :param treat_list_operators_as_allowed_to_use: Treat list of operators as operators that the algorithm is allowed
    to use rather than what the algorithm should use once (Not at least once).
    :return: dictionary of result of the expression and the expression
    """

    """
    List of list of operands as permutations
    
    Notes:
        Alternatively, permutations can be called instead of get_list_permutation which should be less memory intensive
        optimal.
    
    
    """
    permutations_operands = permutations(list_operands)

    # List of list of operators as combinations with replacement
    if treat_list_operators_as_allowed_to_use:

        """
        Get every combination with replacement of operators within list_operators
        
        Notes:
            Alternatively, combinations_with_replacement can be called here instead because the set function below this
            variable will make this not exhaustible.
        
        """
        list_list_operators_every_combination = combinations_with_replacement(set(list_operators),
                                                                              len(list_operands) - 1)

        """
        *** Get every permutation of of every combination from list_list_operators_every_combination into 1 chain object
        of type iterable, then remove duplicate permutations by putting them into a set.
        
        """
        list_list_operators = set(chain(*[permutations(i) for i in list_list_operators_every_combination]))

        # print(set(list_list_operators))
    # List of list of operators as permutations
    else:

        # list_list_operators needs to be not exhaustible because it will be reused over again
        list_list_operators = get_list_permutation(list_operators)

    # Get list of list of mathematical items
    list_list_item_mathematical = get_list_list_item_mathematical_permutate_operators(permutations_operands,
                                                                                      list_list_operators)

    # Default dict of Key result of expression amd Value set that contains Arithmetic Expression
    dict_result_arithmetic_expression = defaultdict(set)

    # For list of mathematical items
    for list_item_mathematical in list_list_item_mathematical:

        # Get a list Arithmetic Expressions which are objects represent a list_item_mathematical
        list_arithmetic_expression = dfs_permutations_expression_arithmetic_priority(list_item_mathematical)

        # For every Arithmetic Expression
        for arithmetic_expression in list_arithmetic_expression:
            # print(f"Arithmetic Expression: {arithmetic_expression}")
            # print(f"Arithmetic Expression Result: {arithmetic_expression.get_result()}")

            # Add result of Arithmetic Expression as a Key and the Arithmetic Expression its set
            dict_result_arithmetic_expression[arithmetic_expression.get_result()].add(arithmetic_expression)

    # Return dict_result_arithmetic_expression
    return dict_result_arithmetic_expression


def solve_problem(target=24):
    """
    Solve the problem posed in the video "Can you solve this puzzle. Make 24 from 6 4 3 and 1."
    (https://www.youtube.com/watch?v=Jnf18uqZRyw)

    :param target: Value to reach
    :return: None
    """
    operands = [6, 4, 3, 1]
    operators = ["+", "-", "*", "/"]

    dict_results = get_dict_key_result_value_set_arithmetic_expression(operands, operators,
                                                                       treat_list_operators_as_allowed_to_use=True)

    set_solution = dict_results.get(target, None)

    print(f"Target is {target}")
    if set_solution is None:
        print("Target could not be found!")
        print("Solution does not exist")
    else:
        print("Possible solutions are:")
        for expression in set_solution:
            print("\t{} = {}".format(expression, expression.get_result()))


def test_example():
    """
    Possibly show all Arithmetic Expressions and their corresponding result

    :return: None
    """
    operands = [6, 4, 3, 1]
    operators = ["+", "-", "*", "/", "**", "//", "%"]

    dict_results = get_dict_key_result_value_set_arithmetic_expression(operands, operators,
                                                                       treat_list_operators_as_allowed_to_use=True)

    total_expressions = 0

    for key, value in dict_results.items():
        print(key)
        for expression in value:
            total_expressions += 1
            print("\t{}".format(expression))
        print()

    print(f"Total solutions: {len(dict_results)}")
    print(f"Total expressions: {total_expressions}")


if __name__ == '__main__':
    solve_problem()

    print("\n" + 100 * "-" + "\n")

    test_example()
