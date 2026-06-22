import socket
import time


def get_system_info():

    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    return {
        "hostname": hostname,
        "ip": ip,
        "status": "online",
        "timestamp": int(time.time())
    }