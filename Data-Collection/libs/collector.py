from requests import Response

from libs.databaseConnector import DatabaseConnector
from libs.githubConnector import GitHubConnector


class Collector_4:
    def __init__(
        self,
        dbConnection: DatabaseConnector,
        id: int,
        oauthToken: str,
        repository: str,
        sha: str,
        username: str,
        url: str,
    ):
        self.connection = dbConnection
        self.currentPage = 1
        self.githubConnection = GitHubConnector(oauthToken=oauthToken)
        self.id = id
        self.repository = repository
        self.sha = sha
        self.username = username
        self.url = lambda u, r, cp, sha: url.format(u, r, cp, sha)

    def getData(self) -> list:
        response = self.githubConnection.openConnection(
            url=self.url(self.username, self.repository, self.currentPage, self.sha)
        )
        return [response.json(), response]

    def iterateNext(self, responseHeaders: Response) -> bool:
        if (
            self.githubConnection.parseResponseHeaders(responseHeaders)["Last-Page"]
            == -1
        ):
            return False

        self.currentPage += 1
        return self.githubConnection.parseResponseHeaders(responseHeaders)["Last-Page"]

    def exportID(self) -> int:
        return self.id


class Collector_3:
    def __init__(
        self,
        dbConnection: DatabaseConnector,
        oauthToken: str,
        repository: str,
        username: str,
        url: str,
    ):
        self.connection = dbConnection
        self.currentPage = 1
        self.githubConnection = GitHubConnector(oauthToken=oauthToken)
        self.repository = repository
        self.username = username
        self.url = lambda u, r, cp: url.format(u, r, cp)

    def getData(self) -> list:
        response = self.githubConnection.openConnection(
            url=self.url(self.username, self.repository, self.currentPage)
        )
        return [response.json(), response]

    def iterateNext(self, responseHeaders: Response) -> bool:
        if (
            self.githubConnection.parseResponseHeaders(responseHeaders)["Last-Page"]
            == -1
        ):
            return False

        self.currentPage += 1
        return self.githubConnection.parseResponseHeaders(responseHeaders)["Last-Page"]
