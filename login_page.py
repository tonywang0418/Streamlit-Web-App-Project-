import streamlit as st
from msal import PublicClientApplication
import hashlib
#import requests
LOCAL_URL_for_Content = "<LOCAL URL FOR YOUR APP CONTENT>"
# Initialize MSAL PublicClientApplication
app = PublicClientApplication(
    "<CLIENT ID>",
    authority="https://login.microsoftonline.com/<Tenant ID>",
    client_credential=None
    )
result = None
# Function to acquire and use token
def acquire_and_use_token():
    #result = None

    # Attempt to get token from cache or acquire interactively
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(["User.Read"], account=accounts[0])
    else:
        result = app.acquire_token_interactive(scopes=["User.Read"], prompt="select_account")
    if not result["access_token"]:
        st.write("Authenticate to access protected content")
    # Check if token was obtained successfully
    if "access_token" in result:
        st.session_state.token = result["access_token"]
        st.write("Protected content available")
        hashed_token = hashlib.sha256(st.session_state.token.encode()).hexdigest()
        second_app_url_with_token = f"{LOCAL_URL_for_Content}/?access_token={hashed_token}"
        st.write(f'<iframe src="{second_app_url_with_token}" width="800" height="800"></iframe>', unsafe_allow_html=True)
    else:
        st.error("Token acquisition failed")
        st.error(result.get("error_description", "No further details"))
    
def logout():
    logged_accounts = app.get_accounts()
    if logged_accounts:
        for account in logged_accounts:
            app.remove_account(account)
        st.session_state.token = None
            
    
# Streamlit app UI
st.title("Azure Entra ID Login Page")

# Create a placeholder for token
if "token" not in st.session_state:
    st.session_state.token = None

add_selectbox = st.sidebar.container(border=True)
if add_selectbox.button("login", type= "primary"):
    acquire_and_use_token()
    # Update session state with token

if add_selectbox.button("Sign out"):
    st.session_state.token = None
    logout()

if not result:
    st.write("Authenticate to access protected content")

st.write(st.session_state)


    

