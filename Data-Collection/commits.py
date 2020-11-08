from sqlite3 import Connection, Cursor

from requests import Response

from libs import *


class Commits:
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
            "https://api.github.com/repos/{}/{}/commits?per_page=100&page={}".format(
                username, repository, self.currentPage
            )
        )

    def getData(self) -> list:
        response = self.githubConnection.openConnection(url=self.url)
        return [response.json(), response]

    def insertData(self, dataset: dict) -> None:
        for dataPoint in range(len(dataset)):
            sha = dataset[dataPoint]["sha"]
            date = dataset[dataPoint]["commit"]["committer"]["date"]
            author = dataset[dataPoint]["commit"]["author"]["name"]
            message = dataset[dataPoint]["commit"]["message"]
            commentCount = dataset[dataPoint]["commit"]["comment_count"]

            sql = "INSERT OR IGNORE INTO COMMITS (SHA, Commit_Date, Author, Message, Comment_Count) VALUES (?,?,?,?,?);"

            self.connection.executeSQL(
                sql, (sha, date, author, message, commentCount), True
            )

    def iterateNext(self, responseHeaders: Response) -> bool:
        if (
            self.githubConnection.parseResponseHeaders(responseHeaders)["Last-Page"]
            == -1
        ):
            return False
        self.currentPage += 1
        self.url = (
            "https://api.github.com/repos/{}/{}/commits?per_page=100&page={}".format(
                self.username, self.repository, self.currentPage
            )
        )
        return True
