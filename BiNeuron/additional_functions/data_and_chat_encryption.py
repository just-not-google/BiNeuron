from cryptography.fernet import Fernet


def data_and_chat_encryption(filepath: str):
    master_key = Fernet.generate_key()
    with open("master.key", "wb") as f:
        f.write(master_key)

