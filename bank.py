import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import csv
from os.path import isfile

CSV_FILE = "customer_data.csv"
CSV_HEADERS = ["account_number", "customer_name", "balance"]

users = {"admin": "1234", "user": "pass"}

class BankManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management System")
        self.root.resizable(False, False)
        self.customer_data = []
        self._ensure_csv_exists()
        self.load_data()
        self.create_login_screen()

    def create_login_screen(self):
        self.login_frame = tk.Frame(self.root)
        tk.Label(self.login_frame, text="Login", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.login_frame, text="Username").pack()
        self.entry_username = tk.Entry(self.login_frame)
        self.entry_username.pack()
        tk.Label(self.login_frame, text="Password").pack()
        self.entry_password = tk.Entry(self.login_frame, show="*")
        self.entry_password.pack()
        tk.Button(self.login_frame, text="Login", command=self.login).pack(pady=10)
        self.login_frame.pack(fill="both", expand=True)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username in users and users[username] == password:
            self.login_frame.pack_forget()
            self.create_menu()
            self.create_widgets()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")

    def logout(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_login_screen()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        customer_menu = tk.Menu(menubar, tearoff=0)
        customer_menu.add_command(label="Add Customer", command=self.add_customer)
        customer_menu.add_command(label="Show Customers", command=self.show_customers)
        customer_menu.add_command(label="Search Customer", command=self.search_customer)
        customer_menu.add_command(label="Update Customer", command=self.update_customer)
        customer_menu.add_command(label="Delete Customer", command=self.delete_customer)
        menubar.add_cascade(label="Customers", menu=customer_menu)
        transaction_menu = tk.Menu(menubar, tearoff=0)
        transaction_menu.add_command(label="Make Transaction", command=self.make_transaction_dialog)
        menubar.add_cascade(label="Transactions", menu=transaction_menu)
        account_menu = tk.Menu(menubar, tearoff=0)
        account_menu.add_command(label="Logout", command=self.logout)
        account_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="Account", menu=account_menu)
        self.root.config(menu=menubar)

    def create_widgets(self):
        pad = {"padx": 10, "pady": 6}
        tk.Label(self.root, text="Account Number:").grid(row=0, column=0, sticky="e", **pad)
        tk.Label(self.root, text="Customer Name:").grid(row=1, column=0, sticky="e", **pad)
        tk.Label(self.root, text="Balance:").grid(row=2, column=0, sticky="e", **pad)
        self.acc_number_entry = tk.Entry(self.root, width=30)
        self.acc_number_entry.grid(row=0, column=1, **pad)
        self.customer_name_entry = tk.Entry(self.root, width=30)
        self.customer_name_entry.grid(row=1, column=1, **pad)
        self.balance_entry = tk.Entry(self.root, width=30)
        self.balance_entry.grid(row=2, column=1, **pad)
        tk.Button(self.root, text="Add Customer", width=20, command=self.add_customer).grid(row=3, column=0, columnspan=2, **pad)
        tk.Button(self.root, text="Show Customers", width=20, command=self.show_customers).grid(row=4, column=0, columnspan=2, **pad)
        tk.Button(self.root, text="Search", width=20, command=self.search_customer).grid(row=5, column=0, columnspan=2, **pad)
        tk.Button(self.root, text="Update Customer", width=20, command=self.update_customer).grid(row=6, column=0, columnspan=2, **pad)
        tk.Button(self.root, text="Delete Customer", width=20, command=self.delete_customer).grid(row=7, column=0, columnspan=2, **pad)
        tk.Button(self.root, text="Make Transaction", width=20, command=self.make_transaction_dialog).grid(row=8, column=0, columnspan=2, **pad)

    def _ensure_csv_exists(self):
        if not isfile(CSV_FILE):
            with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
                writer.writeheader()

    def _find_index_by_acc(self, acc_number):
        for i, row in enumerate(self.customer_data):
            if row["account_number"] == acc_number:
                return i
        return -1

    def _parse_balance(self, value, field_name="Balance"):
        try:
            return float(value)
        except ValueError:
            messagebox.showerror("Error", f"Invalid {field_name}. Please enter a valid number.")
            return None

    def _clear_entries(self):
        self.acc_number_entry.delete(0, tk.END)
        self.customer_name_entry.delete(0, tk.END)
        self.balance_entry.delete(0, tk.END)

    def add_customer(self):
        acc_number = self.acc_number_entry.get().strip()
        customer_name = self.customer_name_entry.get().strip()
        balance_str = self.balance_entry.get().strip() or "0"
        if not acc_number or not customer_name:
            messagebox.showerror("Error", "Please enter Account Number and Customer Name.")
            return
        if self._find_index_by_acc(acc_number) != -1:
            messagebox.showerror("Error", "Account number already exists.")
            return
        balance = self._parse_balance(balance_str)
        if balance is None:
            return
        self.customer_data.append({
            "account_number": acc_number,
            "customer_name": customer_name,
            "balance": balance
        })
        self.save_data()
        messagebox.showinfo("Success", "Customer added successfully.")
        self._clear_entries()

    def show_customers(self):
        window = tk.Toplevel(self.root)
        window.title("Customer List")
        window.geometry("520x320")
        cols = ("Account Number", "Customer Name", "Balance")
        tree = ttk.Treeview(window, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=160 if c != "Balance" else 120, anchor="center")
        tree.pack(fill=tk.BOTH, expand=True)
        for row in self.customer_data:
            tree.insert("", tk.END, values=(row["account_number"], row["customer_name"], f"{row['balance']:.2f}"))

    def search_customer(self):
        query = simpledialog.askstring("Search", "Enter Account Number or Customer Name:")
        if not query:
            return
        query = query.strip().lower()
        results = [r for r in self.customer_data
                   if r["account_number"].lower() == query or query in r["customer_name"].lower()]
        if not results:
            messagebox.showinfo("Search", "No matching customer found.")
            return
        window = tk.Toplevel(self.root)
        window.title("Search Results")
        cols = ("Account Number", "Customer Name", "Balance")
        tree = ttk.Treeview(window, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=160 if c != "Balance" else 120, anchor="center")
        tree.pack(fill=tk.BOTH, expand=True)
        for row in results:
            tree.insert("", tk.END, values=(row["account_number"], row["customer_name"], f"{row['balance']:.2f}"))

    def update_customer(self):
        acc_number = self.acc_number_entry.get().strip()
        customer_name = self.customer_name_entry.get().strip()
        balance_str = self.balance_entry.get().strip()
        if not acc_number:
            messagebox.showerror("Error", "Please enter Account Number to update.")
            return
        idx = self._find_index_by_acc(acc_number)
        if idx == -1:
            messagebox.showerror("Error", "Account number does not exist.")
            return
        if customer_name:
            self.customer_data[idx]["customer_name"] = customer_name
        if balance_str:
            balance = self._parse_balance(balance_str)
            if balance is None:
                return
            self.customer_data[idx]["balance"] = balance
        self.save_data()
        messagebox.showinfo("Success", "Customer updated successfully.")
        self._clear_entries()

    def delete_customer(self):
        acc_number = self.acc_number_entry.get().strip()
        if not acc_number:
            messagebox.showerror("Error", "Please enter an Account Number.")
            return
        idx = self._find_index_by_acc(acc_number)
        if idx == -1:
            messagebox.showerror("Error", "Account number does not exist.")
            return
        if messagebox.askyesno("Confirm Delete", f"Delete account {acc_number}?"):
            del self.customer_data[idx]
            self.save_data()
            messagebox.showinfo("Success", "Customer deleted successfully.")
            self._clear_entries()

    def make_transaction_dialog(self):
        acc_number = self.acc_number_entry.get().strip()
        if not acc_number:
            messagebox.showerror("Error", "Enter Account Number first.")
            return
        idx = self._find_index_by_acc(acc_number)
        if idx == -1:
            messagebox.showerror("Error", "Account number does not exist.")
            return
        dialog = tk.Toplevel(self.root)
        dialog.title("Make Transaction")
        dialog.resizable(False, False)
        tk.Label(dialog, text=f"Account: {acc_number}").grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 4))
        tk.Label(dialog, text="Type:").grid(row=1, column=0, sticky="e", padx=10, pady=6)
        ttype_var = tk.StringVar(value="Credit")
        ttk.Combobox(dialog, state="readonly", textvariable=ttype_var,
                     values=["Credit", "Debit", "Loan"]).grid(row=1, column=1, padx=10, pady=6)
        tk.Label(dialog, text="Amount:").grid(row=2, column=0, sticky="e", padx=10, pady=6)
        amount_entry = tk.Entry(dialog)
        amount_entry.grid(row=2, column=1, padx=10, pady=6)

        def do_txn():
            amt = self._parse_balance(amount_entry.get().strip(), "Amount")
            if amt is None:
                return
            if amt <= 0:
                messagebox.showerror("Error", "Amount must be positive.")
                return
            customer = self.customer_data[idx]
            if ttype_var.get().lower() == "credit":
                customer["balance"] += amt
            elif ttype_var.get().lower() == "debit":
                if customer["balance"] >= amt:
                    customer["balance"] -= amt
                else:
                    messagebox.showerror("Error", "Insufficient funds for debit.")
                    return
            else:
                if customer["balance"] >= amt:
                    customer["balance"] -= amt
                else:
                    messagebox.showerror("Error", "Insufficient funds for loan repayment.")
                    return
            self.save_data()
            messagebox.showinfo("Success", "Transaction completed.")
            dialog.destroy()

        tk.Button(dialog, text="Submit", command=do_txn, width=12).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(dialog, text="Cancel", command=dialog.destroy, width=12).grid(row=3, column=1, padx=10, pady=10)

    def load_data(self):
        self.customer_data = []
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    bal = float(row.get("balance", "0") or "0")
                except ValueError:
                    bal = 0.0
                self.customer_data.append({
                    "account_number": row.get("account_number", "").strip(),
                    "customer_name": row.get("customer_name", "").strip(),
                    "balance": bal
                })

    def save_data(self):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            writer.writeheader()
            for row in self.customer_data:
                writer.writerow({
                    "account_number": row["account_number"],
                    "customer_name": row["customer_name"],
                    "balance": f"{row['balance']:.2f}"
                })


if __name__ == "__main__":
    root = tk.Tk()
    app = BankManagementSystem(root)
    root.mainloop()
