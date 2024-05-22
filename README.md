# Capstone AI Chatbot Project version 3.0 
For the Streamlit application and login page 

This application utilizes Streamlit as the framework, Azure Entra ID as the Identity provider, and Microsoft Authentication Library (MSAL) to build the authentication flow

4.0 Update info: 
1. Much easier to run the script
    
2. Better logic and better code structure 
    
3. Add Main.py to the repo, and make it much more light weighted.
    
4. ADD new feature: Useranme and password login method, which does not rely on any third party idenity provider, but you need to create a sql database and change the connection info inside login_page.py

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
# Once finish download, change Client ID, authority(Tenant ID) from login_page.py before running the script
optional:  if you need Username/password login to work, you need to create a SQL database and change the connection info inside login_page.py
# Run the Script 
Type the following in your command prompt or VScode command prompt:
cd to the folder you put those three scripts (make sure you are in virtual env before cd) Only running main.py should be fine:  
```
streamlit run main.py
```
WARNING: 
There could be a potential bug that could prompt you with an error message like: "Page not found"  the first time you run the script LOCALLY, refreshing the page should resolve the problem.

This BUG is due to unexpected paths in the URL that Streamlit might try to handle but can't find routes for.
