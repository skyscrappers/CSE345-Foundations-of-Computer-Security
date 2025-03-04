import gmpy2
from Crypto.Cipher import Salsa20
from Crypto.Random import get_random_bytes
from sympy import randprime

# Key for symmetric encryption salsa20
key = get_random_bytes(32)
print("Part A: Alice generates the shared symmetric key ", key)

p = input("Enter a large prime number: ")
q = input("Enter another large prime number: ")

p = gmpy2.mpz(p)
q = gmpy2.mpz(q)

#genarate Bob's public and private keys for RSA
def generate_key(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  
    d = gmpy2.invert(e, phi)
    return (n, e), (n, d)

def encrypt_key(key, public_key):
    n, e = public_key
    key_int = int.from_bytes(key, byteorder='big')
    c = gmpy2.powmod(key_int, e, n)
    return c

def decrypt_key(c, private_key):
    n, d = private_key
    key_int = gmpy2.powmod(c, d, n)
    key_bytes = key_int.to_bytes(32, 'big')  
    return key_bytes


public_key, private_key = generate_key(p, q)
print("\nPart B: Bob generates his asymmetric keys")
print("Bob's Public Key: ", public_key)
print("Bob's Private Key: ", private_key)
ciphertext = encrypt_key(key, public_key)
print("\nPart C: Ciphertext: ", ciphertext)
decrypted_key = decrypt_key(ciphertext, private_key)
print("\nPart D: Decrypted Key: ", decrypted_key)
print("Keys Match:", decrypted_key == key)

message = b"Hello, Alice!"
cipher = Salsa20.new(key=key)
ciphertext = cipher.nonce + cipher.encrypt(message)
print("Part E: Ciphertext:", ciphertext)
nonce = ciphertext[:8]
ciphertext = ciphertext[8:]
cipher = Salsa20.new(key=key, nonce=nonce)
decrypted_message = cipher.decrypt(ciphertext)
print("Part F: Decrypted Message:", decrypted_message)
print("Messages Match:", decrypted_message == message)
