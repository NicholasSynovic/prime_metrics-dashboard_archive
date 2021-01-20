# TODO: Fix the inputs of the classes to be generic instead of specific

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
        self.url = lambda param1, param2, param3, param4: url.format(
            param1, param2, param3, param4
        )

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
        currentPage: str = "1",
        id: int = 0,
        branch: str = None,
    ):
        self.id = id
        self.branch = branch
        self.connection = dbConnection
        self.currentPage = currentPage
        self.githubConnection = GitHubConnector(oauthToken=oauthToken)
        self.repository = repository
        self.username = username
        self.url = lambda param1, param2, param3,: url.format(
            param1,
            param2,
            param3,
        )

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

    def exportID(self) -> int:
        return self.id
