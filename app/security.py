from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()  # argon2 z zalecanymi parametrami


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)
