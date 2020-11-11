from requests import Response

from libs.databaseConnector import DatabaseConnector
from libs.githubConnector import GitHubConnector


class Assignees:
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
            "https://api.github.com/repos/{}/{}/assignees?per_page=100&page={}".format(
                username, repository, self.currentPage
            )
        )

    def getData(self) -> list:
        response = self.githubConnection.openConnection(url=self.url)
        return [response.json(), response]

    def insertData(self, dataset: dict) -> None:
        for dataPoint in range(len(dataset)):
            id = dataset[dataPoint]["id"]
            login = dataset[dataPoint]["login"]
            userType = dataset[dataPoint]["type"]
            siteAdmin = str(dataset[dataPoint]["site_admin"])

            sql = "INSERT OR IGNORE INTO Assigness (ID, Login, Type, Site_Admin) VALUES (?,?,?,?);"

            self.connection.executeSQL(
                sql,
                (
                    id,
                    login,
                    userType,
                    siteAdmin,
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
            "https://api.github.com/repos/{}/{}/assignees?per_page=100&page={}".format(
                self.username, self.repository, self.currentPage
            )
        )
        return True
