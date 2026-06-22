import time
from agent_it.client.eventlog import get_new_events
from agent_it.client.sender import send_event
from agent_it.client.state import get_last_record, save_last_record
from agent_it.common.logger import logger
from agent_it.common.config import POLL_INTERVAL


def start_agent():
    """
    Démarre l'agent de monitoring.
    Envoie périodiquement l'état de la machine au serveur.
    """

    logger.info("Agent démarré")

    system_info = get_system_info()

    while True:
        try:
            publish_status(system_info)
            logger.info("Heartbeat envoyé")
        except Exception as e:
            logger.error(f"Erreur envoi heartbeat : {e}")

        time.sleep(HEARTBEAT_INTERVAL)