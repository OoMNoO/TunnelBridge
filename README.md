# Tunneling Script with Daily Logging

This script ensures reliable SSH and Ngrok tunneling while maintaining logs of its operations. It is designed to manage connectivity, detect port availability, and re-establish tunnels when necessary. Logs are rotated daily for easier tracking and debugging.

## Features

- **SSH Tunnel Management**:

  - Checks the status of an SSH tunnel and reconnects it if necessary.
  - Uses port 48084 for the tunnel to the remote server.

- **Ngrok Tunnel Management**:

  - Verifies if an active Ngrok tunnel exists.
  - Automatically recreates the tunnel if not available.

- **Network Connectivity Check**:

  - Ensures the script runs only when there is an active internet connection.
  - Attempts to reconnect to the network using a predefined login if the connection is lost.

- **Daily Rotating Logs**:
  - Logs all script operations in a `logs` directory.
  - Creates a new log file every day with the format `YYYY-MM-DD.log`.
  - Log entries include timestamps and categorized levels (`INFO`, `WARNING`, `ERROR`).

## Prerequisites

1. **Python Libraries**:

   - `requests`
   - `BeautifulSoup` (`bs4`)

   Install them using:

   ```bash
   pip install requests beautifulsoup4
   ```

2. **Ngrok**:

   - Ensure Ngrok is installed and accessible in the system's PATH.

3. **SSH Configuration**:

   - Add your SSH private key (/home/user/.ssh/server) and ensure the target server (domain.com) is configured for key-based authentication.

4. **Network Login**:

   - Update the login credentials (USERNAME, PASSWORD) and endpoint (http://192.168.1.1/login) in the script for your network.

## How It Works

1. **Port Availability**:

   - Checks if port `48084` is in use to determine if the SSH tunnel is active.

2. **Internet Connectivity**:

   - Pings the remote server (`domain.com`) on port 22 to confirm internet access.

3. **Tunnel Management**:

   - If the SSH tunnel is not active, it reconnects.
   - Verifies the existence of an Ngrok tunnel and recreates it if necessary.

4. **Logging**:
   - Logs all activities, errors, and statuses into daily log files stored in a `logs` directory.

## Usage

1. Clone the repository:

```bash
git clone <repository_url>
cd <repository_directory>
```

2. Run the script:

```bash
python3 Check-Tunnel.py
```

3. Check logs:

- Logs are stored in the `logs` directory with filenames like `2024-12-07.log`.

## Configuration

- **SSH Tunnel**:

  - Update the SSH command to match your server and key configuration:
    ```python
    command = [
        "ssh",
        "-R", "48084:localhost:22",
        "-N", "-f",
        "root@domain.com",
        "-i", "/path/to/your/ssh/key"
    ]
    ```

- **Ngrok Port**:

  - Ensure the Ngrok command matches the desired service and port:
    ```python
    subprocess.Popen(["ngrok", "tcp", "22"], ...)
    ```

- **Network Login**:
  - Replace the placeholder login URL and credentials:
    ```python
    requests.post("http://192.168.1.1/login", data={'username': 'USERNAME', 'password': 'PASSWORD'})
    ```

## Example Log Output

```output
2024-12-07 10:00:00 - INFO - Script started.
2024-12-07 10:00:01 - INFO - Internet connection status: True
2024-12-07 10:00:01 - INFO - Checking Ngrok tunnel status...
2024-12-07 10:00:02 - INFO - Ngrok tunnel exists at: https://1234.ngrok.io
2024-12-07 10:00:02 - INFO - Checking tunnel status and port availability...
2024-12-07 10:00:02 - INFO - Port is in use, tunnel is available.
```

## Notes

- Ensure Ngrok and SSH are properly configured on your system before running this script.
- Logs are stored in the `logs` directory relative to the script's location.

## Troubleshooting

1. **Ngrok Not Found**:

   - Ensure Ngrok is installed and accessible in your system's PATH.
   - Test it with `ngrok version`.

2. **SSH Tunnel Issues**:

   - Verify that your SSH key and server configuration are correct.
   - Check server `logs` for SSH connection errors.

3. **No Logs Created**:

   - Ensure the script has write permissions for the `logs` directory.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue to report bugs or suggest improvements.

## License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License.
