import socket
import time
import subprocess



def get_computer_uuid():

    result = subprocess.run(
        ["wmic", "csproduct", "get", "uuid"],
        capture_output=True,
        text=True
    )

    lines = [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    return lines[1]


def get_system_info():

    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    return {
        "hostname": hostname,
        "ip": ip,
        "status": "online",
        "timestamp": int(time.time())
    }