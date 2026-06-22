from agent_it.client.agent import start_agent
from agent_it.server.api import start_server
import sys


def main():

    if sys.argv[1] == "agent":
        print("Starting agent...")
        start_agent()

    elif sys.argv[1] == "server":
        start_server()


if __name__ == "__main__":
    main()