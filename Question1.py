import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class ATM:
    def __init__(self):
        self.states = {
            'Idle': 'Card_Inserted',
            'Card_Inserted': 'PIN_Verified',
            'PIN_Verified': 'Transaction_Processing',
            'Transaction_Processing': 'Completed',
            'Completed': 'Idle',
            'Card_Locked': 'Idle'
        }
        self.current_state = 'Idle'
        self.max_pin_attempts = 3
        self.pin_attempts = 0
        self.correct_pin = '1234'
        self.pin_entry = ""
        self.balance = random.randint(1, 100000)  # Random initial balance

    def transition(self, input_event):
        if self.current_state == 'Idle':
            if input_event == 'card_inserted':
                self.current_state = 'Card_Inserted'
                return "Card inserted. Please enter your PIN."
            return "Invalid action. Please insert your card."

        elif self.current_state == 'Card_Inserted':
            if input_event == 'pin_entered':
                if self.verify_pin():
                    self.current_state = 'PIN_Verified'
                    return "PIN verified. You can now select a transaction."
                else:
                    self.pin_attempts += 1
                    if self.pin_attempts >= self.max_pin_attempts:
                        self.current_state = 'Card_Locked'
                        return "Too many incorrect PIN attempts. Your card is locked."
                    else:
                        return f"Incorrect PIN. You have {self.max_pin_attempts - self.pin_attempts} attempts left."
            return "Please enter your PIN."

        elif self.current_state == 'PIN_Verified':
            if input_event == 'select_transaction':
                return "Choose a transaction: Withdraw, Balance Inquiry, or Deposit."
            return "Please select a valid transaction."

        elif self.current_state == 'Transaction_Processing':
            return "Transaction is being processed."

        elif self.current_state == 'Completed':
            if input_event == 'card_ejected':
                self.current_state = 'Idle'
                self.pin_attempts = 0  # Reset PIN attempts for a new session
                return "Card ejected. Returning to idle state."
            return "Please eject your card to continue."

        elif self.current_state == 'Card_Locked':
            return "Your card is locked. Please reset PIN attempts at your bank."

        return "Unknown event."

    def verify_pin(self):
        return self.pin_entry == self.correct_pin

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

# GUI Implementation
class ATMApp:
    def __init__(self, root):
        self.atm = ATM()
        self.root = root
        self.root.title("ATM Simulation")
        self.root.geometry("400x400")

        # State label
        self.state_label = tk.Label(root, text=f"Current State: {self.atm.current_state}", font=("Arial", 14))
        self.state_label.pack(pady=10)

        # Card insertion button
        self.insert_card_button = tk.Button(root, text="Insert Card", command=self.insert_card)
        self.insert_card_button.pack(pady=5)

        # PIN entry
        self.pin_label = tk.Label(root, text="Enter PIN:", font=("Arial", 12))
        self.pin_label.pack(pady=5)
        self.pin_entry = tk.Entry(root, show="*")
        self.pin_entry.pack(pady=5)

        # Submit PIN button
        self.submit_pin_button = tk.Button(root, text="Submit PIN", command=self.submit_pin)
        self.submit_pin_button.pack(pady=5)

        # Transaction button
        self.transaction_button = tk.Button(root, text="Select Transaction", command=self.select_transaction)
        self.transaction_button.pack(pady=5)

        # Eject Card button
        self.eject_card_button = tk.Button(root, text="Eject Card", command=self.eject_card)
        self.eject_card_button.pack(pady=5)

    def insert_card(self):
        message = self.atm.transition('card_inserted')
        self.update_state(message)

    def submit_pin(self):
        self.atm.pin_entry = self.pin_entry.get()
        message = self.atm.transition('pin_entered')
        self.update_state(message)

    def select_transaction(self):
        if self.atm.current_state == 'Card_Locked':
            self.update_state("Your card is locked. Please contact your bank.")
            return

        if self.atm.current_state != 'PIN_Verified':
            self.update_state("You must verify your PIN before selecting a transaction.")
            return

        transaction_window = tk.Toplevel(self.root)
        transaction_window.title("Transaction Options")
        transaction_window.geometry("300x200")

        tk.Label(transaction_window, text="Select an option:").pack(pady=10)

        tk.Button(transaction_window, text="Withdraw", command=lambda: self.withdraw(transaction_window)).pack(pady=5)
        tk.Button(transaction_window, text="Balance Inquiry", command=lambda: self.balance_inquiry(transaction_window)).pack(pady=5)
        tk.Button(transaction_window, text="Deposit", command=lambda: self.deposit(transaction_window)).pack(pady=5)

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
        # Display "Transaction is being processed..." message
        self.update_state("Transaction is being processed...")
        # Directly call the transaction completion logic
        self.complete_transaction(transaction_function, window)

    def complete_transaction(self, transaction_function, window):
        result = transaction_function()
        self.update_state(result)

        # Ask user if they want to perform another transaction
        another_transaction = messagebox.askyesno("Another Transaction?", "Would you like to perform another transaction?")
        if not another_transaction:
            self.atm.current_state = 'Completed'
            self.update_state(self.atm.transition('transaction_completed'))
            window.destroy()  # Automatically close the transaction pop-up window

    def eject_card(self):
        message = self.atm.transition('card_ejected')
        self.update_state(message)

    def update_state(self, message):
        self.state_label.config(text=f"Current State: {self.atm.current_state}")
        messagebox.showinfo("ATM Status", message)

# Run the ATM application
if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()
