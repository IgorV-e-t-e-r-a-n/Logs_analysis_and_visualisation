import pandas as pd  # filters data
import plotly.express as px
import plotly.graph_objects as go
import tkinter as tk
from tkinter import filedialog #for GUI option when choosing log file for parsing
from sklearn.cluster import KMeans
import re

# Function to choose a file path
def choose_file_path():
    try:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Select a File")
        if not file_path:
            raise ValueError("Log file was not chosen or does not exist")
    except ValueError as e:  
        print(e)
        file_path = None
    return file_path

# Function to parse logs from file
def parse_logs(file_path):
    log_pattern = re.compile(
        r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) '  # Timestamp
        r'(?P<source>\S+) '                                    # Source (non-whitespace string)
        r'(?P<message>.+)'                                     # Message (remaining line)
    )
                
                
    logs = []
    with open(file_path, 'r') as file:           
        for line in file:     
            match = log_pattern.match(line)
            if match:
                log_entry = match.groupdict()
                logs.append(log_entry)
                
    df = pd.DataFrame(logs)
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    return df


# Event correlation function
def correlate_events(df):
    df['is_login'] = df['message'].str.contains("logged in")
    df['is_failed_login'] = df['message'].str.contains("Failed login attempt") 
    
    # Grouping login events and calculating cumulative sum to identify related events
    df['login_event_group'] = (df['is_login'] | df['is_failed_login']).cumsum()
    correlation_results = df.groupby('login_event_group').filter(lambda x: len(x) > 1)
    
    return correlation_results

# Anomaly detection using KMeans clustering
def detect_anomalies(df):
    df['event_hour'] = df.index.hour  # Extracting hour of event from the timestamp
    df['event_day'] = df.index.day  # Extracting day of event from the timestamp
    
    # Using KMeans clustering to detect anomalies based on event time (hour and day)
    kmeans = KMeans(n_clusters=2)  # assumed 2 clusters, one for normal, one for anomalous, may be customised if needed
    df['cluster'] = kmeans.fit_predict(df[['event_hour', 'event_day']])
    
    # The majority cluster is assumed to represent normal behavior
    anomaly_cluster = df['cluster'].mode()[0]
    # While anomalous clusters are considered as minority
    anomalies = df[df['cluster'] != anomaly_cluster]
    
    return anomalies

# Visualisation of logs over timea
def plot_log_analysis(df):
    time_series = df.resample("h").size()

    # Plotly line chart for log events over time
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=time_series.index, y=time_series, mode='lines', name='Events per Hour'))
    fig_line.update_layout(title="Log Events Over Time", xaxis_title="Time", yaxis_title="Number of Events")
    
    # Plotly pie chart for event sources
    source_counts = df['source'].value_counts()
    fig_pie = px.pie(values=source_counts, names=source_counts.index, title="Event Sources")
    
    # Display both figures (in browser)
    fig_line.show()
    fig_pie.show()

# Main function to drive the process
def main():
    file_path = choose_file_path()  # Choose the file path
    if not file_path:
        return  # If no file path was chosen stop the program
    
    log_df = parse_logs(file_path)  # Parse the logs from the chosen file
    if log_df.empty:
        print("No logs to display.")
        return  # If no logs are found stop the program
    
    # Analysis and visualisation
    log_df['timestamp'] = pd.to_datetime(log_df['timestamp'])  # Convert timestamp to datetime
    log_df.set_index('timestamp', inplace=True)  # Set timestamp as index
    
    # Filter, correlate, and detect anomalies
    filtered_logs = log_df[log_df["message"].str.contains("Error|Critical")]
    correlated_events = correlate_events(log_df)
    anomalies = detect_anomalies(log_df)
    
    # Output results (in terminal)
    print("Filtered Logs:", filtered_logs)
    print("Correlated Events:", correlated_events)
    print("Detected Anomalies:", anomalies)
    
    # Visualize the data
    plot_log_analysis(log_df)

# Run the main function
if __name__ == "__main__":
    main()
