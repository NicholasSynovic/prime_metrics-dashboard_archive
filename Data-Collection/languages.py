from sqlite3 import Connection, Cursor

from requests import Response

from libs.databaseConnector import DatabaseConnector
from libs.githubConnector import GitHubConnector


class Languages:
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
        self.url = "https://api.github.com/repos/{}/{}/languages".format(
            username, repository
        )

    def getData(self) -> list:
        response = self.githubConnection.openConnection(url=self.url)
        return [response.json(), response]

    def insertData(self, dataset: dict) -> None:
        id = 0
        for key in dataset.keys():
            language = key
            bytesOfCode = dataset[key]
            sql = "INSERT OR IGNORE INTO Languages (ID, Language, Bytes_of_Code ) VALUES (?,?,?)"

            self.connection.executeSQL(
                sql,
                (id, language, bytesOfCode),
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
        self.url = "https://api.github.com/repos/{}/{}/languages".format(
            self.username, self.repository
        )
        return True
