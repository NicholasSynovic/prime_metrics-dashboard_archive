from requests import Response

from libs.databaseConnector import DatabaseConnector
from libs.githubConnector import GitHubConnector


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
        repository: str,
        sha: str,
        username: str,
        url: str,
        id: int,
    ):
        """Initializes the class as well as builds the GitHub API request URI.

        Note:
            The self.url lambda function requires that the url arguement has compatible Python string formatting curly brackets ({}).

        Parameters:
            dbConnection (DatabaseConnector): A connection the database where information is being store.
            oauthToken (str): The GitHub personal access token to be used to access the GitHub API.
            apiEndpoint (str): The GitHub API endpoint.
            param_1 (str): The GitHub username of the repository that is being analyzed.
            param_2 (str): The GitHub repository name that is being analyzed.
            param_3(str): The GitHub API enpoint.
            param_4 (str): A unique identifier of an object that is being accessed via the GitHub API.
            id (int): A primary key value of a table

        Returns:
            None: An instance of he class is initalized.
        """
        self.connection = dbConnection
        self.currentPage = 1
        self.githubConnection = GitHubConnector(oauthToken=oauthToken)
        self.repository = repository
        self.sha = sha
        self.username = username
        self.url = lambda u, r, cp, sha: url.format(u, r, cp, sha)
        self.id = id

    def getData(self) -> list:
        """Returns the data recieved from the GitHub API request.

        Returns:
            list: A list containing the response JSON data and the response headers.
        """
        response = self.githubConnection.openConnection(
            url=self.url(self.username, self.repository, self.currentPage, self.sha)
        )
        return [response.json(), response]

    def iterateNext(self, responseHeaders: Response) -> bool:
        """Goes to the next page of requests if the GitHub API response has been truncated to one page.

        Parameters:
            responseHeaders (Response): The response headers returned from the request.

        Returns:
            bool: Returns False if there is no next page. If there is, the next page URI is returned.
        """
        if (
            self.githubConnection.parseResponseHeaders(responseHeaders)["Last-Page"]
            == -1
        ):
            return False

        self.currentPage += 1
        return self.githubConnection.parseResponseHeaders(responseHeaders)["Last-Page"]

    def exportID(self) -> int:
        """A getter method to return the current primary key of the working table in the database.

        Returns:
            int: The current primary key of the working table in the database.
        """
        return self.id


# TODO: Collector_3 is called this because the lambda function takes three inputs. Improve reasoning or name.
# TODO: The arguements seem needlessly complex. Can we improve the ID and Branch arguements?


class Collector_3:
    """Class to use when the GitHub API request URI requires four arguements representing what data to access.

    This class will send a request and recieve a response from the GitHub API as well as parse the response header and JSON recieved. It can also store the JSON data in a database file.

    Note:
        Typically, the three arguements are, but are not limited to:
            1. Repository Owner
            2. Repository Name
            3. Specific data to access (commits. issues, forks, etc.)
    """

    def __init__(
        self,
        dbConnection: DatabaseConnector,
        oauthToken: str,
        url: str,
        username: str,
        repository: str,
        currentPage: str = 1,
        branch: str = None,
        id: int = 0,
    ):
        """Initializes the class as well as builds the GitHub API request URI.

        Note:
            The self.url lambda function requires that the url arguement has compatible Python string formatting curly brackets ({}).

        Parameters:
            dbConnection (DatabaseConnector): A connection the database where information is being store.
            oauthToken (str): The GitHub personal access token to be used to access the GitHub API.
            url (str): The GitHub API endpoint.
            username (str): The GitHub username of the repository owner.
            repository (str): The GitHub repository that is to be analyzed.
            currentPage (str): The current page of reponses that are to be analyzed.
            branch (str): The GitHub repository branch that is to be analyzed.
            id (int): The current database primary key.

        Returns:
            None: An instance of he class is initalized.
        """
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
        """Returns the data recieved from the GitHub API request.

        Returns:
            list: A list containing the response JSON data and the response headers.
        """
        response = self.githubConnection.openConnection(
            url=self.url(self.username, self.repository, self.currentPage)
        )
        return [response.json(), response]

    def iterateNext(self, responseHeaders: Response) -> bool:
        """Goes to the next page of requests if the GitHub API response has been truncated to one page.

        Parameters:
            responseHeaders (Response): The response headers returned from the request.

        Returns:
            bool: Returns False if there is no next page. If there is, the next page URI is returned.
        """
        if (
            self.githubConnection.parseResponseHeaders(responseHeaders)["Last-Page"]
            == -1
        ):
            return False

        self.currentPage += 1
        return self.githubConnection.parseResponseHeaders(responseHeaders)["Last-Page"]

    def exportID(self) -> int:
        """A getter method to return the current primary key of the working table in the database.

        Returns:
            int: The current primary key of the working table in the database.
        """
        return self.id
