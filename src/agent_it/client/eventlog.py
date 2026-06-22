import win32evtlog
import win32evtlogutil
import json
from pathlib import Path

STATE_FILE = Path("state.json")


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"last_record_id": 0}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state))


def read_events():

    state = load_state()
    last_record = state["last_record_id"]

    query = "*[System[(EventID=6005 or EventID=6006 or EventID=6008)]]"

    handle = win32evtlog.EvtQuery(
        "System",
        win32evtlog.EvtQueryForwardDirection,
        query
    )

    newest_record = last_record

    while True:

        events = win32evtlog.EvtNext(handle, 10)

        if not events:
            break

        for event in events:

            values = win32evtlog.EvtRender(
                event,
                win32evtlog.EvtRenderEventValues
            )

            event_id = values[win32evtlog.EvtSystemEventID]
            record_id = values[win32evtlog.EvtSystemEventRecordId]
            timestamp = values[win32evtlog.EvtSystemTimeCreated]

            if record_id <= last_record:
                continue

            if event_id == 6005:
                event_type = "boot"

            elif event_id == 6006:
                event_type = "shutdown"

            elif event_id == 6008:
                event_type = "crash"

            else:
                continue

            event_data = {
                "event": event_type,
                "record_id": record_id,
                "timestamp": str(timestamp)
            }

            print(event_data)

            if record_id > newest_record:
                newest_record = record_id

    state["last_record_id"] = newest_record
    save_state(state)