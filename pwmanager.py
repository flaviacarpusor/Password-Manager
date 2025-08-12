import sys
import os
import base64
import hashlib
from cryptography.fernet import Fernet

DATABASE_FILE = "pwmanager.db"


def generate_key(master_key):
    hashed_key = hashlib.sha256(master_key.encode()).digest()
    return base64.urlsafe_b64encode(hashed_key[:32])


def read_file():
    if not os.path.exists(DATABASE_FILE):
        return {}
    try:
        with open(DATABASE_FILE, "r") as db_file:
            file_content = db_file.read().strip()
            if not file_content or file_content == "{}":
                return {}

            records = eval(file_content)
            return records
    except Exception as error:
        print(f"[ERROR] Eroare la citirea fisierului: {error}")
        return {}


def write_file(stored_data):
    try:
        with open(DATABASE_FILE, "w") as db_file:
            db_file.write("{\n")
            for idx, (site_entry, details) in enumerate(stored_data.items()):
                db_file.write(f'  "{site_entry}": {{\n')
                db_file.write(f'    "username": "{details["username"]}",\n')
                db_file.write(f'    "password": "{details["password"]}"\n')
                db_file.write("  }")
                if idx < len(stored_data) - 1:
                    db_file.write(",\n")
                else:
                    db_file.write("\n")
            db_file.write("}\n")
        print("[STATUS] Fisierul a fost actualizat.")
    except Exception as error:
        print(f"[ERROR] Eroare la salvarea fisierului: {error}")

def add_pw(master_key, site_name, account_name, acc_pw):
    stored_data = read_file()
    encryption_key = Fernet(generate_key(master_key))
    encoded_pw = encryption_key.encrypt(acc_pw.encode()).decode()
    stored_data[site_name] = {"username": account_name, "password": encoded_pw}
    write_file(stored_data)
    print(f"[STATUS] Parola pentru {site_name} a fost adaugata.")

def get_pw(master_key, site_name):
    stored_data = read_file()
    if site_name in stored_data:
        try:
            encryption_key = Fernet(generate_key(master_key))
            decoded_pw = encryption_key.decrypt(stored_data[site_name]["password"].encode()).decode()
            print(f"[STATUS] Website: {site_name}, Utilizator: {stored_data[site_name]['username']}, Parola: {decoded_pw}")
        except Exception:
            print("[ERROR] Parola master este gresita!")
    else:
        print("[ERROR] Nu exista date pentru acest website.")

def delete_pw(master_key, site_name):
    stored_data = read_file()
    if site_name not in stored_data:
        print("[ERROR] Nu exista date pentru acest website.")
        return

    encryption_key = Fernet(generate_key(master_key))
    try:
        encryption_key.decrypt(stored_data[site_name]["password"].encode())
    except Exception:
        print("[ERROR] Parola master nu este corecta!")
        return

    del stored_data[site_name]
    write_file(stored_data)
    print(f"[STATUS] Intrarea pentru {site_name} a fost stearsa.")


def list_sites(master_key):
    stored_data = read_file()
    if not stored_data:
        print("[STATUS] Nu exista site-uri salvate.")
        return

    encryption_key = Fernet(generate_key(master_key))
    valid_sites = []


    for site_entry, details in stored_data.items():
        try:
            encryption_key.decrypt(details["password"].encode())
            valid_sites.append(site_entry)
        except Exception:
            continue

    if valid_sites:
        print("[STATUS] Site-uri salvate:")
        for site in valid_sites:
            print(f"- {site}")
    else:
        print("[ERROR] Parola master este gresita sau nu exista site-uri valide.")


def main():
    if len(sys.argv) < 3:
        print("Utilizare: pwmanager.py <master_password> -<operatie> [<website> <username> <password>]")
        return

    master_key = sys.argv[1]
    command = sys.argv[2]

    if command == "-add" and len(sys.argv) == 6:
        site_name, account_name, acc_pw = sys.argv[3], sys.argv[4], sys.argv[5]
        add_pw(master_key, site_name, account_name, acc_pw)
    elif command == "-get" and len(sys.argv) == 4:
        site_name = sys.argv[3]
        get_pw(master_key, site_name)
    elif command == "-remove" and len(sys.argv) == 4:
        site_name = sys.argv[3]
        delete_pw(master_key, site_name)
    elif command == "-list":
        list_sites(master_key)
    else:
        print("[ERROR] Operatie invalida sau parametri insuficienti.")

if __name__ == "__main__":
    main()

