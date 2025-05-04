import streamlit as st
from cryptography.fernet import Fernet
import hashlib
import json
import os
from pathlib import Path
import time
from datetime import datetime

# Ensure necessary directories exist
os.makedirs('user_data', exist_ok=True)
os.makedirs('uploads', exist_ok=True)

# Encryption key management
def load_or_create_key():
    if os.path.exists('secret.key'):
        with open('secret.key', 'rb') as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open('secret.key', 'wb') as key_file:
            key_file.write(key)
        return key

key = load_or_create_key()
cipher_suite = Fernet(key)

# User management functions
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user_data_dir(username):
    user_dir = f'user_data/{username}'
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

# File encryption/decryption functions
def encrypt_file(file_path, password):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    encrypted_data = cipher_suite.encrypt(file_data)
    return encrypted_data

def decrypt_file(encrypted_data, password):
    try:
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        return decrypted_data
    except:
        return None

def save_encrypted_file(username, file_name, encrypted_data):
    user_dir = create_user_data_dir(username)
    file_path = f'{user_dir}/{file_name}.enc'
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)
    return file_path

def get_user_files(username):
    user_dir = f'user_data/{username}'
    if not os.path.exists(user_dir):
        return []
    return [f for f in os.listdir(user_dir) if f.endswith('.enc')]

# Authentication functions
def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists"
    
    users[username] = {
        'password_hash': hash_password(password),
        'registered_at': datetime.now().isoformat()
    }
    save_users(users)
    create_user_data_dir(username)
    return True, "Registration successful"

def verify_user(username, password):
    users = load_users()
    if username not in users:
        return False, "User not found"
    
    if hash_password(password) == users[username]['password_hash']:
        return True, "Login successful"
    return False, "Incorrect password"

# Data management functions
def delete_data(username, data_key):
    user_dir = create_user_data_dir(username)
    data_file = f'{user_dir}/data.json'
    
    if not os.path.exists(data_file):
        return False, "No data found for this user"
    
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    if data_key not in data:
        return False, "Data key not found"
    
    # If it's a file, delete the encrypted file
    if data[data_key]['type'] == 'file':
        file_path = f"{user_dir}/{data[data_key]['file_name']}"
        if os.path.exists(file_path):
            os.remove(file_path)
    
    # Remove the entry from data
    del data[data_key]
    
    with open(data_file, 'w') as f:
        json.dump(data, f)
    
    return True, "Data deleted successfully"

def update_text_data(username, data_key, new_text, passkey):
    user_dir = create_user_data_dir(username)
    data_file = f'{user_dir}/data.json'
    
    if not os.path.exists(data_file):
        return False, "No data found for this user"
    
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    if data_key not in data:
        return False, "Data key not found"
    
    if data[data_key]['type'] != 'text':
        return False, "Only text data can be updated this way"
    
    # Encrypt the new text
    encrypted_text = encrypt_text(new_text, passkey)
    data[data_key]['encrypted_text'] = encrypted_text.decode()
    data[data_key]['updated_at'] = datetime.now().isoformat()
    
    with open(data_file, 'w') as f:
        json.dump(data, f)
    
    return True, "Text data updated successfully"

# UI Components
def registration_page():
    st.title("👤 User Registration")
    
    username = st.text_input("Choose a username")
    password = st.text_input("Choose a password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")
    
    if st.button("Register"):
        if not username or not password:
            st.error("Username and password are required")
        elif password != confirm_password:
            st.error("Passwords do not match")
        else:
            success, message = register_user(username, password)
            if success:
                st.success(message)
                st.session_state.current_page = "login"
                st.rerun()
            else:
                st.error(message)

def login_page():
    st.title("🔐 User Login")
    
    if 'login_attempts' not in st.session_state:
        st.session_state.login_attempts = 0
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        success, message = verify_user(username, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.login_attempts = 0
            st.success(message)
            time.sleep(1)
            st.rerun()
        else:
            st.session_state.login_attempts += 1
            st.error(f"{message}! Attempts: {st.session_state.login_attempts}/3")
            
            if st.session_state.login_attempts >= 3:
                st.error("Too many failed attempts! Please try again later.")
                time.sleep(5)
                st.rerun()

def dashboard():
    st.sidebar.title(f"🔒 Secure Vault - {st.session_state.username}")
    menu = st.sidebar.selectbox("Menu", ["Store Data", "Retrieve Data", "Manage Data", "Account Info"])
    
    if menu == "Store Data":
        st.header("💾 Store New Data")
        file_type = st.radio("Select data type", ["Text", "File"])
        
        if file_type == "Text":
            user_key = st.text_input("Enter unique name for your data")
            text_data = st.text_area("Enter text to store securely")
            passkey = st.text_input("Create a passkey", type="password")
            
            if st.button("Encrypt & Store"):
                if user_key and text_data and passkey:
                    user_dir = create_user_data_dir(st.session_state.username)
                    data_file = f'{user_dir}/data.json'
                    
                    if os.path.exists(data_file):
                        with open(data_file, 'r') as f:
                            data = json.load(f)
                    else:
                        data = {}
                    
                    if user_key in data:
                        st.warning("This name already exists! Please choose another.")
                    else:
                        encrypted_text = encrypt_text(text_data, passkey)
                        data[user_key] = {
                            "encrypted_text": encrypted_text.decode(),
                            "type": "text",
                            "created_at": datetime.now().isoformat()
                        }
                        with open(data_file, 'w') as f:
                            json.dump(data, f)
                        st.success("Text stored securely! ✅")
                else:
                    st.warning("Please fill all fields!")
        
        else:  # File upload
            st.subheader("Upload File")
            file = st.file_uploader("Choose a file", type=['txt', 'pdf', 'docx', 'png', 'jpg', 'jpeg', 'mp3', 'mp4', 'wav', 'mov'])
            user_key = st.text_input("Enter unique name for this file")
            passkey = st.text_input("Create a passkey for this file", type="password")
            
            if file and user_key and passkey and st.button("Encrypt & Store File"):
                try:
                    # Create uploads directory if not exists
                    os.makedirs('uploads', exist_ok=True)
                    
                    file_path = f"uploads/{file.name}"
                    with open(file_path, "wb") as f:
                        f.write(file.getbuffer())
                    
                    encrypted_data = encrypt_file(file_path, passkey)
                    file_extension = Path(file.name).suffix
                    file_name = f"{user_key}{file_extension}.enc"
                    
                    user_dir = create_user_data_dir(st.session_state.username)
                    encrypted_file_path = f"{user_dir}/{file_name}"
                    
                    with open(encrypted_file_path, 'wb') as f:
                        f.write(encrypted_data)
                    
                    # Save metadata
                    data_file = f'{user_dir}/data.json'
                    
                    if os.path.exists(data_file):
                        with open(data_file, 'r') as f:
                            data = json.load(f)
                    else:
                        data = {}
                    
                    data[user_key] = {
                        "file_name": file_name,
                        "original_name": file.name,
                        "type": "file",
                        "created_at": datetime.now().isoformat()
                    }
                    
                    with open(data_file, 'w') as f:
                        json.dump(data, f)
                    
                    os.remove(file_path)
                    st.success("File encrypted and stored securely! ✅")
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
    
    elif menu == "Retrieve Data":
        st.header("🔓 Retrieve Stored Data")
        
        user_dir = create_user_data_dir(st.session_state.username)
        data_file = f'{user_dir}/data.json'
        
        if not os.path.exists(data_file):
            st.warning("No data found for this user.")
            return
        
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        if not data:
            st.warning("No data found for this user.")
            return
        
        data_items = list(data.items())
        selected_item = st.selectbox("Select data to retrieve", [f"{k} ({v['type']})" for k, v in data_items])
        
        if selected_item:
            selected_key = selected_item.split(" (")[0]
            item_data = data[selected_key]
            
            if 'retrieve_attempts' not in st.session_state:
                st.session_state.retrieve_attempts = 0
            
            passkey = st.text_input(f"Enter passkey for {selected_key}", type="password")
            
            if st.button("Retrieve Data"):
                try:
                    if item_data['type'] == "text":
                        decrypted_text = decrypt_text(item_data["encrypted_text"], passkey)
                        if decrypted_text:
                            st.success("Decrypted Successfully!")
                            st.text_area("Your Text", value=decrypted_text, height=200)
                            st.session_state.retrieve_attempts = 0
                        else:
                            handle_failed_attempt()
                    
                    elif item_data['type'] == "file":
                        encrypted_file_path = f"{user_dir}/{item_data['file_name']}"
                        
                        if not os.path.exists(encrypted_file_path):
                            st.error("File not found in storage. It may have been deleted.")
                            return
                        
                        with open(encrypted_file_path, 'rb') as f:
                            encrypted_data = f.read()
                        
                        decrypted_data = decrypt_file(encrypted_data, passkey)
                        if decrypted_data:
                            st.success("File decrypted successfully!")
                            
                            # Display or download the file based on type
                            file_extension = Path(item_data['original_name']).suffix.lower()
                            
                            if file_extension in ['.png', '.jpg', '.jpeg']:
                                st.image(decrypted_data)
                            elif file_extension in ['.mp3', '.wav']:
                                st.audio(decrypted_data)
                            elif file_extension in ['.mp4', '.mov']:
                                st.video(decrypted_data)
                            else:
                                st.text("File content:")
                                try:
                                    st.text(decrypted_data.decode())
                                except:
                                    st.write("Binary file - download to view")
                            
                            # Download button
                            st.download_button(
                                label="Download File",
                                data=decrypted_data,
                                file_name=item_data['original_name'],
                                mime="application/octet-stream"
                            )
                            st.session_state.retrieve_attempts = 0
                        else:
                            handle_failed_attempt()
                except Exception as e:
                    st.error(f"Error retrieving data: {str(e)}")
    
    elif menu == "Manage Data":
        st.header("🛠️ Manage Your Data")
        
        user_dir = create_user_data_dir(st.session_state.username)
        data_file = f'{user_dir}/data.json'
        
        if not os.path.exists(data_file):
            st.warning("No data found for this user.")
            return
        
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        if not data:
            st.warning("No data found for this user.")
            return
        
        data_items = list(data.items())
        selected_item = st.selectbox("Select data to manage", [f"{k} ({v['type']})" for k, v in data_items])
        
        if selected_item:
            selected_key = selected_item.split(" (")[0]
            item_data = data[selected_key]
            
            st.subheader(f"Manage: {selected_key}")
            
            if item_data['type'] == "text":
                # Update text data
                st.write("Update Text Content")
                new_text = st.text_area("Enter new text content", height=150)
                update_passkey = st.text_input("Enter passkey to update", type="password")
                
                if st.button("Update Text"):
                    if new_text and update_passkey:
                        success, message = update_text_data(
                            st.session_state.username,
                            selected_key,
                            new_text,
                            update_passkey
                        )
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.warning("Please enter both new text and passkey")
            
            # Delete option (available for both text and files)
            st.write("### Delete Data")
            st.warning("This action cannot be undone!")
            
            if st.button("Delete This Data"):
                success, message = delete_data(st.session_state.username, selected_key)
                if success:
                    st.success(message)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(message)
    
    elif menu == "Account Info":
        st.header("👤 Account Information")
        users = load_users()
        user_info = users.get(st.session_state.username, {})
        
        st.write(f"Username: {st.session_state.username}")
        st.write(f"Registered at: {user_info.get('registered_at', 'N/A')}")
        
        # Show user's data statistics
        user_dir = create_user_data_dir(st.session_state.username)
        data_file = f'{user_dir}/data.json'
        
        if os.path.exists(data_file):
            with open(data_file, 'r') as f:
                data = json.load(f)
            st.write(f"Stored items: {len(data)}")
            
            text_count = sum(1 for item in data.values() if item['type'] == 'text')
            file_count = sum(1 for item in data.values() if item['type'] == 'file')
            st.write(f"- Text items: {text_count}")
            st.write(f"- Files: {file_count}")
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()

def handle_failed_attempt():
    st.session_state.retrieve_attempts += 1
    st.error(f"Wrong passkey! Attempts: {st.session_state.retrieve_attempts}/3")
    
    if st.session_state.retrieve_attempts >= 3:
        st.error("Too many failed attempts! Please login again.")
        st.session_state.logged_in = False
        time.sleep(2)
        st.rerun()

def encrypt_text(text, password):
    encrypted = cipher_suite.encrypt(text.encode())
    return encrypted

def decrypt_text(encrypted_text, password):
    try:
        decrypted = cipher_suite.decrypt(encrypted_text.encode())
        return decrypted.decode()
    except:
        return None

# Main app flow
def main():
    st.set_page_config(page_title="Secure Data Vault", page_icon="🔒")
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "login"
    
    if not st.session_state.logged_in:
        if st.session_state.current_page == "login":
            login_page()
            st.write("Don't have an account?")
            if st.button("Go to Registration"):
                st.session_state.current_page = "register"
                st.rerun()
        else:
            registration_page()
            st.write("Already have an account?")
            if st.button("Go to Login"):
                st.session_state.current_page = "login"
                st.rerun()
    else:
        dashboard()

if __name__ == "__main__":
    main()