from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from agent_it.server.database import SessionLocal
from agent_it.server.models import ActivityEvent
from agent_it.common.constants import EVENT_NAMES
from agent_it.common.logger import logger



app = FastAPI(
    title="Agent_IT Server",
    version="0.1.0"
    logger.info("API Agent_IT démarrée")
)

@app.middleware("http")
async def log_requests(request, call_next):

    logger.info(
        f"{request.client.host} "
        f"{request.method} "
        f"{request.url.path}"
    )

    response = await call_next(request)

    logger.info(
        f"STATUS={response.status_code}"
    )

    return response

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/events")
async def receive_event(event: ActivityEvent):
    
    logger.info(event.model_dump_json())

    db = SessionLocal()

    try:
        
        event_name = EVENT_NAMES.get(
            event.event_id,
            f"EVENT_{event.event_id}"
        )

        # Historique
        db.execute(
            text("""
                INSERT IGNORE INTO Activity_WS
                (
                    HostName,
                    ComputerUUID,
                    IpAddress,
                    EventId,
                    EventName,
                    RecordId,
                    EventTimestamp,
                    AgentVersion
                )
                VALUES
                (
                    :hostname,
                    :computer_uuid,
                    :ip_address,
                    :event_id,
                    :event_name,
                    :record_id,
                    :event_timestamp,
                    :agent_version
                )
            """),
            {
                "hostname": event.hostname,
                "ip_address": event.ip_address,
                "event_id": event.event_id,
                "event_name": event_name,
                "record_id": event.record_id,
                "event_timestamp": event.event_timestamp,
                "agent_version": event.agent_version
            }
        )

        # Etat courant
        db.execute(
            text("""
                INSERT INTO Workstation
                (
                    Hostname,
                    ComputerUUID,
                    LastSeen,
                    LastEventId,
                    LastEventTimestamp
                )
                VALUES
                (
                    :hostname,
                    :computer_uuid,
                    NOW(),
                    :event_id,
                    :event_timestamp
                )
                ON DUPLICATE KEY UPDATE
                    LastSeen = NOW(),
                    LastEventId = VALUES(LastEventId),
                    LastEventTimestamp = VALUES(LastEventTimestamp)
            """),
            {
                "hostname": event.hostname,
                "computer_uuid": event.computer_uuid,
                "event_id": event.event_id,
                "event_timestamp": event.event_timestamp
            }
        )

        db.commit()

        return {
            "status": "ok",
            "record_id": event.record_id
        }

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        db.close()
        
