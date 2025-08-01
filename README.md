# 🔐 VaultLocker

A secure, offline desktop vault application for storing your sensitive files, notes, and credentials—protected by strong encryption and a beautiful, modern interface.

---

## 🚀 Features

- **Master password login** (bcrypt-hashed, never stored in plaintext)
- **Per-user encrypted vault**: Each user only sees and manages their own files
- **AES file encryption** (Fernet, with PBKDF2 key derivation)
- **Add, download, and securely delete files**
- **Change password** (with automatic re-encryption of all your files)
- **Auto-lock on inactivity** (vault locks after 2 minutes of no activity)
- **Password strength meter** (real-time feedback during registration and password change)
- **Show/hide password toggle** for easier entry.
- **Midnight blue dark mode** for a polished, modern look.
- **Status bar notifications** for all major actions.
- **Cross-platform**: Works on Windows and Linux.

---

## 🛡️ Security Highlights

- Passwords are hashed with bcrypt (never stored in plaintext)
- Files are encrypted with AES (Fernet) using a key derived from your password (PBKDF2 + salt)
- Each file is associated with its owner—users cannot access each other's files
- Secure file deletion: files are overwritten with random data before removal
- Auto-lock ensures your vault is never left open

---

## 🖥️ Installation & Setup

### 1. **Requirements**
- Python 3.8 or newer (tested up to Python 3.13)
- Tkinter (usually included with Python)
- Pip (Python package manager)


### 2. **Clone or Download the Project**
```bash
git clone https://github.com/pvk-96/VaultLocker.git
cd VaultLocker
```
Or, if using the zip file, extract the file into a new folder and go to the next step.


### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```
If you don't have a `requirements.txt`, install these modules:
```bash
pip install bcrypt cryptography
```

### 4. **Run the App**
- **Windows:**
  ```bash
  python vaultlocker\main.py
  ```
- **Linux:**
  ```bash
  python vaultlocker/main.py
  ```

---

## 📝 Usage Guide

1. **Register a new account** with a strong password (see the strength meter for guidance).
2. **Login** with your credentials.
3. **Add files** to your vault—they are encrypted and only visible to you.
4. **Download files** (decrypts with your password).
5. **Delete files** (securely wipes them from disk).
6. **Change your password** at any time (all your files will be re-encrypted).
7. **Auto-lock**: If you’re inactive for 2 minutes, the vault will lock and require login again.
8. **Logout** at any time to protect your vault.

---

## 🐞 Troubleshooting
- If you see errors about missing modules, make sure you installed all dependencies with `pip install -r requirements.txt`.
- If you have issues with Tkinter, ensure it’s installed (on Linux, you may need `sudo apt install python3-tk`).
- If you upgrade Python, re-install the dependencies in your new environment.

---

## 💡 Notes for Testers
- Each user only sees their own files—test with multiple accounts!
- Password changes will re-encrypt all your files.
- Secure deletion is enabled—deleted files cannot be recovered.
- The app is designed for local, offline use. No data ever leaves your machine.

---

## 📦 Packaging (Optional)
To create a standalone executable (no Python required):

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Build the app:
   ```bash
   pyinstaller --onefile vaultlocker/main.py
   ```
   - On Windows, the executable will be in `dist\main.exe`
   - On Linux, it will be in `dist/main`

---

## 🤝 Contributing & Feedback
Pull requests and feedback are welcome! Please file an issue for bugs or feature requests.

---

## 📝 License
MIT License. Use, modify, and share freely. 

## 🖼️ Screenshots

### Login Screen
![Login Screen](ss/homepage)

### File Vault (Dashboard)
![File Vault](ss/files)

### Change Password Dialog
![Change Password](ss/password)

### File Space/Usage Example
![File Space](ss/filespace) 
