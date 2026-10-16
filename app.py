from flask import Flask, render_template, request
import socket
import ipaddress
import time

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024  # Keep requests small.

COMMON_PORTS = {
    20: "FTP Data", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 123: "NTP", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 465: "SMTPS", 587: "SMTP Submission",
    993: "IMAPS", 995: "POP3S", 1433: "Microsoft SQL Server",
    1521: "Oracle Database", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 5900: "VNC", 6379: "Redis",
    8080: "HTTP Alternate", 8443: "HTTPS Alternate", 27017: "MongoDB",
}

def validate_host(host: str) -> str:
    host = host.strip()
    if not host or len(host) > 253:
        raise ValueError("Enter a valid hostname or IP address.")
    if any(ch.isspace() for ch in host):
        raise ValueError("Hostnames cannot contain spaces.")
    # Resolve once, then connect to the resolved address. This is a basic
    # input sanity check, not a substitute for network-level egress controls.
    try:
        socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
    except socket.gaierror:
        raise ValueError("That hostname could not be resolved. Check the spelling or DNS.")
    return host

def check_port(host: str, port: int, timeout: float = 2.5):
    started = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            elapsed_ms = round((time.perf_counter() - started) * 1000)
            return {"status": "open", "label": "Port is reachable", "detail": "A TCP connection was accepted.", "latency": elapsed_ms}
    except socket.timeout:
        return {"status": "filtered", "label": "Connection timed out", "detail": "No response arrived before the timeout. A firewall or network issue may be involved.", "latency": None}
    except ConnectionRefusedError:
        elapsed_ms = round((time.perf_counter() - started) * 1000)
        return {"status": "closed", "label": "Port is closed", "detail": "The host responded, but the connection was refused.", "latency": elapsed_ms}
    except OSError as exc:
        return {"status": "error", "label": "Could not complete check", "detail": str(exc), "latency": None}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    host = ""
    port = ""
    error = None
    if request.method == "POST":
        host = request.form.get("host", "").strip()
        port = request.form.get("port", "").strip()
        try:
            host = validate_host(host)
            if not port.isdigit() or not 1 <= int(port) <= 65535:
                raise ValueError("Port must be a number between 1 and 65535.")
            port_num = int(port)
            result = check_port(host, port_num)
            result["host"] = host
            result["port"] = port_num
            result["service"] = COMMON_PORTS.get(port_num, "Custom / Unknown service")
        except ValueError as exc:
            error = str(exc)
    return render_template("index.html", result=result, host=host, port=port, error=error, common_ports=COMMON_PORTS)

if __name__ == "__main__":
    # Local development only. Use a production WSGI server for deployment.
    app.run(host="127.0.0.1", port=5000, debug=False)
