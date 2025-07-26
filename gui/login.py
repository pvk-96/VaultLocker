import tkinter as tk
from tkinter import ttk
from auth.user_auth import register_user, login_user
from gui.dashboard import DashboardWindow

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

        self.status_label = ttk.Label(self.frame, text="", foreground="red")
        self.status_label.grid(row=3, column=0, columnspan=2, pady=(5, 10))

        self.login_button = ttk.Button(self.frame, text="Login", command=self.login)
        self.login_button.grid(row=4, column=0, pady=10, sticky=tk.E)

        self.register_button = ttk.Button(self.frame, text="Register", command=self.register)
        self.register_button.grid(row=4, column=1, pady=10, sticky=tk.W)

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