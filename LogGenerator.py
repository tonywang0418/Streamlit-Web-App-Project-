import streamlit as st
import pandas as pd
import win32evtlog

# Network Log Generator
# Code Version
version = "1.0"

# Function to read event logs
def read_event_logs(log_type, num_logs):
    server = 'localhost'
    log = log_type
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    hand = win32evtlog.OpenEventLog(server, log)
    logs = []
    total = 0

    while True:
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        if events:
            for event in events:
                if total >= num_logs:
                    break
                logs.append({
                    'EventID': event.EventID,
                    'SourceName': event.SourceName,
                    'TimeGenerated': event.TimeGenerated,
                    'EventCategory': event.EventCategory,
                    'EventType': event.EventType,
                    'EventData': event.StringInserts
                })
                total += 1
        else:
            break

    win32evtlog.CloseEventLog(hand)
    return logs

# Function to convert logs to DataFrame
def logs_to_df(logs):
    df = pd.DataFrame(logs)
    return df

# Function to get color for event category
def get_event_category_color(category):
    if category == 1:
        return 'red'
    elif category == 2:
        return 'yellow'
    else:
        return 'green'

# Function to apply color coding to DataFrame
def color_event_category(val):
    color = get_event_category_color(val)
    return f'background-color: {color}'

# Streamlit app
st.title("Netchatbot Log Generator")

# Custom warning message and user consent
st.markdown(
    """
    <div style="background-color: red; padding: 10px; border-radius: 5px;">
        <h3 style="color: white;">This application collects data from your local host.</h3>
    </div>
    """,
    unsafe_allow_html=True
)

consent = st.radio("Do you agree to proceed?", ("I'm thinking", "Yes", "No"))

if consent == "Yes":
    log_type = st.selectbox("Select Log Type", ("Application", "System", "Security"))
    
    if log_type == "Security":
        st.error("Sorry, the Security logs function doesn't actually work right now. Please use another function.")
    else:
        num_logs = st.slider("Number of Logs to Display", min_value=5, max_value=50, value=10)
        
        if st.button("Generate Report"):
            logs = read_event_logs(log_type, num_logs)
            df = logs_to_df(logs)
            
            # Apply color coding to EventCategory
            styled_df = df.style.applymap(color_event_category, subset=['EventCategory'])

            # Display DataFrame with color-coded EventCategory
            st.dataframe(styled_df)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{log_type}_logs.csv",
                mime='text/csv',
            )
elif consent == "No":
    st.error("Okay please leave the application.")
