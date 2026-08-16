# TunnelBridge

Scripts for managing SSH and Ngrok tunnels in closed or restricted network environments. TunnelBridge helps maintain connectivity, monitor tunnel availability, and automatically re-establish tunnels when needed.

## Features

- **SSH Tunnel Management**

  - Establishes and maintains reverse SSH tunnels.
  - Automatically reconnects SSH tunnels when necessary.
  - Uses configurable remote-forwarding ports.

- **Ngrok Tunnel Management**

  - Checks whether an active Ngrok tunnel is available.
  - Automatically recreates the tunnel when necessary.
  - Supports TCP tunneling for SSH and other services.

- **Network Connectivity Check**

  - Checks connectivity to a configurable remote host.
  - Can optionally attempt to reconnect to a network requiring web-based authentication.

- **Daily Logging**

  - Stores script activity in a `logs` directory.
  - Creates a separate log file for each day.
  - Includes timestamps and log levels (`INFO`, `WARNING`, `ERROR`).

## Prerequisites

### Python

The tunnel monitoring script requires:

- Python 3
- `requests`
- `beautifulsoup4`

Install the Python dependencies with:

```bash
pip install requests beautifulsoup4
```

### SSH

Ensure OpenSSH is installed and configured for key-based authentication.

The SSH key should **not** be stored in this repository. Configure the scripts to use a private key located outside the repository.

### Autossh

The reverse SSH helper scripts require `autossh` and `tmux`.

Install them using your system's package manager. For example, on Debian/Ubuntu:

```bash
sudo apt install autossh tmux
```

### Ngrok

Install Ngrok and ensure it is available in your system's `PATH`.

## Scripts

### `Check-Tunnel.py`

Monitors network connectivity and tunnel availability.

It:

1. Checks connectivity to a configured remote host.
2. Checks whether the SSH reverse tunnel is available.
3. Re-establishes the SSH tunnel if necessary.
4. Checks for an active Ngrok tunnel.
5. Recreates the Ngrok tunnel if necessary.
6. Records activity in daily log files.

### `start_reverse_ssh.sh`

Starts a persistent reverse SSH tunnel using `autossh` inside a detached `tmux` session.

The connection details should be configured for your environment and should not contain credentials or private keys in the repository.

### `stop_reverse_ssh.sh`

Stops the reverse SSH tunnel and terminates the associated `tmux` session.

## Configuration

The scripts contain environment-specific connection settings that must be adjusted before use.

### SSH Tunnel

Configure the SSH connection according to your environment:

```bash
autossh -M 0 -N \
    -o ServerAliveInterval=30 \
    -o ServerAliveCountMax=3 \
    -o ExitOnForwardFailure=yes \
    -R <remote-port>:localhost:<local-port> \
    <user>@<host> -p <ssh-port> -i <path-to-private-key>
```

Keep private keys outside the repository and use appropriate file permissions.

### Ngrok

For a TCP tunnel, configure the required local port:

```bash
ngrok tcp <port>
```

The Ngrok client must be installed and configured separately.

### Network Login

If your network requires authentication through a login endpoint, configure the endpoint and credentials for your environment.

**Do not commit real usernames, passwords, API tokens, or other credentials to the repository.**

For example:

```python
requests.post(
    "<network-login-url>",
    data={
        "username": "<username>",
        "password": "<password>"
    }
)
```

## Usage

Clone the repository:

```bash
git clone <repository-url>
cd TunnelBridge
```

Make the shell scripts executable:

```bash
chmod +x start_reverse_ssh.sh stop_reverse_ssh.sh
```

Run the tunnel monitoring script:

```bash
python3 Check-Tunnel.py
```

Start the reverse SSH tunnel:

```bash
./start_reverse_ssh.sh
```

Stop the reverse SSH tunnel:

```bash
./stop_reverse_ssh.sh
```

## Logs

`Check-Tunnel.py` stores logs in the `logs` directory.

A new log file is created for each day using the following format:

```text
YYYY-MM-DD.log
```

Example:

```text
logs/
├── 2024-12-07.log
├── 2024-12-08.log
└── 2024-12-09.log
```

Example output:

```text
2024-12-07 10:00:00 - INFO - Script started.
2024-12-07 10:00:01 - INFO - Internet connection status: True
2024-12-07 10:00:01 - INFO - Checking Ngrok tunnel status...
2024-12-07 10:00:02 - INFO - Ngrok tunnel exists at: tcp://example.ngrok.io
2024-12-07 10:00:02 - INFO - Checking tunnel status and port availability...
2024-12-07 10:00:02 - INFO - Port is in use, tunnel is available.
```

## Troubleshooting

### Ngrok Not Found

Ensure Ngrok is installed and available in `PATH`:

```bash
ngrok version
```

### SSH Tunnel Issues

Check that:

- The SSH server is reachable.
- The configured SSH port is correct.
- The SSH key exists and has appropriate permissions.
- The key is authorized on the remote server.
- Reverse port forwarding is permitted by the SSH server.

### No Logs Created

Ensure the user running the script has write permission for the repository's `logs` directory.

## Security Considerations

This project is intended for use in environments where direct network connectivity is restricted or unavailable.

Before deploying it:

- Never commit private SSH keys.
- Never commit passwords, API tokens, or authentication cookies.
- Avoid hardcoding production IP addresses and hostnames when they are not necessary.
- Restrict SSH keys and accounts to the minimum required permissions.
- Carefully review which local ports are exposed through reverse or Ngrok tunnels.
- Ensure that exposed services require appropriate authentication.

A tunnel provides a communication path; it does not automatically make the service behind the tunnel secure.

## Contributing

Contributions are welcome. Feel free to submit a pull request or open an issue for bug reports, improvements, or new features.

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
