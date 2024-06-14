import os
from openai import OpenAI
import pandas as pd
import json
import streamlit as st

# Network Log Chatbot
# Code Version
version = "0.7.2"


#Function to open different file types
def read_logs(file_path):
    ext = os.path.splitext(file_path)[1]
    if ext == '.csv':
        return pd.read_csv(file_path).to_dict(orient='records')
    elif ext == '.json':
        with open(file_path, 'r') as file:
            return json.load(file)
    elif ext == '.txt':
        with open(file_path, 'r') as file:
            return [{'log': log.strip()} for log in file.readlines()]
    else:
        raise ValueError("Unsupported file type. Please upload a CSV, JSON, or TXT file.")

# Function to load and read logs
def read_network_logs(file):
    try:
        # Read the uploaded file-like object
        if file.type == "text/csv":
            return pd.read_csv(file).to_dict(orient='records')
        elif file.type == "application/json":
            return json.load(file)
        elif file.type == "text/plain":
            return [{'log': log.strip()} for log in file.readlines()]
        else:
            raise ValueError("Unsupported file type. Please upload a CSV, JSON, or TXT file.")
    except ValueError as e:
        st.error(str(e))
        return []

# Function to generate a response from the OpenAI API
def generate_response(api_key, prompt, logs, chat_history):
    client = OpenAI(api_key=api_key)
   
    # Reduce the context size by using only the last N logs
    N = 50  # Adjust this number based on your token limits
    recent_logs = logs[-N:]

    # Combine the logs into a single string for context
    logs_context = "\n".join([str(log) for log in recent_logs])

    # Create the messages for the chat history
    messages = [
        {"role": "system", "content": "You are a helpful assistant that answers questions based on network logs."},
        {"role": "system", "content": f"Network Logs:\n{logs_context}"}
    ]

    # Add the chat history to the messages
    messages.extend(chat_history)

    # Add the current user prompt to the messages
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150
    )

    return response.choices[0].message.content

# Function to display a user message
def display_user_message(message):
    user_avatar = os.path.join('icons', 'user_avatar.png')
    st.sidebar.image(user_avatar, width=50)
    st.sidebar.markdown(f"<div style='display: inline-block; background-color: #f1f1f1; padding: 10px; border-radius: 10px;'>{message}</div>", unsafe_allow_html=True)

# Function to display an assistant message
def display_assistant_message(message):
    bot_avatar = os.path.join('icons', 'bot_avatar.png')
    st.sidebar.image(bot_avatar, width=50)
    st.sidebar.markdown(f"<div style='display: inline-block; background-color: #d1e7dd; padding: 10px; border-radius: 10px;'>{message}</div>", unsafe_allow_html=True)

# Function to handle new user input
def handle_user_input():
    user_input = st.session_state.user_input
    if user_input:
        try:
            # Generate the response
            response = generate_response(st.session_state.openai_api_key, user_input, st.session_state.logs, st.session_state.chat_history)

            # Update chat history with the new user input and model response
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "assistant", "content": response})

            # Store the latest response separately
            st.session_state.latest_response = response

            # Clear the input box
            st.session_state.user_input = ""

        except Exception as e:
            st.error(f"Error: {e}")

# Streamlit application
def main():
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: flex-end;">
            <div style="font-size: 2em; font-weight: bold;">Network Logs Chatbot</div>
            <div style="font-size: 1em; text-align: right; color: gray; flex-grow: 1; text-align: right;">{Version}</div>
        </div>
        <hr>
    """, unsafe_allow_html=True)

    # Initialize session state variables
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'latest_response' not in st.session_state:
        st.session_state.latest_response = ""
    if 'logs' not in st.session_state:
        st.session_state.logs = []

    # Sidebar input for OpenAI API key
    st.session_state.openai_api_key = st.sidebar.text_input('Input your OpenAI API Key', value="", type='password')

    if st.session_state.openai_api_key:
        # Upload log file
        uploaded_file = st.file_uploader("Upload your network logs (CSV, JSON, TXT)", type=["csv", "json", "txt"])

        if uploaded_file is not None:
            # Read and parse network logs
            st.session_state.logs = read_network_logs(uploaded_file)
            st.success("Network logs loaded successfully!")

            # User input for questions
            st.text_input("Ask a question about the network logs:", key="user_input", on_change=handle_user_input)

            # Display the latest response under the input field
            if 'latest_response' in st.session_state:
                st.markdown("### Latest Response")
                st.markdown(st.session_state.latest_response)

            # Display the chat history in the sidebar
            st.sidebar.title("Chat History")
            for msg in st.session_state.chat_history:
                if msg['role'] == 'user':
                    display_user_message(msg['content'])
                else:
                    display_assistant_message(msg['content'])

    else:
        st.warning("Please enter your OpenAI API key in the sidebar to proceed.")

if __name__ == "__main__":
    main()
