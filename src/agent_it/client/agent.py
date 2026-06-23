from agent_it.client.eventlog import get_new_events
from agent_it.client.sender import send_event
from agent_it.client.state import (
    get_last_record,
    save_last_record
)

from agent_it.common.logger import logger


def main():

    logger.info("Agent_IT démarré")

    last_record = get_last_record()

    logger.info(
        f"Dernier RecordId envoyé : {last_record}"
    )

    events = get_new_events(last_record)

    logger.info(
        f"{len(events)} événement(s) trouvé(s)"
    )

    for event in events:

        logger.info(
            f"Traitement EventId={event['event_id']} "
            f"RecordId={event['record_id']}"
        )

        if send_event(event):

            save_last_record(
                event["record_id"]
            )

            logger.info(
                f"RecordId {event['record_id']} sauvegardé"
            )

        else:

            logger.error(
                f"Echec envoi RecordId={event['record_id']}"
            )

            # on s'arrête pour réessayer plus tard
            break

    logger.info("Agent_IT terminé")