from requests import Response

from libs.databaseConnector import DatabaseConnector
from libs.githubConnector import GitHubConnector


class Collaborators:
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
        self.url = "https://api.github.com/repos/{}/{}/collaborators?affiliation=all&per_page=100&page={}".format(
            username, repository, self.currentPage
        )

    def getData(self) -> list:
        response = self.githubConnection.openConnection(url=self.url)
        return [response.json(), response]

    def insertData(self, dataset: dict) -> None:

        for dataPoint in range(len(dataset)):
            id = dataset[dataPoint]["id"]
            login = dataset[dataPoint]["login"]
            type = dataset[dataPoint]["type"]
            siteAdmin = str(dataset[dataPoint]["site_admin"])
            canPull = str(dataset[dataPoint]["permissions"]["pull"])
            canPush = str(dataset[dataPoint]["permissions"]["push"])
            isAdmin = str(dataset[dataPoint]["permissions"]["admin"])

            sql = "INSERT OR IGNORE INTO Collaborators (ID, Login, Type, Site_Admin, Can_Pull, Can_Push, Is_Admin) VALUES (?,?,?,?,?,?,?)"

            self.connection.executeSQL(
                sql,
                (id, login, type, siteAdmin, canPull, canPush, isAdmin),
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
        self.url = "https://api.github.com/repos/{}/{}/collaborators?affiliation=all&per_page=100&page={}".format(
            self.username, self.repository, self.currentPage
        )
        return True
