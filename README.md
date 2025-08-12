# Password Manager (CLI)

A simple command-line utility that manages a list of credentials stored in a file that can be updated (insert / update / delete). All passwords are **encrypted** with a **master password** that must be provided for every operation.

- **Input format:** `pwmanager.py <master_password> -<operation> <website> <username> <password>`
- **Output file:** `pwmanager.db` (encrypted passwords)

## Features
- Add new credentials (or update an existing website entry)
- Retrieve and decrypt a password for a given website
- Delete a website entry
- List websites available to the current master password
- AES-based encryption via `cryptography` (Fernet) derived from the master password

## Requirements
- Python 3.8+
- `cryptography` library

```bash
pip install cryptography
```

## Usage

```bash
# General form
python pwmanager.py <master_password> -<operation> [<website> <username> <password>]
```

### Operations

| Operation | Command format | Description |
|---|---|---|
| Add / Update | `python pwmanager.py <master_password> -add <website> <username> <password>` | Creates or overwrites the entry for `<website>` with the encrypted password. |
| Get | `python pwmanager.py <master_password> -get <website>` | Prints the username and **decrypted** password for `<website>`. |
| Remove | `python pwmanager.py <master_password> -remove <website>` | Deletes the entry for `<website>`. |
| List | `python pwmanager.py <master_password> -list` | Lists the websites that can be decrypted using the given master password. |

### Examples

```bash
# Insert
python pwmanager.py <master_password> -add gmail.com johndoe@google.com cookie123

# Retrieve
python pwmanager.py <master_password> -get gmail.com

# Delete
python pwmanager.py <master_password> -remove gmail.com

# List all websites saved for this master password
python pwmanager.py <master_password> -list
```

## Data file

- All data is stored in `pwmanager.db` (a plain text file containing encrypted passwords and usernames as JSON-like content).
- The file is updated on each operation.

## Security notes
- **Do not lose the master password.** Entries cannot be decrypted without it.
- The master password is used to derive an encryption key (SHA-256 → Fernet).
