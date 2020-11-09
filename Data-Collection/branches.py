from sqlite3 import Connection, Cursor

from requests import Response

from libs.databaseConnector import DatabaseConnector
from libs.githubConnector import GitHubConnector


class Branches:
    def __init__(
        self,
        dbConnection: DatabaseConnector,
        oauthToken: str,
        repository: str,
        username: str,
    ):
        self.connection = dbConnection
        self.currentPage = 1
        self.githubConnection = GitHubConnector(oauthToken=oauthToken)
        self.repository = repository
        self.username = username
        self.url = (
            "https://api.github.com/repos/{}/{}/branches?per_page=100&page={}".format(
                username, repository, self.currentPage
            )
        )

    def getData(self) -> list:
        response = self.githubConnection.openConnection(url=self.url)
        return [response.json(), response]

    def insertData(self, dataset: dict) -> None:
        id = 0

        for dataPoint in range(len(dataset)):
            name = dataset[dataPoint]["name"]
            commitSHA = dataset[dataPoint]["commit"]["sha"]

            sql = "INSERT OR IGNORE INTO Branches (ID, Name, Commit_SHA) VALUES (?,?,?)"

            self.connection.executeSQL(
                sql,
                (id, name, commitSHA),
                True,
            )

            id += 1

    def iterateNext(self, responseHeaders: Response) -> bool:
        if (
            self.githubConnection.parseResponseHeaders(responseHeaders)["Last-Page"]
            == -1
        ):
            return False

        self.currentPage += 1
        self.url = (
            "https://api.github.com/repos/{}/{}/branches?per_page=100&page={}".format(
                self.username, self.repository, self.currentPage
            )
        )
        return True
