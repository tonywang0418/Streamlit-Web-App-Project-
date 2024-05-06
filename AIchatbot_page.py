import streamlit as st
import hashlib
from st_pages import Page, show_pages, hide_pages
redirect_login_url = "<Login Page URL with port number>/login%20page"
st.title("AI Chatbot Page")
st.write(st.session_state)

if not st.session_state:
    st.write("BLOCKED")
    st.markdown(f'<meta http-equiv="refresh" content="0;URL={redirect_login_url}">', unsafe_allow_html=True)
    st.stop()
else:
    show_pages([Page("AIchatbot_page.py", "AIchatbot page"), Page("login_page.py", "login page")])
    hide_pages(["login page"])
    if st.button("Sign out"):
        st.session_state.token = None
        st.markdown(f'<meta http-equiv="refresh" content="0;URL={redirect_login_url}">', unsafe_allow_html=True)

    
    
