import streamlit as st
from msal import PublicClientApplication
import hashlib
import pymysql
import re
import requests

def database_connection():
    mydb = pymysql.connect(host='10.0.0.117', user='tony', password='password',database='user_info')
    mycursor = mydb.cursor()
    return mycursor, mydb

def acquire_and_use_token():
    client_id = "<client ID>"
    authority = "https://login.microsoftonline.com/<tanent ID>"
    scopes = ["https://graph.microsoft.com/.default"]
    app = PublicClientApplication(
        client_id,
        authority=authority
    )
    flow = app.initiate_device_flow(scopes=scopes)
    st.write(flow['message'])
    result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:

        st.write("Protected content available")
        return result["access_token"]

    else:
        st.error("Token acquisition failed")
        st.error(result.get("error_description", "No further details"))


@st.dialog("Username & Password LOGIN")
def show_dialog():
    choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
    if choice == 'Login':
        username = st.text_input("Username:")
        password = st.text_input("Password:", type='password')

        hash_pass = hash_password(password)
        if st.button("Login"):
            try:
                response = requests.post("http://127.0.0.1:5000/login", json={'username': username, 'password': hash_pass})
                if response.status_code == 200:
                    st.session_state.login_state = True
                    st.session_state.JWT_token = response.json().get("token")
                    st.title('successfully logged in')
                    st.rerun()
                else:
                    st.error('Bad username or password')
                    return False
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")
    # sign up
    elif choice == 'Sign up':
        signup_email = st.text_input("Enter your unique username")
        signup_password = st.text_input("Password:", type='password')
        if st.button("Sign Up"):
            if not signup_email.strip():
                st.error("Username cannot be empty. Please enter a valid username.")
            if is_valid_password(signup_password):
                if st.session_state.password_requirement is not None and st.session_state.password_requirement != False:
                    hashed_password = hash_password(signup_password)
                    try:
                        response = requests.post("http://127.0.0.1:5000/signup", json={'username': signup_email, 'password': hashed_password})
                        if response.status_code == 201:
                            st.success("Successfully signed up! You may now log in.")
                        elif response.status_code == 409:
                            st.error("Username already exists. Please choose another one.")
                        else:
                            st.error("An error occurred during sign up. Please try again later.")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error connecting to backend: {e}")

    if st.button("Close"):
        st.rerun()

def hash_password(password):
    # Encode the password as UTF-8 before hashing
    password_utf8 = password.encode('utf-8')
    hashed_password = hashlib.md5(password_utf8)
    return hashed_password.hexdigest()

def is_valid_password(password):
    # Define password requirements
    min_length = 8
    special_chars = r"[!@#$%^&*()_+=\[{\]};:<>|./?,-]"
    # Check minimum length
    if len(password) < min_length:
        st.session_state.password_requirement = False
        st.error("Password must be at least 8 characters long")
        return False

        # Check if it contains at least one digit
    if not any(char.isdigit() for char in password):
        st.session_state.password_requirement = False
        st.error("Password must contain at least one digit")
        return False
    # Check if it contains at least one letter
    if not any(char.isalpha() for char in password):
        st.session_state.password_requirement = False
        st.error("Password must contain at least one letter")
        return False
        # Check if it contains at least one special character
    if not re.search(special_chars, password):
        st.session_state.password_requirement = False
        st.error("Password must contain at least one special character")
        return False
    else:
        st.session_state.password_requirement = True
        return True





    

