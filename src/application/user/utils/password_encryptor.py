from passlib.context import CryptContext


class PasswordEncryptor:
    def __init__(self, pwd_context: CryptContext):
        self.pwd_context = pwd_context

    def encrypt_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)
