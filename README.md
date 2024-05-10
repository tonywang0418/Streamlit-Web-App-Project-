# Capstone AI Chatbot Project  
For the Streamlit application and login page 

This application utilizes Streamlit as the framework, Azure Entra ID as the Identity provider, and Microsoft Authentication Library (MSAL) to build the authentication flow    

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
Download requirements.txt to Install following packages:
```
pip install -r requirements.txt
```
# Carefully look at code change these parameters before run the script:
Change Client ID, authority(Tenant ID) 
```
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

```
SAVE to a folder you are working on

Below change the "redirect_login_url" (You should be able to see the port number once you run that script)

Development team, You may write your code below "# Write the actual content below: " This will integrate the authentication feature to your content, hopefully :)
```
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

# Write the actual content below:
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
