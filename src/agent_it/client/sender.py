import requests
from agent_it.common.config import SERVER_URL


def send_event(event):

    try:

        r = requests.post(
            SERVER_URL,
            json=event,
            timeout=5
        )

        if r.status_code == 200:
            return True

    except Exception:
        pass

    return False