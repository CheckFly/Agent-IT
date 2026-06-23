import json

from agent_it.common.config import STATE_FILE


def get_last_record():

    if not STATE_FILE.exists():
        return 0

    with open(
        STATE_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    return data.get(
        "last_record_id",
        0
    )


def save_last_record(record_id):

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "last_record_id": record_id
            },
            f,
            indent=4
        )