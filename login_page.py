import streamlit as st
from msal import PublicClientApplication
import hashlib
def acquire_and_use_token():
    app = PublicClientApplication(
    "25673ac4-5f19-4fc2-b01f-5c46b0a0ab3f",
    authority="https://login.microsoftonline.com/f139cf46-660d-47d6-9df6-4a1ef9fb600f",
    client_credential=None
    )
    global result
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(["User.Read"], account=accounts[0])
    else:
        result = app.acquire_token_interactive(scopes=["User.Read"], prompt="select_account")
    #if not result["access_token"]:
        #st.write("Authenticate to access protected content")
    # Check if token was obtained successfully
    if "access_token" in result:
        #st.write(result)
        #st.session_state.token = result["access_token"]
        st.write("Protected content available")
        return result["access_token"]
    else:
        st.error("Token acquisition failed")
        st.error(result.get("error_description", "No further details"))

def logout():
    logged_accounts = app.get_accounts()
    if logged_accounts:
        for account in logged_accounts:
            app.remove_account(account)
            st.session_state.token = None






    

