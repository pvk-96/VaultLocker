import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import os
import random
from vault.vault import encrypt_file, decrypt_file
from vault.file_utils import add_file_entry, list_file_entries, delete_file_entry
# from gui.login import LoginWindow  # Removed to fix circular import

AUTOLOCK_SECONDS = 120  # 2 minutes

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
        self.change_pwd_button = ttk.Button(self.right_panel, text="Change Password", command=self.change_password)
        self.change_pwd_button.pack(fill=tk.X, pady=5)
        self.logout_button = ttk.Button(self.right_panel, text="Logout", command=self.logout)
        self.logout_button.pack(fill=tk.X, pady=(20, 5))

        # Bottom status bar
        self.status_var = tk.StringVar(value="Ready.")
        self.status_bar = ttk.Label(self.frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))

        # Ensure vault folder exists
        self.vault_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'vault')
        os.makedirs(self.vault_dir, exist_ok=True)

        
        self.autolock_id = None
        self.reset_autolock()
        self.master.bind_all('<Any-KeyPress>', self.reset_autolock)
        self.master.bind_all('<Any-Button>', self.reset_autolock)
        self.master.bind_all('<Motion>', self.reset_autolock)

        self.refresh_vault()

    def reset_autolock(self, event=None):
        if self.autolock_id:
            self.master.after_cancel(self.autolock_id)
        self.autolock_id = self.master.after(AUTOLOCK_SECONDS * 1000, self.autolock)

    def autolock(self):
        messagebox.showinfo("Auto-Lock", "Vault locked due to inactivity.")
        self.logout()

    def get_selected_entry(self):
        idx = self.file_listbox.curselection()
        if not idx:
            return None
        entries = list_file_entries(self.username)
        return entries[idx[0]] if idx[0] < len(entries) else None

    def add_file(self):
        self.reset_autolock()
        file_path = filedialog.askopenfilename(title="Select file to add to vault")
        if not file_path:
            return
        password = simpledialog.askstring("Password Required", "Enter your vault password:", show='*', parent=self.master)
        if not password:
            self.status_var.set("Add file cancelled: No password entered.")
            return
        original_name = os.path.basename(file_path)
        stored_name = original_name + ".enc"
        stored_path = os.path.join(self.vault_dir, stored_name)
        try:
            encrypt_file(file_path, stored_path, password)
            add_file_entry(original_name, stored_name, self.username)
            self.status_var.set(f"Added and encrypted: {original_name}")
            self.refresh_vault()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add file: {e}")
            self.status_var.set("Failed to add file.")

    def download_file(self):
        self.reset_autolock()
        entry = self.get_selected_entry()
        if not entry:
            self.status_var.set("No file selected.")
            return
        password = simpledialog.askstring("Password Required", "Enter your vault password:", show='*', parent=self.master)
        if not password:
            self.status_var.set("Download cancelled: No password entered.")
            return
        save_path = filedialog.asksaveasfilename(title="Save decrypted file as", initialfile=entry['original_name'])
        if not save_path:
            self.status_var.set("Download cancelled: No save location chosen.")
            return
        stored_path = os.path.join(self.vault_dir, entry['stored_name'])
        success = decrypt_file(stored_path, save_path, password)
        if success:
            self.status_var.set(f"Decrypted and saved: {entry['original_name']}")
        else:
            messagebox.showerror("Error", "Failed to decrypt file. Wrong password or corrupted file.")
            self.status_var.set("Failed to decrypt file.")

    def delete_file(self):
        self.reset_autolock()
        entry = self.get_selected_entry()
        if not entry:
            self.status_var.set("No file selected.")
            return
        confirm = messagebox.askyesno("Confirm Delete", f"Delete {entry['original_name']} from vault?")
        if not confirm:
            self.status_var.set("Delete cancelled.")
            return
        stored_path = os.path.join(self.vault_dir, entry['stored_name'])
        try:
            if os.path.exists(stored_path):
                # Securely overwrite file before deleting
                with open(stored_path, 'r+b') as f:
                    length = os.path.getsize(stored_path)
                    f.write(os.urandom(length))
                    f.flush()
                os.remove(stored_path)
            delete_file_entry(entry['stored_name'], self.username)
            self.status_var.set(f"Deleted: {entry['original_name']}")
            self.refresh_vault()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete file: {e}")
            self.status_var.set("Failed to delete file.")

    def refresh_vault(self):
        self.reset_autolock()
        self.file_listbox.delete(0, tk.END)
        for entry in list_file_entries(self.username):
            display = f"{entry['original_name']} ({entry['date']})"
            self.file_listbox.insert(tk.END, display)
        self.status_var.set("Vault refreshed.")

    def change_password(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Change Password")
        dialog.geometry("340x260")
        dialog.transient(self.master)
        dialog.grab_set()

        # Password fields and show/hide toggles
        tk.Label(dialog, text="Current Password:").pack(pady=(15, 0))
        current_frame = tk.Frame(dialog)
        current_frame.pack()
        current_entry = ttk.Entry(current_frame, show="*")
        current_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        show_current = tk.BooleanVar(value=False)
        def toggle_current():
            if show_current.get():
                current_entry.config(show="*")
                current_toggle.config(text="👁️")
                show_current.set(False)
            else:
                current_entry.config(show="")
                current_toggle.config(text="🙈")
                show_current.set(True)
        current_toggle = ttk.Button(current_frame, text="👁️", width=2, command=toggle_current)
        current_toggle.pack(side=tk.LEFT, padx=2)

        tk.Label(dialog, text="New Password:").pack(pady=(10, 0))
        new_frame = tk.Frame(dialog)
        new_frame.pack()
        new_entry = ttk.Entry(new_frame, show="*")
        new_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        show_new = tk.BooleanVar(value=False)
        def toggle_new():
            if show_new.get():
                new_entry.config(show="*")
                new_toggle.config(text="👁️")
                show_new.set(False)
            else:
                new_entry.config(show="")
                new_toggle.config(text="🙈")
                show_new.set(True)
        new_toggle = ttk.Button(new_frame, text="👁️", width=2, command=toggle_new)
        new_toggle.pack(side=tk.LEFT, padx=2)

        tk.Label(dialog, text="Confirm New Password:").pack(pady=(10, 0))
        confirm_frame = tk.Frame(dialog)
        confirm_frame.pack()
        confirm_entry = ttk.Entry(confirm_frame, show="*")
        confirm_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        show_confirm = tk.BooleanVar(value=False)
        def toggle_confirm():
            if show_confirm.get():
                confirm_entry.config(show="*")
                confirm_toggle.config(text="👁️")
                show_confirm.set(False)
            else:
                confirm_entry.config(show="")
                confirm_toggle.config(text="🙈")
                show_confirm.set(True)
        confirm_toggle = ttk.Button(confirm_frame, text="👁️", width=2, command=toggle_confirm)
        confirm_toggle.pack(side=tk.LEFT, padx=2)

        status = tk.Label(dialog, text="", fg="red")
        status.pack(pady=5)

        def do_change(event=None):
            current_pwd = current_entry.get()
            new_pwd = new_entry.get()
            confirm_pwd = confirm_entry.get()
            if not current_pwd or not new_pwd or not confirm_pwd:
                status.config(text="All fields required.")
                return
            if new_pwd != confirm_pwd:
                status.config(text="New passwords do not match.")
                return
            # Password strength check (reuse logic from login)
            from gui.login import LoginWindow
            msg, color = LoginWindow.password_strength(self, new_pwd)
            if color != "#81c784":
                status.config(text=f"Weak password: {msg}", fg=color)
                return
            # Check current password
            from auth.user_auth import login_user, update_user_password
            success, _ = login_user(self.username, current_pwd)
            if not success:
                status.config(text="Current password incorrect.")
                return
            # Re-encrypt all files
            entries = list_file_entries(self.username)
            for entry in entries:
                if entry['original_name'] and entry['stored_name']:
                    file_path = os.path.join(self.vault_dir, entry['stored_name'])
                    # Decrypt with old password
                    from vault.vault import decrypt_file, encrypt_file
                    tmp_path = file_path + ".tmp"
                    if not decrypt_file(file_path, tmp_path, current_pwd):
                        status.config(text=f"Failed to decrypt {entry['original_name']}.")
                        if os.path.exists(tmp_path):
                            os.remove(tmp_path)
                        return
                    # Encrypt with new password
                    encrypt_file(tmp_path, file_path, new_pwd)
                    os.remove(tmp_path)
            # Update password hash
            update_user_password(self.username, new_pwd)
            status.config(text="Password changed!", fg="#228B22")
            dialog.after(1200, dialog.destroy)
            self.status_var.set("Password changed successfully.")

        # Bind Enter key to confirm
        dialog.bind('<Return>', do_change)
        ttk.Button(dialog, text="Change Password", command=do_change).pack(pady=10)

    def logout(self):
        if self.autolock_id:
            self.master.after_cancel(self.autolock_id)
        self.frame.destroy()
        from gui.login import LoginWindow  # Delayed import to fix circular import
        LoginWindow(self.master) 