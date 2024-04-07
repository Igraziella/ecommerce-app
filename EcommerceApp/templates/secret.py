import secrets
import os

#Generate a random 32-byte (256-bit) key
secret_key = os.urandom(32)

# Convert the binary key to a hexadecimal string
secret_key_hex = secret_key.hex()

print("Generated Secret Key:", secret_key_hex)