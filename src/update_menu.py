import tkinter as tk

def create_side_menu(master, options):
    """Δημιουργεί ένα πλευρικό κάθετο μενού."""
    side_menu = tk.Frame(master, bg="lightgray", width=200)
    side_menu.pack(side="left", fill="y")

    for option in options:
        button = tk.Button(side_menu, text=option, bg="white", relief="flat")
        button.pack(fill="x", padx=5, pady=5)

    return side_menu