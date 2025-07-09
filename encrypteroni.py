import hashlib
import base64
import string
import random
import json
import os
import platform

# Characters used in encrypted output
LETTERS = string.ascii_letters
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?/|\\"
ALL_CHARS = LETTERS + DIGITS + SYMBOLS

# Storage file
DATA_FILE = "encrypted_users.json"

# Clear screen (cross-platform)
def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")

# Encryption method
def generate_encrypted_input(user_input, salt):
    salt = salt.lower()
    combined = (user_input + salt).encode()
    hash_bytes = hashlib.sha256(combined).digest()
    base64_hash = base64.b64encode(hash_bytes).decode()

    random.seed(hash_bytes)
    filtered = [c for c in base64_hash if c in ALL_CHARS]

    while len(filtered) < 10:
        filtered += random.choices(ALL_CHARS, k=10)
    random.shuffle(filtered)

    if not any(c in SYMBOLS for c in filtered[:10]):
        idx = random.randint(0, 9)
        filtered[idx] = random.choice(SYMBOLS)

    return ''.join(filtered[:10])

# Load users from file
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save users to file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Integrity check on startup
def verify_integrity(data):
    print("🔍 Verifying integrity of saved encrypted users...")
    all_valid = True
    for entry in data:
        expected = generate_encrypted_input(entry['input'], entry['salt'])
        if entry['encrypted'] != expected:
            print(f"❌ Integrity mismatch for 🔑 {entry['input']} + 🧂 {entry['salt']}")
            all_valid = False
    if all_valid:
        print("✅ All saved entries passed integrity check!\n")
    else:
        print("⚠️ Some entries are corrupted!\n")

# Display saved users
def show_saved_users(data):
    if not data:
        print("\n📭 No encrypted inputs saved yet.")
        return
    print("\n🗂️ Saved Encrypted Users:")
    for idx, entry in enumerate(data, 1):
        print(f"{idx}. 🔑: {entry['input']} | 🧂: {entry['salt']} | 🙏: {entry['encrypted']}")

# Edit or delete user
def edit_or_delete_user(data):
    if not data:
        print("\n📭 No users to edit or delete.")
        return

    show_saved_users(data)
    try:
        choice = int(input("\nSelect user number to edit/delete: ")) - 1
        if choice < 0 or choice >= len(data):
            print("❌ Invalid choice.")
            return

        action = input("Type 'edit' to modify or 'delete' to remove: ").lower().strip()

        if action == "delete":
            removed = data.pop(choice)
            print(f"🗑️ Deleted user 🔑 {removed['input']} with 🧂 {removed['salt']}.")

        elif action == "edit":
            new_input = input("Enter new input 🔑: ")
            new_salt = input("Enter new salt 🧂: ")
            new_encrypted = generate_encrypted_input(new_input, new_salt)
            data[choice] = {
                "input": new_input,
                "salt": new_salt.lower(),
                "encrypted": new_encrypted
            }
            print(f"✏️ Updated user to 🙏: {new_encrypted}")

        else:
            print("❌ Unknown action.")
    except ValueError:
        print("❌ Invalid input.")

# Main menu
def main():
    clear_screen()
    data = load_data()
    verify_integrity(data)

    print("Select an option:")
    print("1️⃣  Encrypt new input")
    print("2️⃣  View saved encrypted users")
    print("3️⃣  Edit or delete a user")

    choice = input("\nEnter 1, 2 or 3: ").strip()

    if choice == "1":
        user_input = input("Enter your input 🔑: ")
        salt = input("Enter your salt 🧂: ")
        encrypted = generate_encrypted_input(user_input, salt)
        print(f"\n🔒 Encrypted input 🙏: {encrypted}")
        data.append({
            "input": user_input,
            "salt": salt.lower(),
            "encrypted": encrypted
        })
        save_data(data)

    elif choice == "2":
        show_saved_users(data)

    elif choice == "3":
        edit_or_delete_user(data)
        save_data(data)

    else:
        print("\n❌ Invalid choice. Please enter 1, 2 or 3.")

if __name__ == "__main__":
    main()
