#!/usr/bin/env python3
"""
Simple CLI Calculator
----------------------
A command-line calculator that supports basic arithmetic operations:
addition, subtraction, multiplication, division, exponentiation, and modulo.

Run it with:
    python calculator.py
"""

import sys
from time import sleep

# Map of supported operators to functions.
# Using a dictionary like this makes it easy to add new operators later
# without needing a long chain of if/elif statements.
OPERATIONS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,       # will raise ZeroDivisionError if b == 0
    "**": lambda a, b: a ** b,     # exponentiation
    "%": lambda a, b: a % b,       # modulo
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
        sys.exit(0)


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


def get_operator() -> str:
    """
    Prompt the user for an operator and keep asking until a supported one
    is given.

    Returns:
        A valid operator symbol as a string (e.g. '+', '-', '*', '/').
    """
    valid_ops = ", ".join(OPERATIONS.keys())
    while True:
        op = input(f"Enter an operator ({valid_ops}): ").strip()
        check_quit(op)
        if op in OPERATIONS:
            return op
        print(f"'{op}' isn't supported. Choose one of: {valid_ops}")


def calculate(a: float, op: str, b: float) -> float:
    """
    Perform the calculation for the given operator and operands.

    Args:
        a: The first number.
        op: The operator symbol.
        b: The second number.

    Returns:
        The result of the calculation.

    Raises:
        ZeroDivisionError: If dividing or taking modulo by zero.
    """
    return OPERATIONS[op](a, b)


def format_result(a: float, op: str, b: float, result: float) -> str:
    """
    Build a nicely formatted string showing the calculation and its result.
    Whole numbers are displayed without a trailing '.0' for readability.
    """
    def clean(n: float) -> str:
        return str(int(n)) if n == int(n) else str(n)

    return f"{clean(a)} {op} {clean(b)} = {clean(result)}"


def main() -> None:
    """Run the calculator loop until the user chooses to quit."""
    print("=== CLI Calculator ===")
    print("Type 'q' at any prompt to quit.\n")

    while True:
        first_input = input("Enter first number (or 'q' to quit): ").strip()
        check_quit(first_input)

        # Re-validate the first number since check_quit only handles 'q'.
        try:
            a = float(first_input)
        except ValueError:
            print(f"'{first_input}' isn't a valid number. Please try again.\n")
            continue

        op = get_operator()
        b = get_number("Enter second number: ")

        try:
            result = calculate(a, op, b)
        except ZeroDivisionError:
            print("Error: Cannot divide (or take modulo) by zero.\n")
            continue

        print(format_result(a, op, b, result))
        print()  # blank line for readability between calculations


if __name__ == "__main__":
    main()
