import tkinter as tk
from gui import App
from db_manager import init_db

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    root.title("Διαχείριση Προσωπικών Οικονομικών")
    root.geometry("800x600")
    app = App(master=root)
    app.mainloop()
