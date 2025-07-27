import tkinter as tk
from tkinter import ttk
from auth.user_auth import register_user, login_user
from gui.dashboard import DashboardWindow
import re

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(master, padding=20)
        self.frame.pack(expand=True)

        self.title_label = ttk.Label(self.frame, text="VaultLocker Login", font=("Arial", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(self.frame, text="Username:").grid(row=1, column=0, sticky=tk.E, pady=5)
        self.username_entry = ttk.Entry(self.frame, width=25)
        self.username_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.frame, text="Password:").grid(row=2, column=0, sticky=tk.E, pady=5)
        self.password_entry = ttk.Entry(self.frame, width=25, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)
        self.password_entry.bind('<KeyRelease>', self.update_strength)

        # Show/hide password button
        self.show_password = False
        self.toggle_btn = ttk.Button(self.frame, text="Show", width=6, command=self.toggle_password)
        self.toggle_btn.grid(row=2, column=2, padx=(5,0))

        self.strength_label = ttk.Label(self.frame, text="", font=("Arial", 10))
        self.strength_label.grid(row=3, column=0, columnspan=3, pady=(0, 5))

        self.status_label = ttk.Label(self.frame, text="", foreground="red")
        self.status_label.grid(row=4, column=0, columnspan=3, pady=(5, 10))

        self.login_button = ttk.Button(self.frame, text="Login", command=self.login)
        self.login_button.grid(row=5, column=0, pady=10, sticky=tk.E)

        self.register_button = ttk.Button(self.frame, text="Register", command=self.register)
        self.register_button.grid(row=5, column=1, pady=10, sticky=tk.W)

    def toggle_password(self):
        self.show_password = not self.show_password
        if self.show_password:
            self.password_entry.config(show="")
            self.toggle_btn.config(text="Hide")
        else:
            self.password_entry.config(show="*")
            self.toggle_btn.config(text="Show")

    def password_strength(self, password):
        if len(password) < 8 or len(password) > 16:
            return "Password must be 8-16 characters.", "#e57373"
        if not re.search("[a-z]", password):
            return "Add a lowercase letter.", "#e57373"
        if not re.search("[A-Z]", password):
            return "Add an uppercase letter.", "#e57373"
        if not re.search("[0-9]", password):
            return "Add a digit.", "#e57373"
        if not re.search("[@#$&_]", password):
            return "Add a special char (@#$&_).", "#e57373"
        if re.search(r"\s", password):
            return "No spaces allowed.", "#e57373"
        if len(password) < 12:
            return "Medium strength password.", "#ffd54f"
        return "Strong password!", "#81c784"

    def update_strength(self, event=None):
        password = self.password_entry.get()
        msg, color = self.password_strength(password)
        self.strength_label.config(text=msg, foreground=color)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if not username or not password:
            self.status_label.config(text="Please enter both username and password.")
            return
        success, msg = login_user(username, password)
        self.status_label.config(text=msg, foreground="green" if success else "red")
        if success:
            self.frame.destroy()
            DashboardWindow(self.master, username)

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if not username or not password:
            self.status_label.config(text="Please enter both username and password.")
            return
        success, msg = register_user(username, password)
        self.status_label.config(text=msg, foreground="green" if success else "red") 