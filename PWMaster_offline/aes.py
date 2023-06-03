from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Util.Padding import pad, unpad

salt = get_random_bytes(16)

with open('user_log.txt', "r") as file:
    lines = file.readlines()
    password_line = lines[1].strip() 
    password = password_line.split(",")[1].strip()

key = scrypt(password, salt, key_len=32, N=2**14, r=8, p=1)

def encrypt_password(password, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(password.encode('utf-8'), AES.block_size))
    return salt + cipher.iv + ciphertext

def decrypt_password(ciphertext, key):
    salt = ciphertext[:16]
    iv = ciphertext[16:32]
    ciphertext = ciphertext[32:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode('utf-8')