import re

class PythonArraySyntaxChecker:
    def __init__(self, program):
        self.program = program.strip().split("\n")  # Split input into lines

    def tokenize(self, line):
        """
        Tokenize a single line of code using regex.
        """
        token_patterns = {
            "VAR": r"[a-zA-Z_][a-zA-Z0-9_]*",  # Variable name
            "ASSIGN": r"=",                   # Assignment operator
            "LBRACKET": r"\[",                # Left square bracket
            "RBRACKET": r"\]",                # Right square bracket
            "NUM": r"\d+",                    # Numbers
            "MULT": r"\*",                    # Multiplication operator
            "COMMA": r",",                    # Commas for list separation
        }

        token_regex = "|".join(f"(?P<{key}>{value})" for key, value in token_patterns.items())
        tokens = [(match.lastgroup, match.group()) for match in re.finditer(token_regex, line)]
        return tokens

    def parse_line(self, tokens):
        """
        Parse a single line of tokens based on Python array syntax.
        """
        if len(tokens) == 0:
            return False

        # Handle array declaration: arr = [0] * NUM
        if len(tokens) >= 6 and tokens[1][0] == "ASSIGN" and tokens[2][1] == "[" and tokens[3][1] == "0" and tokens[4][1] == "]" and tokens[5][0] == "MULT":
            if tokens[6][0] == "NUM":
                return True

        # Handle array initialization: arr = [NUM, NUM, ...]
        if len(tokens) >= 4 and tokens[1][0] == "ASSIGN" and tokens[2][1] == "[" and tokens[-1][1] == "]":
            for i in range(3, len(tokens) - 1, 2):  # Check NUM, COMMA pairs
                if tokens[i][0] != "NUM":
                    return False
                if i + 1 < len(tokens) - 1 and tokens[i + 1][0] != "COMMA":
                    return False
            return True

        # Handle array access: arr[NUM] = NUM
        if len(tokens) >= 6 and tokens[1][1] == "[" and tokens[3][1] == "]" and tokens[4][0] == "ASSIGN" and tokens[5][0] == "NUM":
            return True

        return False

    def check_syntax(self):
        """
        Check the syntax of the entire program and report invalid lines.
        """
        invalid_lines = []
        for i, line in enumerate(self.program):
            tokens = self.tokenize(line.strip())  # Tokenize each line
            if not self.parse_line(tokens):      # Parse the tokens
                invalid_lines.append((i + 1, line.strip()))  # Store line number and content

        if invalid_lines:
            for line_num, code in invalid_lines:
                print(f"Syntax error in line {line_num}: {code}")
            return False

        print("Syntax is correct!")
        return True


# Main program
if __name__ == "__main__":
    while True:
        print("\nEnter your Python program (finish with an empty line):")
        user_input = []
        while True:
            try:
                line = input()
                if not line.strip():  # Stop on empty input
                    break
                user_input.append(line)
            except KeyboardInterrupt:
                print("\nExiting the program. Goodbye!")
                exit()

        if not user_input:  # Handle completely empty input
            print("No input provided. Exiting...")
            break

        program = "\n".join(user_input)  # Combine user input into a single string
        checker = PythonArraySyntaxChecker(program)

        # If no errors, print correct syntax
        checker.check_syntax()

        # Ask if the user wants to check another program
        repeat = input("\nDo you want to check another program? (yes/no): ").strip().lower()
        if repeat != "yes":
            print("Goodbye!")
            break
