from datetime import datetime
import xml.etree.ElementTree as ET

import win32evtlog

from agent_it.common.constants import EVENT_NAMES
from agent_it.common.logger import logger


LOG_NAME = "System"

WATCHED_EVENTS = set(EVENT_NAMES.keys())


def parse_xml(xml):

    return ET.fromstring(xml)


def extract_event_id(xml):

    root = parse_xml(xml)

    return int(
        root.find(
            ".//{*}EventID"
        ).text
    )


def extract_record_id(xml):

    root = parse_xml(xml)

    return int(
        root.find(
            ".//{*}EventRecordID"
        ).text
    )


def extract_timestamp(xml):

    root = parse_xml(xml)

    node = root.find(
        ".//{*}TimeCreated"
    )

    timestamp = node.attrib["SystemTime"]

    return datetime.fromisoformat(
        timestamp.replace("Z", "+00:00")
    )


def get_new_events(last_record_id: int):

    event_filter = " or ".join(
        f"EventID={event_id}"
        for event_id in WATCHED_EVENTS
    )

    query = (
        f"*[System[({event_filter})]]"
    )

    logger.info(
        f"Recherche événements après RecordId={last_record_id}"
    )

    handle = win32evtlog.EvtQuery(
        LOG_NAME,
        win32evtlog.EvtQueryReverseDirection,
        query
    )

    events = []

    while True:

        try:

            records = win32evtlog.EvtNext(
                handle,
                50
            )

        except Exception:
            break

        if not records:
            break

        for record in records:

            xml = win32evtlog.EvtRender(
                record,
                win32evtlog.EvtRenderEventXml
            )

            event_id = extract_event_id(xml)

            record_id = extract_record_id(xml)

            # Comme on lit du plus récent vers le plus ancien,
            # dès qu'on atteint le dernier événement déjà envoyé,
            # on peut arrêter la recherche.
            if record_id <= last_record_id:

                events.sort(
                    key=lambda e: e["record_id"]
                )

                logger.info(
                    f"{len(events)} nouvel(s) événement(s) trouvé(s)"
                )

                return events

            events.append(
                {
                    "record_id": record_id,
                    "event_id": event_id,
                    "event_timestamp": extract_timestamp(xml)
                }
            )

    events.sort(
        key=lambda e: e["record_id"]
    )

    logger.info(
        f"{len(events)} nouvel(s) événement(s) trouvé(s)"
    )

    return events