import streamlit as st
from msal import PublicClientApplication
import hashlib
import pymysql
import re

def acquire_and_use_token():
    app = PublicClientApplication("35af6748-20e6-4470-9bad-08154a34db69", authority="https://login.microsoftonline.com/cfb43c26-9c6c-4fc7-b47d-c433bb597d82")
    #global result
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(["User.Read"], account=accounts[0])
    else:
        result = app.acquire_token_interactive(scopes=["User.Read"], prompt="select_account")


    if "access_token" in result:
        
        st.write("Protected content available")
        return result["access_token"]
    
    else:
        st.error("Token acquisition failed")
        st.error(result.get("error_description", "No further details"))

@st.experimental_dialog("Username & Password LOGIN")
def show_dialog():
    choice = st.selectbox('Login/Signup',['Login','Sign up'])
    if choice == 'Login':
        username = st.text_input("Username:")
        password = st.text_input("Password:", type='password')
        
        hash_pass = hash_password(password)
        try:
            if st.button("Login"):
                
                mycursor, mydb = database_connection()
                hash_query = "SELECT * FROM user_info WHERE username = %s AND password = %s"
                mycursor.execute(hash_query, (username, hash_pass))
                user = mycursor.fetchone()
                if "login_state" not in st.session_state:
                    st.session_state.login_state = None
                mydb.close()
                if user:
                    st.title('successfully logged in')
                    st.session_state.login_state = True
                    st.rerun()
                else:
                    st.error('Bad username or password')
                    return False
            
        except pymysql.Error as error:
                st.write("Error:", error)
                return False
    #sign up
    else:
        signup_email = st.text_input("Enter your unique username")
        signup_password = st.text_input("Password:", type='password')
        if st.button("Sign Up"):
            if not signup_email.strip():
                st.error("Username cannot be empty. Please enter a valid username.")
            #st.session_state.password_requirement = None
            else:
                valid_pass = is_valid_password(signup_password)
                if st.session_state.password_requirement != None and st.session_state.password_requirement != False:
                    try:
                        mycursor, mydb = database_connection()
                        hash = hash_password(signup_password)

                        query =  "INSERT INTO `user_info` (`username`, `password`) VALUES (%s,%s)"
                        mycursor.execute(query,(signup_email, hash))
                        mydb.commit()
                        mydb.close()
                        if st.session_state.password_requirement == True:
                            st.title('successfully sign up! You may log in now')
                    except pymysql.IntegrityError as error:
                        st.error("Username has been taken, Please change another one.")
                    #except Exception as e:
                        #st.error("An error occurred during sign up. Please try again later.")
                #else:
                    #st.error("bad")

    if st.button("Close"):
        st.rerun()

def database_connection():
    mydb = pymysql.connect(host='10.0.0.116', user='capstone', password='Zx2012abcd', database='capstone') 
    mycursor = mydb.cursor() 
    return mycursor, mydb

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






    

