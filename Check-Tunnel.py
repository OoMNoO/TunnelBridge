import os
import subprocess
import socket
import requests
import json
import time
import logging
from datetime import datetime
from bs4 import BeautifulSoup

# Setup logging
def setup_logger():
    """Configure daily rotating logs."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

# Check if a port is in use
def is_port_in_use(port: int) -> bool:
    """Check if a given port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

# Check internet connectivity
def internet(host="domain.com", port=22, timeout=10):
    """Check connectivity to a remote host and port."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        logging.error(f"Internet connectivity issue: {ex}")
        return False

# Ensure SSH tunnel is active
def tunnel_to_server():
    """Ensure SSH tunnel to server is active."""
    logging.info("Checking tunnel status and port availability...")
    if is_port_in_use(48084):
        logging.info("Port is in use, tunnel is available.")
    else:
        logging.info("Port is free; reconnecting the tunnel...")
        command = [
            "ssh",
            "-R", "48084:localhost:22",
            "-N", "-f",
            "root@domain.com",
            "-i", "/home/user/.ssh/server"
        ]
        try:
            subprocess.Popen(command, env=os.environ)
            logging.info("Tunnel reconnected to server.")
        except Exception as e:
            logging.error(f"Failed to reconnect tunnel to server: {e}")

# Ensure Ngrok tunnel is active
def tunnel_to_ngrok():
    """Ensure Ngrok tunnel is active."""
    logging.info("Checking Ngrok tunnel status...")
    try:
        response = requests.get('http://127.0.0.1:4040/api/tunnels', timeout=5)
        response.raise_for_status()
        data = response.json()
        if data['tunnels']:
            url = data['tunnels'][0]['public_url']
            logging.info(f"Ngrok tunnel exists at: {url}")
        else:
            logging.warning("No active Ngrok tunnels found.")
            raise ValueError("No tunnels available.")
    except Exception as e:
        logging.error(f"Ngrok connection issue: {e}")
        logging.info("Recreating Ngrok tunnel...")
        try:
            subprocess.Popen(
                ["ngrok", "tcp", "22"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=os.environ
            )
            logging.info("Ngrok tunnel created.")
        except Exception as e:
            logging.error(f"Failed to create Ngrok tunnel: {e}")

# Main function
def main():
    setup_logger()
    logging.info("Script started.")
    connection = internet()
    logging.info(f"Internet connection status: {connection}")
    if connection:
        tunnel_to_ngrok()
        tunnel_to_server()
    else:
        logging.warning("Internet connection lost. Attempting to reconnect...")
        try:
            requests.post("http://192.168.1.1/login", data={'username': 'USERNAME', 'password': 'PASSWORD'})
            logging.info("Reconnected to the network. Waiting before retrying tunnels...")
            time.sleep(10)
            tunnel_to_ngrok()
            tunnel_to_server()
        except Exception as e:
            logging.error(f"Failed to reconnect to the network: {e}")

if __name__ == "__main__":
    main()
