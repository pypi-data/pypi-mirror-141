#!/bin/python3
import os
import sys

from itertools import product
from typing import Dict, Optional, Tuple, Any


# import logging


class PrefixNotationException(BaseException):
    "Base Expection to use in the project"
    pass


class Stack:
    def __init__(self):
        """
        Initializing Stack.
        """
        self.stack = []

    def is_empty(self):
        return self.stack == []

    def push(self, stack):
        self.stack.append(stack)

    def pop(self):
        # check for stack underflow
        if self.is_empty():
            print("Stack Underflow!! Calling exit()…")
        return self.stack.pop()


class PrefixNotation:
    def __init__(self):
        """
        Initializing PrefixNotation.
        """

        self.ops = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x // y,
        }
        self.stack = Stack()

    def is_valid_operand(self, item: str) -> bool:
        return item not in list(self.ops.keys())

    def perform_operation(self, exp: str, item1, item2):
        # logging.debug(f"Performing operation exp: {exp} b/w {item1} and {item2}")
        print(f"Performing operation exp: {exp} b/w {item1} and {item2}")
        return self.ops[exp](item1, item2)

    def parse_variables_permutations(
            self, variables_dict: Dict[str, Tuple[int, int]]
    ) -> [Dict[str, int]]:
        """
        Parse list of possible variables permutations
        """
        var_ranges = {}
        for key in variables_dict.keys():
            value = variables_dict[key]
            if type(value) is tuple:
                var_ranges[key] = list(range(value[0], value[1]))
            else:
                var_ranges[key] = [value]
        return [dict(zip(var_ranges.keys(), it)) for it in product(*var_ranges.values())]

    def validate_expression(self, expression: str) -> []:
        """
        Validate expression to check pre conditions

        If checks don't pass then an PrefixNotationException raised

        :param expression: "* 3 4"
        :return: ["4" "3" "*("]
        """
        # TODO: Handle new line
        # if "\n" in expression:
        #     expression = expression.replace("\n", "")
        # if "\t" in expression:
        #     expression = expression.replace("\t", "")

        if " " in expression:

            exprs_list = expression.split(" ")

            valid_exprs = [string for string in exprs_list if string != ""][::-1]

            len_operands = len([it for it in valid_exprs if self.is_valid_operand(it)])
            len_operation = len(valid_exprs) - len_operands

            if (
                    len(valid_exprs) == 0
                    or len_operation == 0
                    or len_operands == 0
                    or len_operands - len_operation != 1
            ):
                raise PrefixNotationException("Invalid expression - Pre check failed")

        return valid_exprs

    def evaluate_operand(self, op, variables: Dict):
        try:
            operand = int(op) if op.isdigit() else variables[op]
            if type(operand) != int or type(op) == float or operand < 0:
                raise PrefixNotationException("Invalid - Only Positive Numeric literal operands are Valid")
        except Exception:
            raise PrefixNotationException("Invalid - Only Positive Numeric literal operands are Valid")

        self.stack.push(operand)

    def prefix_expression(self, expression: [str], expression_variables: Dict) -> int:
        for exp in expression:
            if self.is_valid_operand(exp):
                self.evaluate_operand(exp, expression_variables)
            else:
                self.stack.push(self.perform_operation(exp, self.stack.pop(), self.stack.pop()))

        return self.stack.pop()

    def single_expr_check(self, exp: str) -> Tuple[bool, int]:
        if len(exp) == 1:
            try:
                if type(int(exp)) == int:
                    return True, int(exp)
            except PrefixNotationException as ie:
                print(f"PrefixNotationException: {ie} and return None")
                return False, 0
        else:
            return False, 0

    def evaluate_max_result(self, expression: str, variables: Dict[str, Tuple[int, int]]) -> Optional[int]:

        is_digit, res = self.single_expr_check(expression)
        if is_digit:
            return res
        try:
            valid_expression = self.validate_expression(expression)

            variables_permutations = self.parse_variables_permutations(variables)

            result = max([self.prefix_expression(valid_expression, it) for it in variables_permutations])
            # logging.info(f"Maximum result evaluated: {result}")
            print(f"Maximum result evaluated: {result}")
            return result
        except PrefixNotationException as ie:
            print(f"PrefixNotationException: {ie} and return None")
            return None
        except Exception:
            return None


def max_result_expression(expression: str, variables: Dict[str, Tuple[int, int]]) -> Optional[int]:
    """
    Evaluates the prefix expression and calculates the maximum result for the given variable ranges.

    Expression:
        Supports only 4 operators: +, -, * and /
        Only positive Numeric literal operands are Valid
            1, 2, 99 are valid
            -1, -X433, 0, 012 are not Valid

    Variables can be any integer value: positive, negative or zero

    Operator must have exactly two operands otherwise exp is invalid
    Valid variable is any sequ of chars that does not include whitespaces: Spaces, Tabs, newlines

    Arguments:
        expression: the prefix expression to evaluate.
        variables: Keys of this dictionary may appear as variables in the expression.
            Values are tuples of `(min, max)` that specify the range of values of the variable.
            The upper bound `max` is NOT included in the range, so (2, 5) expands to [2, 3, 4].

    Returns:
        int:  the maximum result of the expression for any combination of the supplied variables.
        None: in the case there is no valid result for any combination of the supplied variables.
    """
    prefix = PrefixNotation()

    return prefix.evaluate_max_result(expression, variables)



# def test_basic_prefix_notation():
#     max_result_expression("+ 1       2", {})
#     assert max_result_expression("0", {}) == None
#     assert max_result_expression("* + 1 2 3 ", {}) == 9
#     assert max_result_expression("9", {}) == 9
#
#     assert max_result_expression("-1", {}) == None
#     assert max_result_expression("+ 6 * - 4 + 2 3 8", {}) == -2
#     max_result_expression("+ 1       2", {})
#     max_result_expression("+ 1       2", {})
#     assert max_result_expression("* + 2 x y", {"x": (0, 2), "y": (2, 4)}) == 9
#     assert max_result_expression("+ 1", {}) == None
#     assert max_result_expression("-+1 5 3", {}) == None

def test_basic_prefix_notation():
    assert max_result_expression("+ 2 5", {}) == 7
    assert max_result_expression("* + 1 2 3", {}) == 9
    assert max_result_expression("- * + 1 2 3 4", {}) == 5
    assert max_result_expression("+ 6 * - 4 + 2 3 8", {}) == -2
    assert max_result_expression("+ 1                       2", {}) == 3

def test_invalid_values():
    assert max_result_expression("+ 1 2 3", {}) is None
    assert max_result_expression("+ 1", {}) is None
    assert max_result_expression("9", {}) is 9
    assert max_result_expression("-+1 5 3", {}) is None
    assert max_result_expression("+ * 7 x z / 5", {"x": (5, 14), "z": (0, 3)}) is None
    assert max_result_expression("", {}) is None
    assert max_result_expression("", {"x": (1, -5)}) is None
    assert max_result_expression("+ x            x", {"x": (1, -5)}) is None
    assert max_result_expression("+ x            x", {"x": (-9, -5)}) is None


def test_prefix_notation_with_variables():
    assert max_result_expression("* + 2 x y", {"x": (0, 2), "y": (2, 4)}) == 9
    assert max_result_expression("+ + 10 x y", {"x": (3, 4), "y": (0, 1)}) == 13
    assert max_result_expression("+ 10 x", {"x": (3, 7)}) == 16

if __name__ == '__main__':
    max_result_expression("1 2", {})
    expression = str(input())
    variables = eval(input())

    res = max_result_expression(expression, variables)

    print(res)
