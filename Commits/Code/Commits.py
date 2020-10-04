from datetime import datetime
from githubAPI import GitHubAPI
from sqlite3 import Cursor, Connection


class Logic:
    """
    This class contains the methods needed to access the GitHub Repository Commits API as well as any class specific variables.
    """

    def __init__(
        self,
        gha: GitHubAPI = None,
        data: dict = None,
        responseHeaders: tuple = None,
        cursor: Cursor = None,
        connection: Connection = None,
    ):
        """
        This initializes the class and sets class variables specific variables.\n
        :param gha: An instance of the GitHubAPI class.\n
        :param data: The dictionary of data that is returned from the API call.\n
        :param responseHeaders: The dictionary of data that is returned with the API call.\n
        :param cursor: The database cursor.\n
        :param connection: The database connection.
        """
        self.gha = gha
        self.data = data
        self.responseHeaders = responseHeaders
        self.dbCursor = cursor
        self.dbConnection = connection

    def parser(self) -> None:
        """
        Actually scrapes, sanitizes, and stores the data returned from the API call.
        """
        while True:
            for x in range(len(self.data)):
                # Values below are the values that are to be returned/set if parsing FAILS
                author = "NA"
                author_date = "NA"
                committer = "NA"
                committer_date = "NA"
                message = "NA"  # Message associated with the commit
                comment_count = "NA"  # Number of comments per commit
                commits_url = "NA"
                comments_url = "NA"

                # for the following item, pass in the x param into the functions
                # code was split into function for testing purposes 

                try:
                    author = self.get_author_name(x)
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    committer = self.get_committer_name(x)
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    message = self.get_message(x)
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    comment_count = self.get_comment_count(x)
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    commits_url = self.get_comment_url(x)
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    comments_url = self.comments_url(x)
                except KeyError:
                    pass
                except AttributeError:
                    pass

                # Scrapes and sanitizes the time related data
                try:
                    author_date = self.get_author_date(x)
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    committer_date = (
                        self.data[x]["commit"]["committer"]["date"]
                        .replace("T", " ")
                        .replace("Z", " ")
                    )
                    committer_date = datetime.strptime(
                        committer_date, "%Y-%m-%d %H:%M:%S "
                    )
                except KeyError:
                    pass
                except AttributeError:
                    pass

                # Stores the data into a SQL database
                sql = "INSERT INTO COMMITS (author, author_date, committer, committer_date, commits_url, message, comment_count, comments_url) VALUES (?,?,?,?,?,?,?,?);"
                self.dbCursor.execute(
                    sql,
                    (
                        str(author),
                        str(author_date),
                        str(committer_date),
                        str(committer),
                        str(commits_url),
                        str(message),
                        str(comment_count),
                        str(comments_url),
                    ),
                )
                self.dbConnection.commit()

            # Below checks to see if there are any links related to the data returned
            try:
                foo = self.responseHeaders["Link"]
                if (
                    'rel="next"' not in foo
                ):  # Breaks if there is no rel="next" text in key Link
                    break

                else:
                    bar = foo.split(",")

                    for x in bar:
                        if 'rel="next"' in x:
                            url = x[x.find("<") + 1 : x.find(">")]
                            self.data = self.gha.access_GitHubAPISpecificURL(url=url)
                            self.responseHeaders = self.gha.get_ResponseHeaders()
                            self.parser()  # Recursive
            except KeyError:  # Raises if there is no key Link
                print(self.responseHeaders)
                break
            break
    
    # get author name: self, x -> string (author's name)
    def get_author_name(self, x):
        return self.data[x]["commit"]["author"]["name"]

    def get_committer_name(self, x):
        return self.data[x]["commit"]["committer"]["name"]
    
    def get_message(self, x):
        return self.data[x]["commit"]["message"]

    def get_comment_count(self, x):
        return self.data[x]["commit"]["comment_count"]

    def get_commits_url(self, x):
        return self.data[x]["commit"]["url"]

    def get_comments_url(self, x):
        return self.data[x]["comments_url"]

    def get_author_date(self, x):
        author_date = (
            self.data[x]["commit"]["author"]["date"]
            .replace("T", " ")
            .replace("Z", " ")
        )
        author_date = datetime.strptime(author_date, "%Y-%m-%d %H:%M:%S ")
        return author_date
