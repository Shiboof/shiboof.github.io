import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import (
    add_transaction,
    get_transactions,
    set_budget,
    get_budgets,
    delete_transaction,
    delete_budget
)
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PennyPilot")
        self.root.geometry("720x600")  # Initial window size

        self.canvas = tk.Canvas(self.root)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.create_widgets()
        self.refresh_transactions()

    def create_widgets(self):
        # --- Transaction Entry Frame ---
        entry_frame = tk.LabelFrame(self.scrollable_frame, text="Add Transaction", padx=10, pady=10)
        entry_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(entry_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
        self.date_entry = tk.Entry(entry_frame)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.date_entry.grid(row=0, column=1)

        tk.Label(entry_frame, text="Category:").grid(row=1, column=0)
        self.category_entry = tk.Entry(entry_frame)
        self.category_entry.grid(row=1, column=1)

        tk.Label(entry_frame, text="Amount:").grid(row=2, column=0)
        self.amount_entry = tk.Entry(entry_frame)
        self.amount_entry.grid(row=2, column=1)

        tk.Label(entry_frame, text="Type:").grid(row=3, column=0)
        self.type_var = tk.StringVar()
        self.type_var.set("expense")
        type_menu = ttk.OptionMenu(entry_frame, self.type_var, "expense", "income", "expense")
        type_menu.grid(row=3, column=1)

        add_button = tk.Button(entry_frame, text="Add Transaction", command=self.submit_transaction)
        add_button.grid(row=4, column=0, columnspan=2, pady=5)

        # --- Budget Setting Frame ---
        budget_frame = tk.LabelFrame(self.scrollable_frame, text="Set Budget", padx=10, pady=10)
        budget_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(budget_frame, text="Category:").grid(row=0, column=0)
        self.budget_cat_entry = tk.Entry(budget_frame)
        self.budget_cat_entry.grid(row=0, column=1)

        tk.Label(budget_frame, text="Amount:").grid(row=1, column=0)
        self.budget_amt_entry = tk.Entry(budget_frame)
        self.budget_amt_entry.grid(row=1, column=1)

        budget_button = tk.Button(budget_frame, text="Set Budget", command=self.set_budget)
        budget_button.grid(row=2, column=0, columnspan=2, pady=5)

        self.budget_listbox = tk.Listbox(budget_frame, height=4)
        self.budget_listbox.grid(row=3, column=0, columnspan=2, sticky="we")

        delete_budget_btn = tk.Button(budget_frame, text="Delete Selected Budget", command=self.delete_selected_budget)
        delete_budget_btn.grid(row=4, column=0, columnspan=2, pady=5)

        self.refresh_budget_list()

        # --- Transaction List Frame ---
        self.trans_frame = tk.LabelFrame(self.scrollable_frame, text="Transactions", padx=10, pady=10)
        self.trans_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.trans_listbox = tk.Listbox(self.trans_frame)
        self.trans_listbox.pack(fill="both", expand=True)

        delete_btn = tk.Button(self.trans_frame, text="Delete Selected", command=self.delete_selected_transaction)
        delete_btn.pack(pady=5)

        # --- Chart Frame ---
        chart_frame = tk.LabelFrame(self.scrollable_frame, text="Spending Chart", padx=10, pady=10)
        chart_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.chart_canvas = None
        refresh_chart_btn = tk.Button(chart_frame, text="Refresh Chart", command=self.show_chart)
        refresh_chart_btn.pack()

        self.chart_display = tk.Frame(chart_frame)
        self.chart_display.pack(fill="both", expand=True)

        # --- Budget Summary Frame (with scrollbar) ---
        summary_frame = tk.LabelFrame(self.scrollable_frame, text="Budget vs Actual", padx=10, pady=10)
        summary_frame.pack(fill="both", expand=True, padx=10, pady=5)

        refresh_summary_btn = tk.Button(summary_frame, text="Refresh Summary", command=self.show_budget_summary)
        refresh_summary_btn.pack()

        summary_text_frame = tk.Frame(summary_frame)
        summary_text_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(summary_text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.summary_text = tk.Text(summary_text_frame, height=8, yscrollcommand=scrollbar.set)
        self.summary_text.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.config(command=self.summary_text.yview)

    def submit_transaction(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Amount must be a number.")
            return
        ttype = self.type_var.get()

        if not (date and category and amount):
            messagebox.showerror("Missing Data", "All fields are required.")
            return

        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Date Format Error", "Use YYYY-MM-DD format.")
            return

        add_transaction(date, category, amount, ttype)
        self.refresh_transactions()
        self.show_chart()
        self.show_budget_summary()

    def set_budget(self):
        category = self.budget_cat_entry.get()
        try:
            amount = float(self.budget_amt_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Budget amount must be a number.")
            return

        if not category:
            messagebox.showerror("Missing Data", "Category is required.")
            return

        set_budget(category, amount)
        messagebox.showinfo("Success", f"Budget set for {category}!")
        self.refresh_budget_list()
        self.show_budget_summary()

    def refresh_budget_list(self):
        self.budget_listbox.delete(0, tk.END)
        budgets = get_budgets()
        for category, amount in budgets:
            self.budget_listbox.insert(tk.END, f"{category}: ${amount:.2f}")

    def delete_selected_budget(self):
        selected = self.budget_listbox.get(tk.ACTIVE)
        if not selected:
            messagebox.showwarning("No Selection", "Select a budget to delete.")
            return

        category = selected.split(":")[0].strip()

        confirm = messagebox.askyesno("Confirm Delete", f"Delete budget for '{category}'?")
        if confirm:
            delete_budget(category)
            self.refresh_budget_list()
            self.show_budget_summary()

    def refresh_transactions(self):
        self.trans_listbox.delete(0, tk.END)
        transactions = get_transactions()
        self.transaction_map = {}
        for t in transactions:
            display = f"{t[1]} | {t[4].title()} | {t[2]} | ${t[3]:.2f}"
            self.transaction_map[display] = t[0]
            self.trans_listbox.insert(tk.END, display)

    def delete_selected_transaction(self):
        selected = self.trans_listbox.get(tk.ACTIVE)
        if selected not in self.transaction_map:
            messagebox.showwarning("No Selection", "Please select a transaction to delete.")
            return

        trans_id = self.transaction_map[selected]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this transaction?")
        if confirm:
            delete_transaction(trans_id)
            self.refresh_transactions()
            self.show_chart()
            self.show_budget_summary()

    def show_chart(self):
        conn = sqlite3.connect('budget.db')
        c = conn.cursor()
        c.execute("SELECT category, SUM(amount) FROM transactions WHERE type = 'expense' GROUP BY category")
        data = c.fetchall()
        conn.close()

        if not data:
            messagebox.showinfo("No Data", "No expenses to chart.")
            return

        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
        ax.set_title("Expenses by Category")

        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()

        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_display)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack()

    def show_budget_summary(self):
        self.summary_text.delete(1.0, tk.END)

        budgets = dict(get_budgets())

        if not budgets:
            self.summary_text.insert(tk.END, "No budgets set yet.\n")
            return

        conn = sqlite3.connect('budget.db')
        c = conn.cursor()

        for category, budget_amount in budgets.items():
            c.execute("SELECT SUM(amount) FROM transactions WHERE type = 'expense' AND category = ?", (category,))
            spent = c.fetchone()[0] or 0.0
            remaining = budget_amount - spent

            status = f"${remaining:.2f} left" if remaining >= 0 else f"Over by ${abs(remaining):.2f}"
            line = f"{category}: Budgeted ${budget_amount:.2f}, Spent ${spent:.2f} -> {status}\n"
            self.summary_text.insert(tk.END, line)

        conn.close()
