import streamlit as st
import psutil
import pandas as pd
import time
import socket

# Page Config
st.set_page_config(page_title="Network Monitor", page_icon="📡", layout="wide")

st.title("📡 Real-Time Network Monitor")

def get_total_bytes():
    """Returns total bytes sent and received by the system."""
    io = psutil.net_io_counters()
    return io.bytes_sent, io.bytes_recv

def get_active_connections():
    """
    Scans for active processes with established internet connections.
    Returns a DataFrame of services using the internet.
    """
    connections = []
    try:
        # Get all network connections (requires Admin for full visibility)
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'ESTABLISHED': # Only look at active connections
                try:
                    process = psutil.Process(conn.pid)
                    connections.append({
                        "PID": conn.pid,
                        "Service/App Name": process.name(),
                        "Status": conn.status,
                        "Local Port": conn.laddr.port,
                        "Remote IP": conn.raddr.ip if conn.raddr else "N/A"
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
    except psutil.AccessDenied:
        st.error("⚠️ Permission Denied: Run your terminal as Administrator to see all system services.")
        return pd.DataFrame()

    df = pd.DataFrame(connections)
    if not df.empty:
        # Group by App Name to make the table cleaner
        summary = df.groupby("Service/App Name").size().reset_index(name='Active Connections')
        summary = summary.sort_values(by="Active Connections", ascending=False)
        return summary
    return pd.DataFrame()

# --- Layout ---

# Create placeholders for real-time metrics
col1, col2, col3 = st.columns(3)
with col1:
    upload_metric = st.empty()
with col2:
    download_metric = st.empty()
with col3:
    status_metric = st.empty()

st.markdown("### 🔍 Services Currently Using Internet")
table_placeholder = st.empty()

# --- Main Monitoring Loop ---

# Initialize previous values for speed calculation
prev_sent, prev_recv = get_total_bytes()

while True:
    # Get current total bytes
    curr_sent, curr_recv = get_total_bytes()

    # Calculate Speed (Delta)
    # Since we sleep for 1 second, the difference is exactly bytes/second
    up_speed = (curr_sent - prev_sent) / 1024 / 1024 # Convert to MB
    down_speed = (curr_recv - prev_recv) / 1024 / 1024 # Convert to MB

    # Update Metrics
    upload_metric.metric("Upload Speed", f"{up_speed:.2f} MB/s")
    download_metric.metric("Download Speed", f"{down_speed:.2f} MB/s")
    
    # Get Active Services (Who is connected?)
    df_services = get_active_connections()
    
    if not df_services.empty:
        table_placeholder.dataframe(df_services, use_container_width=True, hide_index=True)
        status_metric.metric("Active Apps", f"{len(df_services)}")
    else:
        table_placeholder.info("No active external connections found (or permission denied).")

    # Update reference values for next loop
    prev_sent, prev_recv = curr_sent, curr_recv

    # Wait before next update
    time.sleep(1)