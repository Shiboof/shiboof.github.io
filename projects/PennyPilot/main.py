# main.py
import tkinter as tk
from db import init_db
from ui import BudgetApp

def main():
    # Initialize the database
    init_db()

    # Launch the Tkinter UI
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
