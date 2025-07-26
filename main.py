import tkinter as tk
from gui.login import LoginWindow


def main():
    root = tk.Tk()
    root.title("VaultLocker - Secure Vault")
    root.geometry("400x350")
    # Optionally set an icon here if available
    app = LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main() 