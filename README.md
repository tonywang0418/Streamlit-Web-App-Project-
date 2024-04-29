# Capstone AI Chatbot Project  
For the Streamlit application and login page 

# Setup
# #Option1 
If you want to run the scripts LOCALLY, you have to activate a virtual environment for Python (Because Python isn’t great at dependency management)
Open your Command prompt or through your vscode command prompt type: 
```
cd C:\Users\<YOUR USERNAME>\AppData\Local\Programs\Python\Python312
```
```
python -m venv venv
```
Once you create the virtual env folder you need to activate it with:
```
venv\Scripts\activate
```
Install following packages:
```
pip install streamlit
```
```
pip install msal
```
# Carefully look at code change these parameters before run the script:
Change Client ID, authority, and port to your application (You should be able to see the port number once you run the script) 
```
import streamlit as st
from msal import PublicClientApplication
import hashlib
#import requests

# Initialize MSAL PublicClientApplication
app = PublicClientApplication(
    "<CLIENT ID>",
    authority="https://login.microsoftonline.com/<tenant ID>",
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
        second_app_url_with_token = f"http://localhost:8501/?access_token={hashed_token}"
        st.write('<iframe src="http://localhost:<port number to your application, should be able to see once you run streamlit>/?access_token=' + hashed_token + '" width="800" height="800"></iframe>', unsafe_allow_html=True)
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
```
SAVE to a folder you are working on

Below change the "URL TO YOUR LOGIN PAGE" (You should be able to see the port number once you run the script) 
```
import streamlit as st
import hashlib
from streamlit.web.server.websocket_headers import _get_websocket_headers
# Retrieve the access token from query parameters
access_token = st.query_params.get("access_token")

if not access_token:
    st.title("Blocked")
    st.write("Access token:", access_token)
    st.error("No access token provided")
    redirect_login_url = "<URL TO YOUR LOGIN PAGE>"
    st.markdown(f'<meta http-equiv="refresh" content="0;URL={redirect_login_url}">', unsafe_allow_html=True)
    st.stop()
else:
    st.title("AI Chatbot Page")
    # Store the access token in session state
    st.session_state.access_token = access_token
    st.write(st.session_state)
```
SAVE to a folder you are working on
# Run the Script 
Type the following in your command prompt or VScode command prompt:
cd to the folder you put them (make sure you are in virtual env before cd)
```
streamlit run login_page.py
```
open another command prompt type:
```
streamlit run AIchatbot_page.py
```
