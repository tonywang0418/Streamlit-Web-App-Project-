# Capstone AI LOG Chatbot Project version 5.0 
For the Streamlit application and login page 

This application utilizes Streamlit as the Frontend framework, Flask for the Backend framework, Azure Entra ID as the Identity provider, and Microsoft Authentication Library (MSAL) to build the authentication flow

5.0 Update info: 
1. Much easier to run the script
    
2. Better logic and better code structure 
    
3. Redesign the entire project structure as Frontend(streamlit) and Backend(flask). Much more flexibility and is easier to manage
4. Before: everything was built solely by Streamlit, including authentication, token generation, database connection, HTTP request handling, and more. It was very difficult to manage HTTP traffic and improve security. In this version, I added Flask to manage all the backend stuff(HTTP requests, app routing, web logic, security) You can now control which route to handle specific requests (GET, POST..). For streamlit, it runs as a frontend, only responsible for UI, User interaction, and interaction with the backend.     
       
5. ADD new feature: Flask framework.  Gives you the flexibility to customize your own HTTP request, security, and more!
# Project structure
```
project-directory/
│
├── frontend/
│   ├── main.py
│   ├── login_page.py
│   ├── AIchatbot_page.py
│
├── backend/
│   ├── app.py
```
# Structure description: 
Frontend: I use Streamlit which focuses purely on rendering the UI, receiving user input, and making requests to the backend.
Backend: I use Flask to handle backend tasks like authentication, database operations, security, HTTP request processing, etc.
Provide much more flexibility to programmers. For anything beyond a simple data app, separating the frontend (Streamlit) and backend (Flask) is a best practice that provides robustness and scalability.
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
