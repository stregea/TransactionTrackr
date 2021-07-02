import hashlib
import uuid


def encrypt_string(string_to_encrypt: str) -> str:
    """
    Hash a string for a user.
    :param string_to_encrypt: The string to hash.
    :return: The hashed version of the string in the form: 'hash:salt'.
    """
    salt = uuid.uuid4().hex
    return f"{hashlib.sha256(salt.encode()+string_to_encrypt.encode()).hexdigest()}:{salt}"


def match(hashed_string: str, string_to_encrypt: str):
    """
    Determine if a string matches a specified hashed counterpart.
    :param hashed_string: The string containing the hashed string and the salt for encryption.
    :param string_to_encrypt: The non-hashed string to be hashed and compared to the original hashed string.
    :return: True if the hashed strings match, False otherwise.
    """
    string, salt = hashed_string.split(":")
    temp_hash = hashlib.sha256(salt.encode()+string_to_encrypt.encode()).hexdigest()
    return string == temp_hash
