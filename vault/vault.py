import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

# Constants
SALT_SIZE = 16  # bytes
KDF_ITERATIONS = 100_000


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a Fernet key from the password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def encrypt_file(input_path: str, output_path: str, password: str) -> bytes:
    """Encrypt a file and write to output_path. Returns the salt used."""
    salt = os.urandom(SALT_SIZE)
    key = derive_key(password, salt)
    fernet = Fernet(key)
    with open(input_path, 'rb') as f:
        data = f.read()
    encrypted = fernet.encrypt(data)
    with open(output_path, 'wb') as f:
        f.write(salt + encrypted)  # prepend salt
    return salt


def decrypt_file(input_path: str, output_path: str, password: str) -> bool:
    """Decrypt a file and write to output_path. Returns True if successful."""
    with open(input_path, 'rb') as f:
        filedata = f.read()
    salt = filedata[:SALT_SIZE]
    encrypted = filedata[SALT_SIZE:]
    key = derive_key(password, salt)
    fernet = Fernet(key)
    try:
        decrypted = fernet.decrypt(encrypted)
    except Exception:
        return False
    with open(output_path, 'wb') as f:
        f.write(decrypted)
    return True 