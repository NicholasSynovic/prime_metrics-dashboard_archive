from sqlite3 import Connection, Cursor

from requests import Response

from libs.databaseConnector import DatabaseConnector
from libs.githubConnector import GitHubConnector


class Contributors:
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
        self.url = "https://api.github.com/repos/{}/{}/contributors?anon=true&per_page=100&page={}".format(
            username, repository, self.currentPage
        )

    def getData(self) -> list:
        response = self.githubConnection.openConnection(url=self.url)
        return [response.json(), response]

    def insertData(self, dataset: dict) -> None:
        for dataPoint in range(len(dataset)):

            try:
                id = str(dataset[dataPoint]["id"])
            except KeyError:
                id = dataset[dataPoint]["email"]
            try:
                login = dataset[dataPoint]["login"]
            except KeyError:
                login = dataset[dataPoint]["name"]
            type = dataset[dataPoint]["type"]
            try:
                siteAdmin = str(dataset[dataPoint]["site_admin"])
            except KeyError:
                siteAdmin = "False"
            contributions = str(dataset[dataPoint]["contributions"])

            sql = "INSERT OR IGNORE INTO Contributors (ID, Login, Type, Site_Admin, Contributions) VALUES (?,?,?,?,?)"

            self.connection.executeSQL(
                sql,
                (
                    id,
                    login,
                    type,
                    siteAdmin,
                    contributions,
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
        self.url = "https://api.github.com/repos/{}/{}/contributors?anon=true&per_page=100&page={}".format(
            self.username, self.repository, self.currentPage
        )
        return True
