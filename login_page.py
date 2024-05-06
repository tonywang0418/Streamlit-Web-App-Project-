import streamlit as st
from msal import PublicClientApplication
import hashlib
from st_pages import Page, show_pages, hide_pages
# Initialize MSAL PublicClientApplication
app = PublicClientApplication(
    "<Client ID>",
    authority="https://login.microsoftonline.com/<Tenant ID>",
    client_credential=None
    )

# Function to acquire and use token
def acquire_and_use_token():
    global result
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(["User.Read"], account=accounts[0])
    else:
        result = app.acquire_token_interactive(scopes=["User.Read"], prompt="select_account")
    if not result["access_token"]:
        st.write("Authenticate to access protected content")
    # Check if token was obtained successfully
    if "access_token" in result:
        st.write(result)
        st.session_state.token = result["access_token"]
        st.write("Protected content available")
        st.rerun()
    else:
        st.error("Token acquisition failed")
        st.error(result.get("error_description", "No further details"))

def logout():
    logged_accounts = app.get_accounts()
    if logged_accounts:
        for account in logged_accounts:
            app.remove_account(account)
        st.session_state.token = None


# Create a placeholder for token
if "token" not in st.session_state:
    st.session_state.token = None
    
add_selectbox = st.sidebar.container(border=True)
if not st.session_state.token:
    login_button_clicked = add_selectbox.button("Login", type="primary")
    if login_button_clicked:
        acquire_and_use_token()
        
        
if add_selectbox.button("Sign out"):
    st.session_state.token = None
    logout()
    st.rerun()
if not st.session_state.token:
    st.title("Azure Entra ID Login Page")
    st.write("Authenticate to access protected content")
    show_pages([Page("AIchatbot_page.py", "AIchatbot page"), Page("login_page.py", "login page")])
    hide_pages(["AIchatbot page"])
else:
    st.title("Welcome! AI Chatbot ")
    

st.write(st.session_state)


    

