import streamlit as st
from login_page import acquire_and_use_token
from AIchatbot_page import main_content


def main():
    add_selectbox = st.sidebar.container(border=True)
    login_button_clicked = add_selectbox.button("Azure Login", type="primary")
    
    
    
    if "access_token" not in st.session_state or st.session_state.access_token == None:
        
        st.title("Azure Entra ID Login Page")
        st.write("Authenticate to access protected content")

    else:
        st.title("AI Chatbot Page")
        main_content()
        st.write(st.session_state)
        if st.button("Sign out"):
            st.session_state.access_token = None
            st.session_state.clear()
            st.rerun()

    if login_button_clicked:
        st.session_state.access_token = None
        access_token = acquire_and_use_token()
        st.session_state.access_token = access_token
        st.rerun()
        
        
if __name__ == "__main__":
    main()