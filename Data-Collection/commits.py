from datetime import datetime
from sqlite3 import Connection, Cursor

from libs import *


class Commits:
    def __init__(
        self,
        dbConnection: Connection,
        dbCursor: Cursor,
        oauthToken: str,
        repository: str,
        username: str,
    ):
        self.connection = dbConnection
        self.cursor = dbCursor
        self.githubConnection = GitHubConnector(oauthToken=oauthToken)
        self.url = (
            "https://api.github.com/repos/{}/{}/commits?per_page=100&page={}".format(
                username,
                repository,
            )
        )

    def getData(self) -> dict:
        self.githubConnection.openConnection(url=self.url)

    def parser(self) -> None:

        while True:
            for x in range(len(self.data)):
                author = self.get_github_data(self.get_author_name, x)
                committer = self.get_github_data(self.get_committer_name, x)
                message = self.get_github_data(self.get_message, x)
                comment_count = self.get_github_data(self.get_comment_count, x)
                commits_url = self.get_github_data(self.get_commits_url, x)
                comments_url = self.get_github_data(self.get_commits_url, x)
                author_date = self.get_github_data(self.get_author_date, x)
                committer_date = self.get_github_data(self.get_committer_date, x)
                sql = "INSERT INTO COMMITS (author, author_date, committer, committer_date, commits_url, message, comment_count, comments_url) VALUES (?,?,?,?,?,?,?,?);"
                self.dbCursor.execute(
                    sql,
                    (
                        str(author),
                        str(author_date),
                        str(committer),
                        str(committer_date),
                        str(commits_url),
                        str(message),
                        str(comment_count),
                        str(comments_url),
                    ),
                )

                self.dbConnection.commit()

            try:
                key_link = self.responseHeaders["Link"]
                if 'rel="next"' not in key_link:
                    break
                else:
                    bar = key_link.split(",")
                    for x in bar:
                        if 'rel="next"' in x:
                            url = x[x.find("<") + 1 : x.find(">")]
                            self.data = self.gha.access_GitHubAPISpecificURL(url=url)
                            self.responseHeaders = self.gha.get_ResponseHeaders()
                            self.parser()
            except KeyError:
                print(self.responseHeaders)
                break
            break
