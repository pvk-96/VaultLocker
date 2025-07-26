import tkinter as tk
from tkinter import ttk

class DashboardWindow:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        self.frame = ttk.Frame(master, padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Top label
        self.title_label = ttk.Label(self.frame, text=f"Welcome, {username}", font=("Arial", 14, "bold"))
        self.title_label.pack(pady=(0, 10))

        # Main panels
        self.main_pane = ttk.PanedWindow(self.frame, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        # Left: File list
        self.left_panel = ttk.Frame(self.main_pane, width=250)
        self.main_pane.add(self.left_panel, weight=1)
        self.file_list_label = ttk.Label(self.left_panel, text="Vault Files:")
        self.file_list_label.pack(anchor=tk.W)
        self.file_listbox = tk.Listbox(self.left_panel, height=15)
        self.file_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

        # Right: Actions
        self.right_panel = ttk.Frame(self.main_pane, width=150)
        self.main_pane.add(self.right_panel, weight=0)
        self.add_button = ttk.Button(self.right_panel, text="Add File", command=self.add_file)
        self.add_button.pack(fill=tk.X, pady=5)
        self.download_button = ttk.Button(self.right_panel, text="Download File", command=self.download_file)
        self.download_button.pack(fill=tk.X, pady=5)
        self.delete_button = ttk.Button(self.right_panel, text="Delete File", command=self.delete_file)
        self.delete_button.pack(fill=tk.X, pady=5)
        self.refresh_button = ttk.Button(self.right_panel, text="Refresh Vault", command=self.refresh_vault)
        self.refresh_button.pack(fill=tk.X, pady=5)
        self.logout_button = ttk.Button(self.right_panel, text="Logout", command=self.logout)
        self.logout_button.pack(fill=tk.X, pady=(20, 5))

        # Bottom status bar
        self.status_var = tk.StringVar(value="Ready.")
        self.status_bar = ttk.Label(self.frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))

    def add_file(self):
        self.status_var.set("Add File clicked (not implemented)")

    def download_file(self):
        self.status_var.set("Download File clicked (not implemented)")

    def delete_file(self):
        self.status_var.set("Delete File clicked (not implemented)")

    def refresh_vault(self):
        self.status_var.set("Refresh Vault clicked (not implemented)")

    def logout(self):
        self.status_var.set("Logout clicked (not implemented)") 