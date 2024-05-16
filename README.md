# Capstone AI Chatbot Project version 3.0 
For the Streamlit application and login page 

This application utilizes Streamlit as the framework, Azure Entra ID as the Identity provider, and Microsoft Authentication Library (MSAL) to build the authentication flow

3.0 Update info: 
1. Much easier to run the script
    
2. Better logic and better code structure 
    
3. Add Main.py to the repo, and make it much more light weighted.
    
4. Change the way to display the Content

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
Download login_page.py, AIchatbot_page.py and main.py, and make sure to save them into one folder.
# Carefully look at code change these parameters before run the script:
Change Client ID, authority(Tenant ID) 
```
import streamlit as st
from msal import PublicClientApplication
import hashlib
def acquire_and_use_token():
    app = PublicClientApplication(
    "<Client ID>",
    authority="https://login.microsoftonline.com/<Tenant ID>",
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

```
# Run the Script 
Type the following in your command prompt or VScode command prompt:
cd to the folder you put those three scripts (make sure you are in virtual env before cd) Only running main.py should be fine:  
```
streamlit run main.py
```
WARNING: 
There could be a potential bug that could prompt you with an error message like: "Page not found"  the first time you run the script LOCALLY, refreshing the page should resolve the problem.

This BUG is due to unexpected paths in the URL that Streamlit might try to handle but can't find routes for.
