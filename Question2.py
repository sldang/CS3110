import tkinter as tk
from tkinter import Toplevel, Text, Button, Label

class PythonArraySyntaxChecker:
    def __init__(self, program):
        self.program = program.strip().split("\n")  # Split input into lines

    def tokenize(self, line):
        import re
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
        invalid_lines = []
        for i, line in enumerate(self.program):
            tokens = self.tokenize(line.strip())  # Tokenize each line
            if not self.parse_line(tokens):      # Parse the tokens
                invalid_lines.append((i + 1, line.strip()))  # Store line number and content

        if invalid_lines:
            errors = [f"Syntax error in line {line_num}: {code}" for line_num, code in invalid_lines]
            return False, errors

        return True, ["Syntax is correct!"]


def show_results_popup(input_code, results):
    # Create a new window for the popup
    popup = Toplevel(root)
    popup.title("Results")

    # Input code display
    Label(popup, text="Input Code:").pack(anchor="w", padx=10, pady=5)
    input_display = Text(popup, height=8, width=50, state="normal")
    input_display.pack(padx=10, pady=5)
    input_display.insert("1.0", input_code)
    input_display.configure(state="disabled")  # Make the text read-only

    # Results display
    Label(popup, text="Results:").pack(anchor="w", padx=10, pady=5)
    results_display = Text(popup, height=8, width=50, state="normal")
    results_display.pack(padx=10, pady=5)
    results_display.insert("1.0", "\n".join(results))
    results_display.configure(state="disabled")  # Make the text read-only

    # Back button to close the popup
    Button(popup, text="Back", command=popup.destroy).pack(pady=10)


def check_syntax():
    # Get the user input from the text box
    user_input = text_input.get("1.0", tk.END).strip()
    if not user_input:
        # Show a warning directly in the results area if the input is empty
        results_output.delete("1.0", tk.END)
        results_output.insert(tk.END, "No input provided. Please enter some code to check.")
        return

    # Use the syntax checker class to check the code
    checker = PythonArraySyntaxChecker(user_input)
    is_correct, results = checker.check_syntax()

    # Clear input after checking
    text_input.delete("1.0", tk.END)

    # Show the results in a popup
    show_results_popup(user_input, results)


# Create the main application window
root = tk.Tk()
root.title("Python Array Syntax Checker")

# Label for input area
input_label = tk.Label(root, text="Enter Python Code:")
input_label.pack(anchor="w", padx=5, pady=5)

# Text input for Python code
text_input = tk.Text(root, height=15, width=70)
text_input.pack(padx=5, pady=5)

# Check Syntax Button
check_button = tk.Button(root, text="Check Syntax", command=check_syntax)
check_button.pack(pady=10)

# Results output area (Optional, to track activity in the main window)
results_output = tk.Text(root, height=10, width=70)
results_output.pack(padx=5, pady=5)

# Start the application
root.mainloop()
