# Code By Praneeth Varma Kopperla
# Contact Info: praneethvarma.kopperla@gmail.com GitHub: https://github.com/pvk-96
# Collaborators are welcome to contribute to the project.
# This is a simple vault locker application that allows you to store and retrieve files securely.
# The application is built using tkinter and ttk for the GUI.
# 
import tkinter as tk
from tkinter import ttk
import os
from gui.login import LoginWindow

def load_midnight_theme(root):
    style = ttk.Style(root)
    theme_path = os.path.join(os.path.dirname(__file__), 'gui', 'assets', 'style.theme')
    try:
        style.theme_create('MidnightBlue', parent='clam', settings={})
        style.theme_use('MidnightBlue')
        
        style.configure('.', background='#101a2b', foreground='#e0e6f0', font=('Arial', 11))
        style.configure('TFrame', background='#101a2b')
        style.configure('TLabel', background='#101a2b', foreground='#e0e6f0', font=('Arial', 11))
        style.configure('TButton', background='#18294a', foreground='#e0e6f0', bordercolor='#22335a', font=('Arial', 11, 'bold'), padding=6)
        style.map('TButton', background=[('active', '#28406e')])
        style.configure('TEntry', fieldbackground='#18294a', foreground='#e0e6f0', bordercolor='#22335a', font=('Arial', 11))
        style.configure('TListbox', background='#18294a', foreground='#e0e6f0', selectbackground='#28406e', selectforeground='#ffffff', bordercolor='#22335a', font=('Arial', 11))
        style.configure('TScrollbar', background='#22335a', troughcolor='#101a2b')
        style.configure('TPanedwindow', background='#101a2b', bordercolor='#22335a')
        style.configure('TStatusbar', background='#18294a', foreground='#b0b8c9', font=('Arial', 10, 'italic'))
    except Exception:
        pass  

def main():
    root = tk.Tk()
    root.title("VaultLocker - Secure Vault")
    root.geometry("400x350")
    load_midnight_theme(root)
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main() 