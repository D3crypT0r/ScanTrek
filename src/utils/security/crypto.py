from cryptography.fernet import Fernet
import hmac
import hashlib

class CryptoUtils:
    @staticmethod
    def generate_key():
        return Fernet.generate_key()

    @staticmethod
    def encrypt_data(data, key):
        cipher = Fernet(key)
        return cipher.encrypt(data.encode())

    @staticmethod
    def decrypt_data(encrypted_data, key):
        cipher = Fernet(key)
        return cipher.decrypt(encrypted_data).decode()

    @staticmethod
    def secure_hash(data, salt=None):
        if not salt:
            salt = os.urandom(16)
        return hashlib.pbkdf2_hmac('sha256', data.encode(), salt, 100000)

    @staticmethod
    def verify_hmac(message, signature, key):
        expected = hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)
