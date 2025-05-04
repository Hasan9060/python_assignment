# Develop a streamlit-based secure data storage and retrieval system

import streamlit as st
import hashlib
import json
import os
import time
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from hashlib import pbkdf2_hmac


# === data inforamation of user ===
DATA_FILE = "secure_data.json"
SALT = b"secure_salt_value"
LOCKOUT_DURATION = 60  # in seconds
MAX_ATTEMPTS = 3


# === section login deatails ===
if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = None

if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

if "lockout_time" not in st.session_state:
    st.session_state.lockout_time = 0

#if data is load ==
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {}
    
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def generate_key(passkey):
    key = pbkdf2_hmac('sha256', passkey.encode(), SALT, 100000)
    return urlsafe_b64encode(key)

def hash_password(password):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), SALT, 100000).hex()

# === cryptography.fernet used ===
def encrypt_text(text, key):
    cipher = Fernet(generate_key(key))
    return cipher.encrypt(text.encode().decode())

def decrypt_text(encrypted_text, key):
    try:
        cipher = Fernet(generate_key(key))
        return cipher.decrypt(encrypted_text.encode()).decode()
    except:
        return None
    
stored_data = load_data()

#  === navigation bar ===
st.sidebar.title("🔐Secure Data Encryption System")
menu = ["Home", "Register", "Login", "Store Data", "Retrieval Data"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.title("Welcome to Secure Data Encryption System")
    st.markdown("Develop a Streamlit-based secure data storage and retrieval system where: users store data with  a password, and the data is encrypted using the Fernet symmetric encryption algorithm. The data is stored in a JSON file and can be retrieved using the same password. The system also includes a login feature to authenticate users before accessing the data storage and retrieval features.")

# User registration ===
elif choice == "Register":
    st.title("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if username and password:
            if username in stored_data:
                st.warning("User already exists")
            else:
                stored_data[username] = {
                    "password": hash_password(password),
                    "data": []
                }
                save_data(stored_data)
                st.success("✅ User registered successfully!")
        else:
            st.error("Both fields are required.")
    elif choice == "Login":
        st.subheader("🔑 User Login")

        if time.time() <st.session_state.lockout_time:
            remaining = int(st.session_state.lockout_time - time.time())
            st.error(f"⌚ Too many failed attempts. please wait {remaining} seconds.")
            st.stop()

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in stored_data and stored_data[username]["password"] == hash_password(password):
                st.session_state.authenticated_user = username
                st.session_statefailed_attempts = 0
                st.success(f"✅ Welcome back, {username}!")
            else:
                st.session_state.failed_attempts += 1
                remaining= 3 - st.session_state.failed_attempts
                st.error(f"❌ Incorrect username or password. {remaining} attempts remaining.")

                if st.session_state.failed_attempts >= 3:
                    st.session_state.lockout_time = time.time() + LOCKOUT_DURATION
                    st.error(f"⌚ Too many failed attempts. please wait {LOCKOUT_DURATION} seconds.")
                    st.stop()

# === data store section ===
elif choice == "Store Data":
    if not st.session_state.authenticated_user:
        st.error("🔐 Please login First.")
    else:
        st.subheader("📝 Store Encrypted Data")
        data = st.text_area("Enter data to store")
        passkey = st.text_input("Encrypted key (passpharse)", type="password")

        if st.button("Encrpted And Save"):
            if data and passkey:
                encrypted_data = encrypt_text(data, passkey)
                stored_data[st.session_state.authenticated_user]["data"].append(encrypted)
                save_data(stored_data)
                st.success("✅ Data stored successfully!")
            else:
                st.error("Both fields are required to fill.")

# === data retieve data section ===
elif choice == "Retieve Data":
    if not st.session_state.authenticated_user:
        st.warning("🔐 Please login First.")
    else:
        st.subheader("📝 Retrieve Encrypted Data")
        user_data = stored_data.get(st.session_state.authenticated_user, {}).get("data", [])
    
        if not user_data:
            st.info("No Data Found!")
        else:
            st.write("Encryted Data Enteries:")
            for i, item in enumerate(user_data):
                st.code(item,language="text")

            encrypted_input = st.text_input("Enter Encrypted Data")
            passkey = st.text_input("Enter Passkey T Decrypt", type="password")

            if st.button("Decrypt"):
                result = decrypt_text(encrypted_input, passkey)
                if result:
                    st.success(f"✅ Decrypted Data: {result}")
                else:
                    st.error("❌ Invalid Passkey or corrupted data")
        
    



   
 
    
