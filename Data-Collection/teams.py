from sqlite3 import Connection, Cursor

from requests import Response

from libs.databaseConnector import DatabaseConnector
from libs.githubConnector import GitHubConnector


class Teams:
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
            "https://api.github.com/repos/{}/{}/teams?per_page=100&page={}".format(
                username, repository, self.currentPage
            )
        )

    def getData(self) -> list:
        response = self.githubConnection.openConnection(url=self.url)
        return [response.json(), response]

    def insertData(self, dataset: dict) -> None:
        for dataPoint in range(len(dataset)):

            id = dataset[dataPoint]["id"]
            name = dataset[dataPoint]["name"]
            description = dataset[dataPoint]["description"]
            privacy = dataset[dataPoint]["privacy"]
            permission = dataset[dataPoint]["permission"]
            parent = dataset[dataPoint]["parent"]

            sql = "INSERT OR IGNORE INTO Teams (ID, Name, Description, Privacy, Permission, Parent) VALUES (?,?,?,?,?,?)"

            self.connection.executeSQL(
                sql,
                (
                    id,
                    name,
                    description,
                    privacy,
                    permission,
                    parent,
                ),
                True,
            )

    def iterateNext(self, responseHeaders: Response) -> bool:
        if (
            self.githubConnection.parseResponseHeaders(responseHeaders)["Last-Page"]
            == -1
        ):
            return False

        self.currentPage += 1
        self.url = (
            "https://api.github.com/repos/{}/{}/teams?per_page=100&page={}".format(
                self.username, self.repository, self.currentPage
            )
        )
        return True
