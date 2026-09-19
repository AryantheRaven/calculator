# CLI Calculator 🧮

A simple, dependency-free command-line calculator written in Python. Chain together as many numbers and operators as you like into a single expression, review and undo any step before calculating, and get the final result printed all at once.

## Features

- **Chained expressions** — combine multiple numbers and operators in one calculation instead of doing one operation at a time (e.g. `10 + 5 * 2 sqrt`).
- **Seven operators** — addition, subtraction, multiplication, division, exponentiation, modulo, and percentage, plus square root.
- **Undo at any point** — press `u` to remove the last step you entered, even while you're in the middle of typing the next number. Keep undoing to go all the way back and change the first number.
- **Live expression preview** — see exactly what you've built so far before you calculate.
- **Friendly error handling** — invalid numbers, division/modulo by zero, and square roots of negative numbers are caught with clear messages instead of crashing.
- **Zero dependencies** — uses only the Python standard library.

## Requirements

- Python 3.6 or higher

## Installation

Clone the repository and you're ready to go — no extra packages required:

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

## Usage

Run the calculator from your terminal:

```bash
python calculator.py
```

You'll be guided through building an expression step by step:

```
=== CLI Calculator ===
Build an expression with as many numbers and operators as you like.
Type '=' to calculate, 'u' to undo the last step, or 'q' to quit.

Enter first number (or 'q' to quit): 10
Current expression: 10
Enter next operator (+, -, *, /, **, %, %of, sqrt), '=' to calculate, or 'u' to undo: +
Enter next number: 5
Current expression: 10 + 5
Enter next operator (+, -, *, /, **, %, %of, sqrt), '=' to calculate, or 'u' to undo: *
Enter next number: 2
Current expression: 10 + 5 * 2
Enter next operator (+, -, *, /, **, %, %of, sqrt), '=' to calculate, or 'u' to undo: =
10 + 5 * 2 = 30
```

### Supported operators

| Operator | Meaning              | Type   | Example              |
|----------|----------------------|--------|-----------------------|
| `+`      | Addition              | Binary | `5 + 3` → `8`         |
| `-`      | Subtraction           | Binary | `5 - 3` → `2`         |
| `*`      | Multiplication        | Binary | `5 * 3` → `15`        |
| `/`      | Division              | Binary | `6 / 3` → `2`         |
| `**`     | Exponentiation        | Binary | `2 ** 3` → `8`        |
| `%`      | Modulo (remainder)    | Binary | `7 % 3` → `1`         |
| `%of`    | Percentage of a number| Binary | `20 %of 200` → `40`   |
| `sqrt`   | Square root           | Unary  | `sqrt(16)` → `4`      |

> **Note:** Binary operators need a second number; `sqrt` applies directly to the running result and doesn't ask for one.

> **Note on order of operations:** Steps are calculated strictly left to right, in the order you enter them — there's no operator precedence (e.g. `*` is not evaluated before `+`). This keeps behavior simple and predictable.

### Correcting a mistake

Type `u` at almost any prompt to undo:

- At the **operator prompt**, `u` removes the last completed step. If there are no steps left, it lets you re-enter the first number.
- At the **"enter next number" prompt**, `u` cancels the operator you just picked and takes you back to choose a different one.

```
Enter next operator (...): +
Enter next number ('u' to change the operator instead): u
Cancelled that operator. Choose again.

Current expression: 10
Enter next operator (...): *
```

### Quitting

Type `q` at any prompt to exit the program immediately.

## Error handling

| Situation                          | What happens                                              |
|-------------------------------------|-------------------------------------------------------------|
| Non-numeric input                   | You're asked to re-enter the number.                        |
| Division or modulo by zero          | An error is shown and the current expression is discarded.  |
| Square root of a negative number    | An error is shown and the current expression is discarded.  |

## Project structure

```
.
├── calculator.py   # The calculator's source code
└── README.md       # This file
```

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
