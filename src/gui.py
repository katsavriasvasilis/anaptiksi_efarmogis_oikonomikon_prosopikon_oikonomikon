
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from db_manager import (
    get_categories, add_category, delete_category,
    add_transaction, get_transactions_by_month, delete_transaction
)
from charts import plot_expenses_by_category
from excel_export import export_month_to_excel
import tkinter.filedialog as filedialog

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.sidebar = tk.Frame(self, bg="#2C3E50", width=200)
        self.sidebar.pack(side="left", fill="y")
        self.content = tk.Frame(self, bg="#F3F4F6")
        self.content.pack(side="right", fill="both", expand=True)
        self.create_sidebar_button("📂 Κατηγορίες", self.show_categories)
        self.create_sidebar_button("💰 Έσοδα/Έξοδα", self.show_transactions)
        self.create_sidebar_button("📊 Γραφήματα", self.show_charts)
        self.create_sidebar_button("📤 Εξαγωγή", self.show_export)
        self.frames = {}
        self.init_categories_tab()
        self.init_transactions_tab()
        self.init_charts_tab()
        self.init_export_tab()
        self.show_categories()

    def create_sidebar_button(self, text, command):
        button = tk.Button(self.sidebar, text=text, command=command, bg="#34495E", fg="white",
                           relief="flat", anchor="w", padx=15, font=("Arial", 12))
        button.pack(fill="x", pady=5)

    def clear_content(self):
        for frame in self.frames.values():
            frame.pack_forget()

    def show_categories(self):
        self.clear_content()
        self.frames["categories"].pack(fill="both", expand=True)
        self.refresh_categories()

    def show_transactions(self):
        self.clear_content()
        self.frames["transactions"].pack(fill="both", expand=True)
        self.refresh_categories_dropdown()
        self.refresh_transactions()

    def show_charts(self):
        self.clear_content()
        self.frames["charts"].pack(fill="both", expand=True)

    def show_export(self):
        self.clear_content()
        self.frames["export"].pack(fill="both", expand=True)

    def init_categories_tab(self):
        frame = tk.Frame(self.content, bg="#F3F4F6")
        self.frames["categories"] = frame
        inner_frame = tk.Frame(frame, bg="#F3F4F6")
        inner_frame.place(relx=0.5, rely=0.3, anchor="center")
        tk.Label(inner_frame, text="Όνομα Κατηγορίας:", bg="#F3F4F6").pack(pady=(0, 5))
        self.entry_cat_name = tk.Entry(inner_frame, justify="center")
        self.entry_cat_name.pack(pady=(0, 10))
        tk.Label(inner_frame, text="Τύπος:", bg="#F3F4F6").pack(pady=(0, 5))
        self.combo_type = ttk.Combobox(inner_frame, values=["income", "expense"], justify="center")
        self.combo_type.pack(pady=(0, 10))
        tk.Button(inner_frame, text="Προσθήκη", command=self.add_category, bg="#34495E", fg="white").pack(pady=(0, 10))
        self.categories_listbox = tk.Listbox(inner_frame, width=50)
        self.categories_listbox.pack(pady=(10, 10))
        tk.Button(inner_frame, text="Διαγραφή Επιλεγμένης", command=self.delete_selected_category,
                  bg="#34495E", fg="white").pack(pady=(10, 0))

    def init_transactions_tab(self):
        frame = tk.Frame(self.content, bg="#F3F4F6")
        self.frames["transactions"] = frame
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        tk.Label(frame, text="Ποσό:", bg="#F3F4F6").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_amount = tk.Entry(frame)
        self.entry_amount.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(frame, text="Ημερομηνία:", bg="#F3F4F6").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_date = tk.Entry(frame)
        self.entry_date.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(frame, text="Κατηγορία:", bg="#F3F4F6").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.combo_category = ttk.Combobox(frame, values=[])
        self.combo_category.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        tk.Label(frame, text="Περιγραφή:", bg="#F3F4F6").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entry_description = tk.Entry(frame)
        self.entry_description.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.is_recurring = tk.IntVar()
        self.check_rec = tk.Checkbutton(frame, text="Επαναλαμβανόμενο", variable=self.is_recurring, bg="#F3F4F6")
        self.check_rec.grid(row=4, column=0, columnspan=2, pady=(5, 10))

        tk.Button(frame, text="Προσθήκη", command=self.add_transaction, bg="#34495E", fg="white").grid(row=5, column=0, columnspan=2, pady=10)
        self.transactions_listbox = tk.Listbox(frame, width=80, height=10)
        self.transactions_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        tk.Button(frame, text="Διαγραφή Επιλεγμένης", command=self.delete_selected_transaction,
                  bg="#34495E", fg="white").grid(row=7, column=0, columnspan=2, pady=10)

    def init_charts_tab(self):
        frame = tk.Frame(self.content, bg="#F3F4F6")
        self.frames["charts"] = frame
        inner_frame = tk.Frame(frame, bg="#F3F4F6")
        inner_frame.place(relx=0.5, rely=0.15, anchor="center")
        tk.Label(inner_frame, text="Έτος:", bg="#F3F4F6").pack(pady=(0, 5))
        self.entry_chart_year = tk.Entry(inner_frame, justify="center")
        self.entry_chart_year.insert(0, "2025")
        self.entry_chart_year.pack(pady=(0, 10))
        tk.Label(inner_frame, text="Μήνας:", bg="#F3F4F6").pack(pady=(0, 5))
        self.entry_chart_month = tk.Entry(inner_frame, justify="center")
        self.entry_chart_month.insert(0, "05")
        self.entry_chart_month.pack(pady=(0, 10))
        tk.Button(inner_frame, text="Προβολή Γραφήματος", command=self.show_expense_chart,
                  bg="#34495E", fg="white").pack(pady=(10, 0))

    def init_export_tab(self):
        frame = tk.Frame(self.content, bg="#F3F4F6")
        self.frames["export"] = frame
        inner_frame = tk.Frame(frame, bg="#F3F4F6")
        inner_frame.place(relx=0.5, rely=0.15, anchor="center")
        tk.Label(inner_frame, text="Έτος:", bg="#F3F4F6").pack(pady=(0, 5))
        self.entry_export_year = tk.Entry(inner_frame, justify="center")
        self.entry_export_year.insert(0, "2025")
        self.entry_export_year.pack(pady=(0, 10))
        tk.Label(inner_frame, text="Μήνας:", bg="#F3F4F6").pack(pady=(0, 5))
        self.entry_export_month = tk.Entry(inner_frame, justify="center")
        self.entry_export_month.insert(0, "05")
        self.entry_export_month.pack(pady=(0, 10))
        tk.Button(inner_frame, text="Εξαγωγή", command=self.export_to_excel,
                  bg="#34495E", fg="white").pack(pady=(10, 0))

    def refresh_categories(self):
        self.categories_listbox.delete(0, tk.END)
        for cat in get_categories():
            display_text = f"{cat[0]} - {cat[1]} ({cat[2]})"
            self.categories_listbox.insert(tk.END, display_text)

    def add_category(self):
        name = self.entry_cat_name.get()
        category_type = self.combo_type.get()
        if name and category_type:
            add_category(name, category_type)
            self.entry_cat_name.delete(0, tk.END)
            self.combo_type.set("")
            self.refresh_categories()
            self.refresh_categories_dropdown()

    def delete_selected_category(self):
        selection = self.categories_listbox.curselection()
        if selection:
            selected_text = self.categories_listbox.get(selection[0])
            category_id = int(selected_text.split(" - ")[0])
            delete_category(category_id)
            self.refresh_categories()
            self.refresh_categories_dropdown()

    def refresh_categories_dropdown(self):
        categories = get_categories()
        display = [f"{cat[0]} - {cat[1]} ({cat[2]})" for cat in categories]
        self.combo_category["values"] = display

    def add_transaction(self):
        try:
            amount = float(self.entry_amount.get())
            date = self.entry_date.get()
            category_text = self.combo_category.get()
            category_id = int(category_text.split(" - ")[0])
            description = self.entry_description.get()
            is_rec = self.is_recurring.get()
            add_transaction(amount, date, category_id, description, is_rec)
            self.entry_amount.delete(0, tk.END)
            self.entry_date.delete(0, tk.END)
            self.entry_description.delete(0, tk.END)
            self.combo_category.set("")
            self.is_recurring.set(0)
            self.refresh_transactions()
        except Exception as e:
            print("Σφάλμα προσθήκης:", e)

    def refresh_transactions(self):
        self.transactions_listbox.delete(0, tk.END)
        now = datetime.now()
        for t in get_transactions_by_month(now.year, now.month):
            txt = f"{t[0]} | {t[1]:.2f}€ | {t[2]} | {t[3]} ({t[4]}) | {t[5]}"
            self.transactions_listbox.insert(tk.END, txt)

    def delete_selected_transaction(self):
        selection = self.transactions_listbox.curselection()
        if selection:
            selected_text = self.transactions_listbox.get(selection[0])
            transaction_id = int(selected_text.split(" | ")[0])
            delete_transaction(transaction_id)
            self.refresh_transactions()

    def show_expense_chart(self):
        try:
            year = int(self.entry_chart_year.get())
            month = int(self.entry_chart_month.get())
            plot_expenses_by_category(year, month)
        except Exception as e:
            print("Σφάλμα στο γράφημα:", e)

    def export_to_excel(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                     filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
                                                     title="Αποθήκευση Ως")
            if file_path:
                export_month_to_excel(int(self.entry_export_year.get()), int(self.entry_export_month.get()), file_path)
        except Exception as e:
            tk.messagebox.showerror("Σφάλμα", f"Η εξαγωγή απέτυχε: {str(e)}")
