import socket
import subprocess


def get_hostname():

    return socket.gethostname()


def get_ip_address():

    try:

        hostname = socket.gethostname()

        return socket.gethostbyname(
            hostname
        )

    except Exception:

        return "0.0.0.0"


def get_computer_uuid():

    try:

        result = subprocess.run(
            [
                "wmic",
                "csproduct",
                "get",
                "uuid"
            ],
            capture_output=True,
            text=True,
            timeout=5
        )

        lines = [
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip()
        ]

        if len(lines) >= 2:

            return lines[1]

    except Exception:
        pass

    return "UNKNOWN"