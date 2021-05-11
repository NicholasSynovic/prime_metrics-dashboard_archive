import re
from os import name

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from requests import Response

from libs.databaseConnector import DatabaseConnector
from libs.githubConnector import GitHubCommitWebScraper, GitHubConnector


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

