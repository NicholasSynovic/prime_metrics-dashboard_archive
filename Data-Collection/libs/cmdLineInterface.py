import argparse
from argparse import Namespace


def arguementHandling() -> Namespace:
    """The method responsible for collecting and parsing command line inputs from the user.

    Important:
        Only meant to be used to initalize the Data Collection porition of the Metrics Dashboard at the current time.

    Note:
        It does not take any arguements.

    Returns:
        Namespace: Contains the user's GitHub Personal Access Token, the database that will be used to store information about a repository, and the repository URL that is to be scraped for information.
    """
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
