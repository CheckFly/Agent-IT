import argparse

from agent_it.common.bootstrap import initialize_environment


def main():

    parser = argparse.ArgumentParser(
        prog="Agent_IT",
        description="Agent_IT Client / Server"
    )

    parser.add_argument(
        "mode",
        nargs="?",
        default="client",
        choices=["client", "server"],
        help="Mode de fonctionnement"
    )

    args = parser.parse_args()

    initialize_environment()

    if args.mode == "client":

        from agent_it.client.agent import (
            main as client_main
        )

        client_main()

    elif args.mode == "server":

        from agent_it.server.server import (
            main as server_main
        )

        server_main()


if __name__ == "__main__":
    main()