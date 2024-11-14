# Logs Analysis and Visualisation Tool

This Python project provides an easy-to-use GUI for selecting log files, parsing their contents, and analyzing log events. The tool offers multiple visualization options to help track and analyze log activity over time.

## Features

- **File Selection**: Choose a log file via a graphical file selection window.
- **Log Parsing**: Extracts timestamps, sources, and message details from the log entries.
- **Data Filtering**: Filters log messages based on keywords like "Error" or "Critical" for targeted analysis.
- **Visualisations**:
  - **Line Chart**: Displays the number of events per hour over time.
  - **Pie Chart**: Shows the distribution of event sources.

## Requirements

- Python 3.8 or higher
- Required Libraries:
  - `pandas` for data handling and filtering
  - `matplotlib` and `plotly` for visualizations
  - `tkinter` for file dialog GUI

Install the necessary packages with the following command:
```bash
pip install pandas matplotlib plotly

## Attachments 
- Log sample is attached to this reprository to test this code: "sample.log"
