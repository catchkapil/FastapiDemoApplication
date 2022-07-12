from passlib.context import CryptContext

# Password Hashing Technique
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify_hash(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
