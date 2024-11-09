import tkinter as tk
from tkinter import messagebox

class ATM:
    def __init__(self):
        self.states = ['Idle', 'Card_Inserted', 'PIN_Verified', 'Transaction_Processing', 'Completed', 'PIN_Incorrect', 'Card_Locked']
        self.current_state = 'Idle'
        self.max_pin_attempts = 3
        self.pin_attempts = 0
        self.correct_pin = '1234'
        self.pin_entry = ""

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
                self.current_state = 'Transaction_Processing'
                return "Transaction is being processed."
            return "Please select a valid transaction."

        elif self.current_state == 'Transaction_Processing':
            if input_event == 'transaction_completed':
                self.current_state = 'Completed'
                return "Transaction completed. Please eject your card."
            return "Transaction is still in progress."

        elif self.current_state == 'Completed':
            if input_event == 'card_ejected':
                self.current_state = 'Idle'
                self.pin_attempts = 0  # Reset PIN attempts for a new session
                return "Card ejected. Returning to idle state."
            return "Please eject your card to continue."

        elif self.current_state == 'Card_Locked':
            if input_event == 'reset_pin_attempts':
                self.current_state = 'Idle'
                self.pin_attempts = 0
                return "PIN attempts reset. Card is unlocked."
            return "Card is locked. Please reset PIN attempts."

        return "Unknown event."

    def verify_pin(self):
        # Simulate PIN verification
        return self.pin_entry == self.correct_pin

# GUI Implementation
class ATMApp:
    def __init__(self, root):
        self.atm = ATM()
        self.root = root
        self.root.title("ATM Simulation")
        self.root.geometry("400x300")
        
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
        
        # Complete Transaction button
        self.complete_transaction_button = tk.Button(root, text="Complete Transaction", command=self.complete_transaction)
        self.complete_transaction_button.pack(pady=5)
        
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
        message = self.atm.transition('select_transaction')
        self.update_state(message)
    
    def complete_transaction(self):
        message = self.atm.transition('transaction_completed')
        self.update_state(message)
    
    def eject_card(self):
        message = self.atm.transition('card_ejected')
        self.update_state(message)

    def update_state(self, message):
        # Update the state label and show any message as a popup
        self.state_label.config(text=f"Current State: {self.atm.current_state}")
        messagebox.showinfo("ATM Status", message)

# Run the ATM application
if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()
