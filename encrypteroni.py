import hashlib
import base64
import string
import random

# Character sets used in the final encrypted output
LETTERS = string.ascii_letters
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?/|\\"
ALL_CHARS = LETTERS + DIGITS + SYMBOLS

def generate_encrypted_input(user_input, salt):
    """
    Generates a secure, deterministic 10-character encrypted output
    based on a user input and a unique salt (e.g. email).
    
    Parameters:
    - user_input (str): The main input string (like a password).
    - salt (str): A unique, case-insensitive string used to differentiate outputs.
    Returns:
    - str: A 10-character string using letters, digits, and at least one symbol.
    """
    # Normalize salt to lowercase for consistency
    salt = salt.lower()
    combined = (user_input + salt).encode()

    # Create SHA-256 hash and encode in Base64
    hash_bytes = hashlib.sha256(combined).digest()
    base64_hash = base64.b64encode(hash_bytes).decode()

# Seed random generator for deterministic shuffling
    random.seed(hash_bytes)

    # Filter Base64 characters into allowed characters
    filtered = [c for c in base64_hash if c in ALL_CHARS]

    # Pad if less than 10 characters
    while len(filtered) < 10:
        filtered += random.choices(ALL_CHARS, k=10)

    # Shuffle for added variation
    random.shuffle(filtered)

    # Ensure at least one symbol in the result
    if not any(c in SYMBOLS for c in filtered[:10]):
        idx = random.randint(0, 9)
        filtered[idx] = random.choice(SYMBOLS)

    return ''.join(filtered[:10])

if __name__ == "__main__":
    # User-friendly input labels
    user_input = input("Enter your input 🔑: ")
    salt = input("Enter your salt 🧂: ")

    encrypted = generate_encrypted_input(user_input, salt)
    print(f"\n🔒 Encrypted input 🙏: {encrypted}")
