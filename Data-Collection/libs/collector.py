# TODO: Fix the arguements of the classes to have generic names instead of specific ones

from requests import Response

from libs.databaseConnector import DatabaseConnector
from libs.githubConnector import GitHubConnector

# TODO: Collector_4 is called this because the lambda function takes four inputs. Improve reasoning or name.
class Collector_4:
    """Class to use when the GitHub API request URI requires four arguements representing what data to access.

    This class will send a request and recieve a response from the GitHub API as well as parse the response header and JSON recieved. It can also store the JSON data in a database file.

    Note:
        Typically, the four arguements are, but are not limited to:
            1. Repository Owner
            2. Repository Name
            3. Specific data to access (commits. issues, forks, etc.)
            4. Data specific information (hash code or SHA)
    """

    def __init__(
        self,
        dbConnection: DatabaseConnector,
        oauthToken: str,
        url: str,
        param_1: int,
        param_2: str,
        param_3: str,
        param_4: str,
    ):
        """Initializes the class as well as builds the GitHub API request URI.

        Note:
            The self.url lambda function requires that the url arguement has compatible Python string formatting curly brackets ({}).
        """
        self.connection = dbConnection
        self.currentPage = 1
        self.githubConnection = GitHubConnector(oauthToken=oauthToken)
        self.params = [param_1, param_2, param_3, param_4]
        self.url = lambda param1, param2, param3, param4: url.format(
            param1, param2, param3, param4
        )

    def getData(self) -> list:
        response = self.githubConnection.openConnection(
            url=self.url(self.params[0], self.params[1], self.params[2], self.params[3])
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


# TODO: Collector_3 is called this because the lambda function takes three inputs. Improve reasoning or name.
# TODO: The arguements seem needlessly complex. Can we improve the ID and Branch arguements?


class Collector_3:
    def __init__(
        self,
        dbConnection: DatabaseConnector,
        oauthToken: str,
        repository: str,
        username: str,
        url: str,
        currentPage: str = 1,
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
