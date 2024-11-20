import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class ATM:
    def __init__(self):
        self.states = ["Idle", "Card_Inserted", "PIN_Verified", "Transaction_Processing", "Completed", "PIN_Incorrect", "Card_Locked"]
        self.transitions = {
            "Idle": {"card_inserted": "Card_Inserted"},
            "Card_Inserted": {"pin_entered": "PIN_Verified", "pin_incorrect": "PIN_Incorrect"},
            "PIN_Incorrect": {"pin_incorrect": "Card_Locked", "pin_entered": "PIN_Verified"},
            "PIN_Verified": {"select_transaction": "Transaction_Processing"},
            "Transaction_Processing": {"transaction_completed": "Completed"},
            "Completed": {"card_ejected": "Idle"},
            "Card_Locked": {"reset_pin_attempts": "Idle"}
        }
        self.current_state = "Idle"
        self.max_pin_attempts = 3  
        self.pin_attempts = 0
        self.correct_pin = "1234"
        self.balance = random.randint(1, 100000)

    def transition(self, input_event):
        if input_event in self.transitions[self.current_state]:
            self.current_state = self.transitions[self.current_state][input_event]
            return True
        return False

    def verify_pin(self, pin):
        return pin == self.correct_pin

    def withdraw(self, amount):
        if amount <= 0:
            return "Error: Amount must be greater than 0."
        if amount > self.balance:
            return "Error: Insufficient balance."
        self.balance -= amount
        return f"Withdrawal successful. Remaining balance: ${self.balance}"

    def deposit(self, amount):
        if amount <= 0:
            return "Error: Deposit amount must be greater than 0."
        self.balance += amount
        return f"Deposit successful. New balance: ${self.balance}"

class ATMApp:
    def __init__(self, root):
        self.atm = ATM()
        self.root = root
        self.root.title("ATM Simulation")
        self.root.geometry("400x400")

        self.state_label = tk.Label(root, text=f"Current State: {self.atm.current_state}", font=("Arial", 14))
        self.state_label.pack(pady=10)

        self.insert_card_button = tk.Button(root, text="Insert Card", command=self.insert_card)
        self.insert_card_button.pack(pady=5)

        self.pin_label = tk.Label(root, text="Enter PIN:", font=("Arial", 12))
        self.pin_label.pack(pady=5)
        self.pin_entry = tk.Entry(root, show="*")
        self.pin_entry.pack(pady=5)

        self.submit_pin_button = tk.Button(root, text="Submit PIN", command=self.submit_pin)
        self.submit_pin_button.pack(pady=5)

        self.transaction_button = tk.Button(root, text="Select Transaction", command=self.select_transaction)
        self.transaction_button.pack(pady=5)

        self.eject_card_button = tk.Button(root, text="Eject Card", command=self.eject_card)
        self.eject_card_button.pack(pady=5)

        self.reset_pin_button = tk.Button(root, text="Reset PIN", command=self.reset_pin)
        self.reset_pin_button.pack(pady=5)

    def update_state_label(self):
        self.state_label.config(text=f"Current State: {self.atm.current_state}")

    def display_locked_message(self):
        self.display_message("Card is locked. Please reset PIN.")

    def insert_card(self):
        if self.atm.current_state == "Card_Locked":
            self.display_locked_message()
            return

        if self.atm.current_state == "Idle":
            if self.atm.transition("card_inserted"):
                self.update_state_label()
                self.display_message("Card inserted. Please enter your PIN.")
        elif self.atm.current_state in ["Card_Inserted", "PIN_Incorrect", "PIN_Verified"]:
            self.display_message("Card is already inserted.")
        else:
            self.display_message("Invalid action.")

    def submit_pin(self):
        if self.atm.current_state == "Card_Locked":
            self.display_locked_message()
            return

        if self.atm.current_state == "Idle":
            self.display_message("Please insert a card first.")
        elif self.atm.current_state == "PIN_Verified":
            self.display_message("You have already entered the correct PIN.")
        elif self.atm.current_state in ["Card_Inserted", "PIN_Incorrect"]:
            pin = self.pin_entry.get()
            if self.atm.verify_pin(pin):
                self.atm.transition("pin_entered")
                self.atm.pin_attempts = 0
                self.update_state_label()
                self.display_message("PIN verified. You can now select a transaction.")
            else:
                self.atm.pin_attempts += 1
                if self.atm.pin_attempts == 1:
                    self.update_state_label()
                    self.display_message(f"Incorrect PIN. {self.atm.max_pin_attempts - self.atm.pin_attempts} attempts left.")
                elif self.atm.pin_attempts == 2:
                    self.atm.transition("pin_incorrect")
                    self.update_state_label()
                    self.display_message(f"Incorrect PIN. {self.atm.max_pin_attempts - self.atm.pin_attempts} attempts left.")
                elif self.atm.pin_attempts >= self.atm.max_pin_attempts:
                    # Lock the card after the third incorrect attempt
                    self.atm.transition("pin_incorrect")
                    self.atm.transition("card_locked")
                    self.update_state_label()
                    self.display_message("Too many incorrect PIN attempts. Your card is locked.")
        else:
            self.display_message("Invalid action.")

    def select_transaction(self):
        if self.atm.current_state == "Card_Locked":
            self.display_locked_message()
            return

        if self.atm.current_state == "Idle":
            self.display_message("Please insert a card first.")
        elif self.atm.current_state == "Card_Inserted":
            self.display_message("Please input PIN first.")
        elif self.atm.current_state == "PIN_Incorrect":
            self.display_message("Enter the correct PIN first.")
        elif self.atm.current_state == "PIN_Verified":
            self.atm.transition("select_transaction")
            self.update_state_label()
            transaction_window = tk.Toplevel(self.root)
            transaction_window.title("Transaction Options")
            transaction_window.geometry("300x200")

            tk.Label(transaction_window, text="Select an option:").pack(pady=10)
            tk.Button(transaction_window, text="Withdraw", command=lambda: self.withdraw(transaction_window)).pack(pady=5)
            tk.Button(transaction_window, text="Balance Inquiry", command=lambda: self.balance_inquiry(transaction_window)).pack(pady=5)
            tk.Button(transaction_window, text="Deposit", command=lambda: self.deposit(transaction_window)).pack(pady=5)
            tk.Button(transaction_window, text="Cancel", command=lambda: self.cancel_transaction(transaction_window)).pack(pady=5)
        else:
            self.display_message("Invalid action.")

    def cancel_transaction(self, window):
        if self.atm.current_state == "Transaction_Processing":
            self.atm.transition("transaction_completed")
            self.update_state_label()
            self.display_message("Transaction cancelled. Returning to main menu.")
            window.destroy()
        else:
            self.display_message("Invalid action.")

    def eject_card(self):
        if self.atm.current_state == "Card_Locked":
            self.display_locked_message()
            return

        if self.atm.current_state == "Idle":
            self.display_message("Please insert a card first.")
        elif self.atm.current_state == "Card_Inserted":
            self.display_message("Invalid action.")
        elif self.atm.current_state == "Completed":
            self.atm.transition("card_ejected")
            self.update_state_label()
            self.display_message("Card ejected. Returning to idle state.")
        elif self.atm.current_state in ["PIN_Incorrect", "PIN_Verified"]:
            self.display_message("Invalid action.")
        else:
            self.display_message("Invalid action.")

    def reset_pin(self):
        if self.atm.current_state == "Card_Locked":
            self.atm.transition("reset_pin_attempts")
            self.atm.pin_attempts = 0
            self.update_state_label()
            self.display_message("PIN attempts reset. You can now use your card.")
        else:
            self.display_message("Invalid action.")

    def withdraw(self, window):
        amount = simpledialog.askinteger("Withdraw", "Enter amount to withdraw:")
        if amount is not None:
            self.process_transaction(lambda: self.atm.withdraw(amount), window)

    def balance_inquiry(self, window):
        self.process_transaction(lambda: f"Your current balance is: ${self.atm.balance}", window)

    def deposit(self, window):
        amount = simpledialog.askinteger("Deposit", "Enter amount to deposit:")
        if amount is not None:
            self.process_transaction(lambda: self.atm.deposit(amount), window)

    def process_transaction(self, transaction_function, window):
        if self.atm.current_state != "Transaction_Processing":
            self.display_message("You must select a transaction first.")
            return

        self.display_message("Transaction is being processed...")
        result = transaction_function()
        self.display_message(result)

        another_transaction = messagebox.askyesno("Another Transaction?", "Would you like to perform another transaction?")
        if not another_transaction:
            self.atm.transition("transaction_completed")
            self.update_state_label()
            self.display_message("Transaction completed. Returning to main menu.")
            window.destroy()

    def display_message(self, message):
        messagebox.showinfo("ATM Status", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()
