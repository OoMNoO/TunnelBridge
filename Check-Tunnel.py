import os
import subprocess
import socket
import requests
import json
import time
from bs4 import BeautifulSoup

def is_port_in_use(port: int) -> bool:
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
    print(f"checking tunnel status and port availability")
    port_in_use = is_port_in_use(48084)
    if(port_in_use):
        print(f"port is in use, tunnel is available")
    else:
        print(f"port is free, no tunnel is available on it,")
        print(f"reconnecting the tunnel")
        subprocess.Popen("ssh -R 48084:localhost:22 -N -f root@domain.com -i /home/user/.ssh/server", shell=True, env=os.environ)

def tunnel_to_ngrok():
    try:
        req = requests.get('http://127.0.0.1:4040/api/tunnels')
        soup = BeautifulSoup(req.text, 'lxml')
        tunnelsjson = json.loads(soup.find('p').text)
        url = tunnelsjson['tunnels'][0]['public_url']
        print(f"tunnel to ngrok exist on:")
        print(url)
    except Exception as e:
        print("no ngrok connection")
        print(f"recreating tunnel to ngrok")
        subprocess.Popen("ngrok tcp 22 > /dev/null &", shell=True, env=os.environ)
        
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