import requests

from agent_it.common.config import (
    SERVER_URL,
    AGENT_NAME,
    AGENT_VERSION
)

from agent_it.common.logger import logger

from agent_it.client.system import (
    get_hostname,
    get_computer_uuid,
    get_ip_address
)


def send_event(event):

    hostname = get_hostname()
    ip_address = get_ip_address()
    computer_uuid = get_computer_uuid()

    payload = {
        "source_application": AGENT_NAME,
        "agent_version": AGENT_VERSION,
        "hostname": hostname,
        "computer_uuid": computer_uuid,
        "ip_address": ip_address,
        "event_id": event["event_id"],
        "record_id": event["record_id"],
        "event_timestamp": event["event_timestamp"].isoformat()
    }

    logger.info(
        f"Envoi EventID={event['event_id']} "
        f"RecordID={event['record_id']} "
        f"Host={hostname} "
        f"IP={ip_address} "
        f"Vers={SERVER_URL}"
    )

    try:

        response = requests.post(
            SERVER_URL,
            json=payload,
            timeout=5
        )

        logger.info(
            f"Réponse serveur : "
            f"{response.status_code}"
        )

        if response.status_code == 200:
            return True

        logger.error(
            f"Erreur HTTP : "
            f"{response.status_code} "
            f"{response.text}"
        )

    except Exception as e:

        logger.exception(
            f"Erreur envoi EventID={event['event_id']}"
        )

    return False