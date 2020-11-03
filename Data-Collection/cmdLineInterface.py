import argparse
from argparse import Namespace

import main


class DataCollection:
    def arguementHandling(self) -> Namespace:
        parser = argparse.ArgumentParser(
            prog="SSL Metrics Dashboard Defect Density Module",
            usage="To collect, store, parse, and calculate information related to the Defect Density software metric.",
            description="This module will access the GitHub REST API to gather information about a specific repository pertaining to Defect Density.\n\n Afterwards, the data will be analyzed and displayed as graphs.",
            epilog="This program was created by the Loyola University Chicago Software and Systems Laboratory.",
        )

        parser.add_argument(
            "-u",
            "--url",
            nargs=1,
            default="https://github.com/SoftwareSystemsLaboratory/Metrics-Dashboard",
            type=str,
            required=True,
            help="The GitHub URL of the project that is to be analyzed",
        )
        parser.add_argument(
            "-t",
            "--token",
            nargs=1,
            default="",
            type=str,
            required=True,
            help="The GitHub Personal Access Token that is used to properly interact with the GitHub REST API",
        )
        parser.add_argument(
            "-f",
            "--outFile",
            nargs=1,
            default="Metrics-Dashboard",
            type=str,
            required=True,
            help="The database file where all data will be stored and analyzed",
        )

        return parser.parse_args()

    def stripURL(self, url: str) -> list:
        if url.find("github.com/") == -1:
            exit("❗ Invalid URL Arg: {}".format(url))

        splitURL = self.githubURL.split("/")

        if len(splitURL) != 5:
            exit("❗ Invalid URL Arg")

        username = splitURL[-2]
        repository = splitURL[-1]

        return [repository, username]

    def startDataCollection(
        self,
        repository: str,
        repositoryURL: str,
        username: str,
        token: str,
        outFile: str,
    ) -> None:
        pass


if __name__ == "__main__":
    s = DataCollection()

    args = s.arguementHandling()

    url = args.url[0]
    token = args.token[0]
    outFile = args.outFile[0]

    parsedValues = s.stripURL(url=args.url[0])

    s.startDataCollection(
        repository=parsedValues[0],
        repositoryURL=url,
        username=parsedValues[1],
        token=token,
        outFile=outFile,
    )
