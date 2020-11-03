from datetime import datetime
from sqlite3 import Connection, Cursor

from githubAPI import GitHubAPI


class Commits:
    def __init__(
        self,
        gha: GitHubAPI = None,
        data: dict = None,
        responseHeaders: tuple = None,
        cursor: Cursor = None,
        connection: Connection = None,
    ):

        self.gha = gha
        self.data = data
        self.responseHeaders = responseHeaders
        self.dbCursor = cursor
        self.dbConnection = connection

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

    def get_author_name(self, x) -> str:
        return self.data[x]["commit"]["author"]["name"]

    def get_committer_name(self, x) -> str:
        return self.data[x]["commit"]["committer"]["name"]

    def get_message(self, x) -> str:
        return self.data[x]["commit"]["message"]

    def get_comment_count(self, x) -> int:
        return self.data[x]["commit"]["comment_count"]

    def get_commits_url(self, x) -> str:
        return self.data[x]["commit"]["url"]

    def get_comments_url(self, x) -> str:
        return self.data[x]["comments_url"]

    def get_author_date(self, x) -> datetime:
        author_date = (
            self.data[x]["commit"]["author"]["date"].replace("T", " ").replace("Z", " ")
        )
        author_date = datetime.strptime(author_date, "%Y-%m-%d %H:%M:%S ")
        return author_date

    def get_committer_date(self, x) -> datetime:
        committer_date = (
            self.data[x]["commit"]["committer"]["date"]
            .replace("T", " ")
            .replace("Z", " ")
        )
        committer_date = datetime.strptime(committer_date, "%Y-%m-%d %H:%M:%S ")
        return committer_date

    def get_github_data(self, other_func, x):
        try:
            return_string = other_func(x)
        except KeyError:
            return_string = "NA"
        except AttributeError:
            return_string = "NA"
        return return_string
