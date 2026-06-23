# server/server.py

import uvicorn


def main():

    uvicorn.run(
        "agent_it.server.api:app",
        host="0.0.0.0",
        port=8000
    )