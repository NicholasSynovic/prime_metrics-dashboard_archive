import argparse
from argparse import Namespace


def arguementHandling() -> Namespace:
    parser = argparse.ArgumentParser(
        prog="SSL Data Collection Module",
        usage="To download and store GitHub repository information using the GitHub APIs.",
        description="This module was written by the Software and System's Laboratory (SSL) Metrics Dashboard team in order to facilitate the collection and storage of data derived from the GitHub APIs.",
        epilog="While this module can be ran on its own, it is best ran as part of the larger SSL Metrics Dashboard.",
    )

    parser.add_argument(
        "-u",
        "--url",
        nargs=1,
        default="https://github.com/SoftwareSystemsLaboratory/Metrics-Dashboard",
        type=str,
        required=True,
        help="The GitHub repository URL.",
    )

    parser.add_argument(
        "-t",
        "--token",
        nargs=1,
        type=str,
        required=True,
        help="A GitHub OAuth Token/ Personal Access Token with the 'repo' scope enabled.",
    )

    parser.add_argument(
        "-o",
        "--outfile",
        nargs=1,
        default="Metrics Dashboard.db",
        type=str,
        required=True,
        help="The database file to store the collected data from GitHub.",
    )

    return parser.parse_args()

if __name__ == "__main__":
    print("""This file is not meant to be ran as a standalone program.
Please import this file into your application.""")

