# PortScope — TCP Port Checker

A polished Flask website for checking whether a TCP port is reachable from the machine running the app.

## Features

- Responsive dark UI with mint accents
- Hostname or IP address input
- Common port shortcuts and service selector
- TCP connection result: reachable, refused, timeout, or error
- Basic response-time measurement
- Input validation and a short connection timeout

## Run locally

Python 3.10+ recommended.

```bash
# 1. Create and activate a virtual environment (optional but recommended)
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\\Scripts\\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the site
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Important notes

- This performs a **single TCP connection test** to the host and port you enter. It is not a vulnerability scanner and does not identify the software running on a port.
- Results reflect connectivity from the machine running this Flask app, which may differ from your laptop or another network.
- Only test systems you own or have explicit permission to assess.
- The development server is bound to localhost. Before deploying, use a production WSGI server, add rate limiting and authentication as appropriate, and apply network egress controls. Do not expose an unrestricted network-checking endpoint to the public internet.
- A timeout is inconclusive: firewalls, routing, or a host that silently drops packets can all cause it.
