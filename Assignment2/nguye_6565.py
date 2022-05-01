# Samson Nguyen
# 1001496565
# 4381 Info Sec II Assignment 2 pt 1
# 4/7/2022

import re
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, padding

vault_dir = "vault/"
auth_file_path = "vault/_auth"


def encrypt(content: bytes, key: bytes, iv: bytes, algorithm="AES"):
    if algorithm == "AES":
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    elif algorithm == "DES":
        cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
    else:
        cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    return encryptor.update(content) + encryptor.finalize()


def decrypt(content: bytes, key: bytes, iv: bytes, algorithm="AES"):
    if algorithm == "AES":
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    elif algorithm == "DES":
        cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
    else:
        cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(content) + decryptor.finalize()


def create_hash(content: bytes, algorithm="SHA-3"):
    if algorithm == "SHA-3":
        # SHA-3
        digest = hashes.Hash(hashes.SHA3_256())
    else:
        # SHA-2
        digest = hashes.Hash(hashes.SHA256())
    digest.update(content)
    return digest.finalize()


def login_or_register():
    login_input = ""
    login_input = input("Login(1) or Register(2)?")[0]
    if login_input != "1" and login_input != "2":
        print("Invalid input. Type 1 or 2.")
    elif login_input == "1":
        # login
        u_p = [line.split(",") for line in open(auth_file_path)]
        username = input("Username:")
        password = input("Password:")
        for account in u_p:
            if (account[0], account[1]) == (username, str(create_hash(bytes(password, 'utf-8')))):
                print("Login accepted.")
                sk = account[2]
                return bytes.fromhex(sk)
        print("Invalid credentials.")
    elif login_input == "2":
        # register
        u_p = [line.split(",") for line in open(auth_file_path)]
        print("Password be minimum 8 characters and must contain: lowercase, uppercase, number, and special character")
        reg = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$"
        pat = re.compile(reg)
        username = input("Username:")
        password = input("Password:")
        if len(u_p) > 0 and username in u_p[:][0]:
            print("Username already exists.")
        else:
            # password validation https://www.geeksforgeeks.org/password-validation-in-python/
            mat = re.search(pat, password)
            if mat:
                # valid password
                auth_file = open(auth_file_path, 'w+')
                pass_hash = create_hash(bytes(password, 'utf-8'))
                super_key = os.urandom(32)
                auth_file.write(username + "," + str(pass_hash) + "," + super_key.hex())
                auth_file.close()
            else:
                # invalid password
                print("Invalid password.")
    return None


def encrypt_file(super_key):
    input_file_path = input("Path to file to encrypt:")
    if os.path.isfile(input_file_path):
        enc_alg = input("Encryption algorithm(AES/DES/CAST5):")
        if enc_alg in ["AES", "DES", "CAST5"]:
            # open input file
            input_file = open(input_file_path, "rb")
            # generate key and iv for file encryption
            key = os.urandom(32)
            iv = os.urandom(16)
            # pad file
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(input_file.read()) + padder.finalize()
            # encrypt file data
            encrypted_data = encrypt(padded_data, key, iv, enc_alg)
            encrypted_file = open(vault_dir + input_file.name + ".encrypted", "wb")
            # store 128-bit iv at beginning of encrypted file
            encrypted_file.write(iv)
            encrypted_file.write(encrypted_data)
            encrypted_file.close()
            # encrypt key for storage using user's super key
            key_file = open(vault_dir + input_file.name + ".key", "wb")
            iv = os.urandom(16)
            encrypted_key = encrypt(key, super_key, iv)
            key_file.write(iv)
            key_file.write(encrypted_key)
            key_file.close()
        else:
            print("Invalid algorithm.")
    else:
        print("File does not exist.")


def decrypt_file(super_key):
    print("(Leave out .encrypted)")
    input_file_path = input("File to decrypt:")
    if os.path.exists(vault_dir + input_file_path + ".encrypted"):
        # open input file
        input_file = open(vault_dir + input_file_path + ".encrypted", "rb")
        if os.path.exists(vault_dir + input_file_path + ".key"):
            # open key file
            key_file = open(vault_dir + input_file_path + ".key", "rb")
            # extract key
            iv = key_file.read(16)
            key = decrypt(key_file.read(), super_key, iv)
            key_file.close()
            enc_alg = input("Encryption algorithm(AES/DES/CAST5):")
            if enc_alg in ["AES", "DES", "CAST5"]:
                # retrieve iv
                iv = input_file.read(16)
                # decrypt file data
                unpadder = padding.PKCS7(128).unpadder()
                padded_data = decrypt(input_file.read(), key, iv, enc_alg)
                decrypted_data = unpadder.update(padded_data) + unpadder.finalize()
                decrypted_file = open(input_file_path, "wb")
                decrypted_file.write(decrypted_data)
                decrypted_file.close()
                input_file.close()
            else:
                print("Invalid algorithm.")
        else:
            print("Key file does not exist.")
    else:
        print("File does not exist.")


def hash_file():
    input_file_path = input("Path to file to hash:")
    if os.path.isfile(input_file_path):
        hash_alg = input("Hash algorithm(SHA-2/SHA-3):")
        if hash_alg in ["SHA-2", "SHA2", "SHA-3", "SHA3"]:
            input_file = open(input_file_path, "rb")
            hashed_data = create_hash(input_file.read(), hash_alg)
            hash_file = open(vault_dir + input_file.name + ".hash", 'wb')
            hash_file.write(hashed_data)
            input_file.close()
            hash_file.close()
            print("Hashed data:", str(hashed_data))
        else:
            print("Invalid algorithm.")
    else:
        print("File does not exist.")


def download_file():
    download_file_name = input("File to download:")
    if os.path.exists(vault_dir + os.path.basename(download_file_name)):
        d_file = open(vault_dir + download_file_name, 'rb')
        u_file = open(download_file_name, 'wb')
        u_file.write(d_file.read())
        d_file.close()
        u_file.close()
    else:
        print(download_file_name + " does not exist in vault.")


def remove_file():
    input_file_name = input("File to remove from vault:")
    if input_file_name != "_auth" and os.path.isfile(vault_dir + input_file_name):
        os.remove(vault_dir + input_file_name)
    else:
        print(input_file_name + " does not exist in vault.")


if __name__ == "__main__":
    if not os.path.exists(vault_dir):
        os.mkdir(vault_dir)
    user_super_key = None
    while user_super_key is None:
        user_super_key = login_or_register()
    main_menu = """Inputs:
    1: submit plaintext file for encryption
    2: create file hash
    3: download a file from the vault
    4: remove a file from the vault
    5: decrypt a file"""
    while True:
        print("vault contents:", os.listdir(vault_dir))
        print(main_menu)
        user_input = input("Input:")[0]
        if user_input not in ["1", "2", "3", "4", "5"]:
            print("Invalid input. Type 1, 2, 3, 4, or 5.")
        elif user_input == "1":
            # encrypt file
            encrypt_file(user_super_key)
        elif user_input == "2":
            # create file hash
            hash_file()
        elif user_input == "3":
            # download file
            download_file()
        elif user_input == "4":
            # remove file
            remove_file()
        elif user_input == "5":
            # decrypt file
            decrypt_file(user_super_key)
        else:
            print("...")
