__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."
from cryptography.fernet import Fernet


class KeyEncryption(object):
    """
        Encrypt and decrypt a key through a Fernet generator. The encrypted key is encoded
        as an array of bytes.
    """
    key: bytes = Fernet.generate_key()
    fernet = Fernet(key)

    def encrypt(self, key: str) -> bytes:
        return self.fernet.encrypt(key.encode())

    def decrypt(self, encryptedKey: bytes) -> str:
        return self.fernet.decrypt(encryptedKey).decode()
