from cryptography.fernet import Fernet
import os

key = os.getenv("FERNET_SECRET_KEY").encode()
cipher = Fernet(key)

# Encrypt
def encrypt_data(data: dict) -> str:
    import json
    return cipher.encrypt(json.dumps(data).encode()).decode()

# Decrypt
def decrypt_data(token: str) -> dict:
    return json.loads(cipher.decrypt(token.encode()).decode())

