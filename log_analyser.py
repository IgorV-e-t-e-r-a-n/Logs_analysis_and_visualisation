import pandas as pd  # filters data
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import tkinter as tk
from tkinter import filedialog

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

file_path = choose_file_path()

# Function to parse logs from file
def parse_logs(file_path):
    logs = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(" ")
            log_entry ={ 
                "timestamp": parts[0] + " " + parts[1],
                "source": parts[2],
                "message": " ".join(parts[3:])
            }
            logs.append(log_entry)
    return pd.DataFrame(logs)

log_df = parse_logs(file_path)
log_df['timestamp'] = pd.to_datetime(log_df['timestamp'])

# Check for empty DataFrame before proceeding
if log_df == None:
    print("No logs to display.")
else:
    # Filtering logs by specific message types
    filtered_logs = log_df["message"].str.contains("Error|Critical")
    print(f"Filtered logs:", filtered_logs)

    # Grouping logs by hour for time analysis
    log_df.set_index('timestamp', inplace=True)
    time_series = log_df.resample("H").size()

    # Plotly line chart for log events over time
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=time_series.index, y=time_series, mode='lines', name='Events per Hour'))
    fig_line.update_layout(title="Log Events Over Time", xaxis_title="Time", yaxis_title="Number of Events")
    
    # Plotly pie chart for event sources
    source_counts = log_df['source'].value_counts()
    fig_pie = px.pie(values=source_counts, names=source_counts.index, title="Event Sources")
    
    # Display both figures in plotly, i.e. in browser
    fig_line.show()
    fig_pie.show()
