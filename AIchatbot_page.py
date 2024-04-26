import streamlit as st
import hashlib
from streamlit.web.server.websocket_headers import _get_websocket_headers
# Retrieve the access token from query parameters
access_token = st.query_params.get("access_token")

if not access_token:
    st.title("Blocked")
    st.write("Access token:", access_token)
    st.error("No access token provided")
    redirect_login_url = "http://localhost:8503"
    st.markdown(f'<meta http-equiv="refresh" content="0;URL={redirect_login_url}">', unsafe_allow_html=True)
    st.stop()
else:
    st.title("AI Chatbot Page")
    # Store the access token in session state
    st.session_state.access_token = access_token
    st.write(st.session_state)

    
    
