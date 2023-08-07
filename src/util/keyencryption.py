__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2023. All rights reserved."
from cryptography.fernet import Fernet
from typing import AnyStr


class KeyEncryption(object):
    """
        Encrypt and decrypt a key through a Fernet generator. The encrypted key is encoded
        as an array of bytes.
    """
    # key = Fernet.generate_key()
    key = b'D1huLCayW6GbZat2UPLmdYrDASuov1ccN_6q9l1F_io='
    fernet = Fernet(key)

    def encrypt(self, key: AnyStr) -> bytes:
        return self.encrypt_bytes(key.encode())

    def encrypt_bytes(self, key: bytes) -> bytes:
        return self.fernet.encrypt(key)

    def decrypt(self, encryptedKey: bytes) -> AnyStr:
        return self.decrypt_bytes(encryptedKey).decode()

    def decrypt_bytes(self, encryptedKey: bytes) -> bytes:
        return self.fernet.decrypt(encryptedKey)

    def encrypt_file(self, src_file_name: AnyStr, dest_file_name: AnyStr) -> None:
        with open(src_file_name, 'rb') as f:
            clear_content = f.read()
            encrypted_content = self.encrypt_bytes(clear_content)
            with open(dest_file_name, 'wb') as g:
                g.write(encrypted_content)

    def decrypt_file(self, src_file_name: AnyStr, dest_file_name: AnyStr) -> None:
        with open(src_file_name, 'rb') as f:
            clear_content = f.read()
            # bytes_content = bytes(clear_content, 'utf-8')
            decrypted_content = self.decrypt_bytes(clear_content)
            with open(dest_file_name, 'wb') as g:
                g.write(decrypted_content)


if __name__ == '__main__':
    import json
    import os
    keys = ['TOKEN','REFRESH_TOKEN', 'TOKEN_URI', 'CLIENT_ID', 'CLIENT_SECRET', 'EXPIRY']
    gmail_vars = { k.lower(): v for k, v in os.environ.items() if k in keys}
    gmail_vars['scopes'] = ['https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/gmail.send']
    gmail_token_json = json.dumps(gmail_vars)
    with open('tok.json', 'wt') as f:
        f.write(gmail_token_json)






    # key_encryption = KeyEncryption()
    """
    test_key = "This is not a good day!j"
    encrypted = key_encryption.encrypt(test_key)
    decrypted_key = key_encryption.decrypt(encrypted)
    print(decrypted_key)
    """

    # key_encryption.encrypt_file('../creds.json', '../encrypted_credentials')
    # key_encryption.decrypt_file('../encrypted_credentials', '../credsx.json')
