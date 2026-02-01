# Network Monitor Web App

A real-time internet usage monitor built with Python and Streamlit. This application allows Windows users to track their upload/download speeds and view a list of active services connecting to the internet.

## Features

* **Real-Time Speed Tracking:** Displays current Upload and Download speeds in MB/s.
* **Active Service Monitoring:** Lists all applications (services) currently holding an active connection.
* **Live Dashboard:** Updates metrics every second automatically.
* **Simple UI:** Clean interface built with Streamlit.

## Technologies Used

* **Python:** Core programming language.
* **Streamlit:** For the web interface.
* **Psutil:** For retrieving system network statistics.
* **Pandas:** For data formatting and display.

## Installation

1.  Clone this repository or download the source code.
2.  Open your terminal or command prompt.
3.  Install the required dependencies using pip:

```
pip install streamlit psutil pandas
```

## How to Run
To get accurate data about system services, this application works best when run with Administrator privileges.

Open Command Prompt or PowerShell as Administrator.

Navigate to the project folder.

Run the application:

```
streamlit run monitor.py
```
The app will open in your default web browser at http://localhost:8501.

## Important Note
Administrator Rights: Windows restricts access to network details for security reasons. If you do not run the terminal as Administrator, the "Active Services" table may be empty or incomplete.

Data Accuracy: The speed shown is the total system bandwidth usage. Due to Windows OS limitations, getting exact bandwidth usage per specific app (e.g., "Chrome is using 5MB/s") requires specialized drivers not available in standard Python libraries.

## License
This project is open-source and available for personal and educational use.
