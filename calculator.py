#!/usr/bin/env python3
"""
Simple CLI Calculator
----------------------
A command-line calculator that supports chaining many numbers and
operations together (addition, subtraction, multiplication, division,
exponentiation, modulo, percentage, and square root) into a single
expression. All the steps are collected first, and only once the user
finishes the expression is the whole thing calculated and the final
result printed.

Run it with:
    python calculator.py
"""

from math import sqrt
from sys import exit
from time import sleep

# Map of supported two-operand (binary) operators to functions.
# Using a dictionary like this makes it easy to add new operators later
# without needing a long chain of if/elif statements.
OPERATIONS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,             # will raise ZeroDivisionError if b == 0
    "**": lambda a, b: a ** b,           # exponentiation
    "%": lambda a, b: a % b,             # modulo (remainder)
    "%of": lambda a, b: (a / 100) * b,   # percentage, e.g. "20 %of 200" -> 40
}

# Map of supported one-operand (unary) operators to functions.
# These apply to the running result on their own, without needing a
# second number, so they're handled separately from OPERATIONS above.
UNARY_OPERATIONS = {
    "sqrt": sqrt,  # square root, applied to the running result
}


def check_quit(value: str) -> None:
    """
    Exit the program gracefully if the user typed 'q'.

    Centralizing this logic here means every prompt in the program
    behaves the same way when the user wants to quit, and any future
    change to the exit behavior only needs to happen in one place.

    Args:
        value: The raw input string to check.
    """
    if value.lower() == "q":
        print("Goodbye!")
        sleep(3)  # Optional: brief pause before exiting
        exit(0)


def get_number(prompt: str) -> float:
    """
    Prompt the user for a number and keep asking until valid input is given.

    Args:
        prompt: The message to display to the user.

    Returns:
        The number entered, as a float.
    """
    while True:
        value = input(prompt).strip()
        check_quit(value)
        try:
            return float(value)
        except ValueError:
            print(f"'{value}' isn't a valid number. Please try again.")


def get_number_or_undo(prompt: str):
    """
    Like get_number(), but also lets the user type 'u' to back out of
    entering this number instead of a value — e.g. if they picked the
    wrong operator and want to change it before finishing this step.

    Args:
        prompt: The message to display to the user.

    Returns:
        The number entered as a float, or None if the user typed 'u'
        to cancel instead.
    """
    while True:
        value = input(prompt).strip()
        check_quit(value)
        if value.lower() == "u":
            return None
        try:
            return float(value)
        except ValueError:
            print(f"'{value}' isn't a valid number. Please try again.")


def clean(n: float) -> str:
    """Format a number without a trailing '.0' when it's a whole number."""
    return str(int(n)) if n == int(n) else str(n)


def describe_step(step: tuple) -> str:
    """Build a short human-readable description of a single step, e.g.
    '+ 5' for a binary step or 'sqrt' for a unary step. Used when telling
    the user what was just undone."""
    op, operand = step
    if operand is None:
        return op
    return f"{op} {clean(operand)}"


def build_expression_string(a: float, steps: list) -> str:
    """
    Build a human-readable string of the whole expression entered so far,
    e.g. '10 + 5 sqrt %of 50' (without the result).

    Args:
        a: The first number.
        steps: The list of (operator, operand_or_None) tuples entered
            after the first number, in order.
    """
    parts = [clean(a)] + [describe_step(step) for step in steps]
    return " ".join(parts)


def evaluate(a: float, steps: list) -> float:
    """
    Apply every step in order to the running result, left to right.
    There's no operator precedence (e.g. '*' before '+') here on purpose:
    steps are applied strictly in the order the user entered them, since
    that's the most predictable behavior for a simple CLI tool.

    Args:
        a: The starting number.
        steps: The list of (operator, operand_or_None) tuples to apply.

    Returns:
        The final result after applying every step.

    Raises:
        ZeroDivisionError: If dividing or taking modulo by zero at any step.
        ValueError: If taking the square root of a negative number at any step.
    """
    result = a
    for op, operand in steps:
        if op in UNARY_OPERATIONS:
            result = UNARY_OPERATIONS[op](result)
        else:
            result = OPERATIONS[op](result, operand)
    return result


def collect_expression() -> tuple:
    """
    Interactively build an expression: a starting number followed by any
    number of operator/operand steps. The user can:
      - type an operator (e.g. '+', 'sqrt') to add the next step
      - type '=' once at least one step has been added, to finish
      - type 'u' to undo the most recently added step (or re-enter the
        first number, if there are no steps left to undo)
      - type 'q' at any point to quit the whole program

    Returns:
        A tuple (a, steps) ready to be passed to evaluate().
    """
    a = get_number("Enter first number (or 'q' to quit): ")
    steps = []  # list of (operator, operand_or_None) tuples, in order

    all_ops = list(OPERATIONS.keys()) + list(UNARY_OPERATIONS.keys())
    valid_ops = ", ".join(all_ops)

    while True:
        print(f"Current expression: {build_expression_string(a, steps)}")
        prompt = (
            f"Enter next operator ({valid_ops}), "
            "'=' to calculate, or 'u' to undo: "
        )
        op = input(prompt).strip()
        check_quit(op)

        if op == "=":
            if not steps:
                print("Add at least one operator before calculating.\n")
                continue
            return a, steps

        elif op.lower() == "u":
            if steps:
                removed = steps.pop()
                print(f"Undid last step: {describe_step(removed)}\n")
            else:
                print("Nothing left to undo, so let's redo the first number.")
                a = get_number("Enter first number: ")

        elif op in UNARY_OPERATIONS:
            ''' Unary operators apply to the running result directly, so no
             extra number is needed.'''
            steps.append((op, None))

        elif op in OPERATIONS:
            operand = get_number_or_undo(
                "Enter next number ('u' to change the operator instead): "
            )
            if operand is None:
                ''' The user backed out of this number; just go back to the
                 operator prompt without adding a step, so they can pick
                 a different operator (or press 'u' again from there to
                 go back even further, to a previous step or the first
                 number).'''
                print("Cancelled that operator. Choose again.\n")
                continue
            steps.append((op, operand))

        else:
            print(f"'{op}' isn't supported. Choose one of: {valid_ops}\n")


def main() -> None:
    """Run the calculator loop until the user chooses to quit."""
    print("=== CLI Calculator ===")
    print("Build an expression with as many numbers and operators as you like.")
    print("Type '=' to calculate, 'u' to undo the last step, or 'q' to quit.\n")

    while True:
        a, steps = collect_expression()

        try:
            result = evaluate(a, steps)
        except ZeroDivisionError:
            print("Error: Cannot divide (or take modulo) by zero. Let's start over.\n")
            continue
        except ValueError:
            print("Error: Cannot take the square root of a negative number. "
                  "Let's start over.\n")
            continue

        print(f"{build_expression_string(a, steps)} = {clean(result)}")
        print()  # blank line for readability between calculations


if __name__ == "__main__":
    main()
