from sqlite3 import Connection, Cursor
from requests import Response
from libs import *


class Commits:
    def __init__(
        self,
        dbConnection: Connection,
        oauthToken: str,
        repository: str,
        username: str,
        page: int,
    ):
        self.connection = dbConnection
        self.currentPage = page
        self.githubConnection = GitHubConnector(oauthToken=oauthToken)
        self.repository = repository
        self.username = username
        self.url = (
            "https://api.github.com/repos/{}/{}/commits?per_page=100&page={}".format(
                username, repository, page
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

            sql = "INSERT INTO COMMITS (SHA, Commit_Date, Author, Message, Comment_Count) VALUES (?,?,?,?,?);"

            self.connection.execute(sql, (sha, date, author, message, commentCount))
            self.connection.commit()

    def iterateNext(self, responseHeaders: Response) -> bool:
        if (
            self.currentPage
            == self.githubConnection.parseResponseHeaders(responseHeaders)["Last-Page"]
        ):
            return False
        self.currentPage += 1
        self.url = (
            "https://api.github.com/repos/{}/{}/commits?per_page=100&page={}".format(
                self.username, self.repository, self.currentPage
            )
        )
        return True
        # try:
        #     key_link = self.responseHeaders["Link"]
        #     if 'rel="next"' not in key_link:
        #         break
        #     else:
        #         bar = key_link.split(",")
        #         for x in bar:
        #             if 'rel="next"' in x:
        #                 url = x[x.find("<") + 1 : x.find(">")]
        #                 self.data = self.gha.access_GitHubAPISpecificURL(url=url)
        #                 self.responseHeaders = self.gha.get_ResponseHeaders()
        #                 self.parser()
        # except KeyError:
        #     print(self.responseHeaders)
        #     break
        # break
