import bcrypt

def hash_pwd_bcrypt(plain_pwd: str) -> str:
    pwd_bytes = plain_pwd.encode("utf-8")
    salt = bcrypt.gensalt()

    hashed_pwd = bcrypt.hashpw(pwd_bytes, salt)

    return hashed_pwd.decode("utf-8")

def verify_pwd_hash(plain_pwd: str, hashed_pwd: str) -> bool:
    return bcrypt.checkpw(
        plain_pwd.encode("utf-8"),
        hashed_pwd.encode("utf-8")
    )
