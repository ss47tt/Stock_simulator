import tkinter as tk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class StockTradingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Trading Simulator")

        # Initial user data
        self.balance = 10000  # Starting balance
        self.portfolio = {"MEOW": 0}  # Initial portfolio with zero shares of MEOW
        self.stock_prices = {"MEOW": 150}  # Single stock MEOW
        self.price_history = [self.stock_prices["MEOW"]]  # Track stock price history

        # Initialize figure and axes for the plot (Increase graph size)
        self.fig, self.ax = plt.subplots(figsize=(10, 6))  # Increased figure size

        # GUI Layout
        self.create_widgets()
        self.update_prices_periodically()

    def create_widgets(self):
        # Balance display (Increase font size)
        self.balance_label = tk.Label(self.root, text=f"Balance: ${self.balance}", font=("Arial", 18))
        self.balance_label.pack(pady=20)

        # Stock prices display
        self.stock_frame = tk.Frame(self.root)
        self.stock_frame.pack()

        tk.Label(self.stock_frame, text="Stock", font=("Arial", 14)).grid(row=0, column=0, padx=20)
        tk.Label(self.stock_frame, text="Price", font=("Arial", 14)).grid(row=0, column=1, padx=20)

        # Display stock MEOW
        tk.Label(self.stock_frame, text="MEOW", font=("Arial", 14)).grid(row=1, column=0, padx=20)
        self.stock_price_label = tk.Label(self.stock_frame, text=f"${self.stock_prices['MEOW']}", font=("Arial", 14))
        self.stock_price_label.grid(row=1, column=1, padx=20)

        # Buy/Sell inputs
        self.action_frame = tk.Frame(self.root)
        self.action_frame.pack(pady=30)

        tk.Label(self.action_frame, text="Quantity:", font=("Arial", 14)).grid(row=0, column=0, padx=10)
        self.quantity_entry = tk.Entry(self.action_frame, font=("Arial", 14))
        self.quantity_entry.grid(row=0, column=1, padx=10)

        self.buy_button = tk.Button(self.action_frame, text="Buy", font=("Arial", 14), command=self.buy_stock)
        self.buy_button.grid(row=0, column=2, padx=20)

        self.sell_button = tk.Button(self.action_frame, text="Sell", font=("Arial", 14), command=self.sell_stock)
        self.sell_button.grid(row=0, column=3, padx=20)

        # Portfolio display (show number of shares directly)
        self.shares_label = tk.Label(self.root, text=f"MEOW Shares: {self.portfolio['MEOW']}", font=("Arial", 14))
        self.shares_label.pack(pady=20)

        # Plot the graph
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(pady=30)

        # Initialize canvas variable
        self.canvas = None

    def buy_stock(self):
        quantity = self.quantity_entry.get()

        if not quantity.isdigit() or int(quantity) <= 0:
            messagebox.showerror("Error", "Quantity must be a positive integer.")
            return

        quantity = int(quantity)
        total_cost = self.stock_prices["MEOW"] * quantity

        if total_cost > self.balance:
            messagebox.showerror("Error", "Insufficient balance.")
            return

        self.balance -= total_cost
        self.portfolio["MEOW"] += quantity
        self.update_balance()  # Update the balance on the GUI
        self.update_shares()  # Update the shares on the GUI
        messagebox.showinfo("Success", f"Bought {quantity} shares of MEOW for ${total_cost}.")

    def sell_stock(self):
        quantity = self.quantity_entry.get()

        if not quantity.isdigit() or int(quantity) <= 0:
            messagebox.showerror("Error", "Quantity must be a positive integer.")
            return

        quantity = int(quantity)

        if quantity > self.portfolio["MEOW"]:
            messagebox.showerror("Error", "You do not own enough shares.")
            return

        total_revenue = self.stock_prices["MEOW"] * quantity
        self.balance += total_revenue
        self.portfolio["MEOW"] -= quantity

        self.update_balance()  # Update the balance on the GUI
        self.update_shares()  # Update the shares on the GUI
        messagebox.showinfo("Success", f"Sold {quantity} shares of MEOW for ${total_revenue}.")

    def update_shares(self):
        self.shares_label.config(text=f"MEOW Shares: {self.portfolio['MEOW']}")

    def update_prices(self):
        # Introduce a 5% chance for larger fluctuations (70% to 130%)
        if random.random() < 0.05:  # 5% chance
            multiplier = random.uniform(0.7, 1.3)
        else:  # 95% chance for normal fluctuation
            multiplier = random.uniform(0.95, 1.05)

        # Update the stock price
        self.stock_prices["MEOW"] = round(self.stock_prices["MEOW"] * multiplier, 2)
        self.price_history.append(self.stock_prices["MEOW"])  # Append the new price to history
        self.stock_price_label.config(text=f"${self.stock_prices['MEOW']}")

    def update_prices_periodically(self):
        self.update_prices()
        self.plot_graph()  # Update the graph live
        self.root.after(2000, self.update_prices_periodically)  # Update every 2 seconds

    def plot_graph(self):
        # Clear the previous plot data and replot the updated prices
        self.ax.clear()
        self.ax.plot(self.price_history, label='MEOW Stock Price', color='blue')
        self.ax.set_title("Stock Price History", fontsize=18)
        self.ax.set_xlabel("Time (in 2-second intervals)", fontsize=14)
        self.ax.set_ylabel("Price ($)", fontsize=14)
        self.ax.legend(fontsize=12)

        # Redraw the canvas (ensure to re-embed in tkinter window)
        if self.canvas is None:
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
            self.canvas.get_tk_widget().pack()
        else:
            self.canvas.draw()

    def update_balance(self):
        self.balance_label.config(text=f"Balance: ${self.balance}")


if __name__ == "__main__":
    root = tk.Tk()
    app = StockTradingApp(root)
    root.mainloop()