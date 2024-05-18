import streamlit as st
import hashlib
import pymysql
from login_page import acquire_and_use_token, show_dialog
from AIchatbot_page import main_content
#st.session_state.login_state = None
def main():
    #add_selectbox = st.sidebar.container(border=True)

    st.write(st.session_state)
    
    #if "login_state" not in st.session_state and "access_token" not in st.session_state:
    if 'login_state' not in st.session_state:
        st.session_state.login_state = None
    if 'access_token' not in st.session_state:
        st.session_state.access_token = None
    if 'password_requirement' not in st.session_state:
        st.session_state.password_requirement = None
    if st.session_state.login_state == None and st.session_state.access_token == None:
        st.title("Login Page")
        st.write("Authenticate to access protected content")
        # Below is for Azure Entra ID LOGIN
        add_selectbox = st.sidebar.container(border=True)
        login_button_clicked = add_selectbox.button("Azure Login", type="primary")
        if login_button_clicked:
            st.session_state.access_token = None
            access_token = acquire_and_use_token()
            st.session_state.access_token = access_token
            st.rerun()
        # Below is for username/password LOGIN
        if add_selectbox.button("Username/Password Login"):
            show_dialog()
            if st.session_state.login_state == True:
                st.rerun()
                    
                

    else:
        st.title("AI Chatbot Page")
        main_content()
        #st.write(st.session_state)
        if st.button("Sign out"):
            st.session_state.access_token = None
            st.session_state.login_state = None
            st.session_state.clear()
            st.rerun()


        
        
if __name__ == "__main__":
    main()
