import os
import subprocess
import socket
import requests
import json
import time
from bs4 import BeautifulSoup

def is_port_in_use(port: int) -> bool:
    """Check if a given port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def internet(host="domain.com", port=22, timeout=10):
    """
    Host: ir-server (middle man server)
    OpenPort: 22/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False


def tunnel_to_server():
    """Ensure SSH tunnel to server is active."""
    print("Checking tunnel status and port availability...")
    if is_port_in_use(48084):
        print("Port is in use, tunnel is available.")
    else:
        print("Port is free; reconnecting the tunnel...")
        command = [
            "ssh",
            "-R", "48084:localhost:22",
            "-N", "-f",
            "root@domain.com",
            "-i", "/home/user/.ssh/server"
        ]
        try:
            subprocess.Popen(command, env=os.environ)
            print("Tunnel reconnected to server.")
        except Exception as e:
            print(f"Failed to reconnect tunnel to server: {e}")

def tunnel_to_ngrok():
    """Ensure Ngrok tunnel is active."""
    print("Checking Ngrok tunnel status...")
    try:
        response = requests.get('http://127.0.0.1:4040/api/tunnels', timeout=5)
        response.raise_for_status()
        data = response.json()
        if data['tunnels']:
            url = data['tunnels'][0]['public_url']
            print(f"Ngrok tunnel exists at: {url}")
        else:
            print("No active Ngrok tunnels found.")
            raise ValueError("No tunnels available.")
    except Exception as e:
        print(f"Ngrok connection issue: {e}")
        print("Recreating Ngrok tunnel...")
        try:
            subprocess.Popen(["ngrok", "tcp", "22"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=os.environ)
            print("Ngrok tunnel created.")
        except Exception as e:
            print(f"Failed to create Ngrok tunnel: {e}")
        
def main():
    connection = internet()
    print(f"internet connections: {connection}")
    if(connection):
        tunnel_to_ngrok()
        tunnel_to_server()
    else:
        print(f"reconnecting to net")
        requests.post("http://192.168.1.1/login", data={'username': 'USERNAME', 'password': 'PASSWORD'})
        time.sleep(10)
        tunnel_to_ngrok()
        tunnel_to_server()

if __name__ == "__main__":
    main()