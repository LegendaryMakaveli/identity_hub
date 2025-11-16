import os
from cryptography.fernet import Fernet


KEY_FILE = "secret.key"


class Encryptor:
    def __init__(self):
        self.fernet = self.load_key()

    def load_key(self):
        if not os.path.exists(KEY_FILE):
            key = Fernet.generate_key()
            with open(KEY_FILE, "wb") as file:
                file.write(key)
        else:
            with open(KEY_FILE, "rb") as file:
                key = file.read()

        return Fernet(key)

    def encrypt(self, password):
        return self.fernet.encrypt(password.encode()).decode()

    def verify(self, encrypted_password, plain_password):
        try:
            decrypted = self.fernet.decrypt(encrypted_password.encode()).decode()
            return decrypted == plain_password
        except:
            return False
