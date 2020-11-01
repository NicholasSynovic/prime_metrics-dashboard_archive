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
                
                # retrieve data from github dict 
                author         = self.get_github_data(self.get_author_name,    x)
                committer      = self.get_github_data(self.get_committer_name, x)
                message        = self.get_github_data(self.get_message,        x)
                comment_count  = self.get_github_data(self.get_comment_count,  x)
                commits_url    = self.get_github_data(self.get_commits_url,    x)
                comments_url   = self.get_github_data(self.get_commits_url,    x)
                author_date    = self.get_github_data(self.get_author_date,    x) 
                committer_date = self.get_github_data(self.get_committer_date, x) 

                # Stores the data into a SQL database
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

            # Below checks to see if there are any links related to the data returned
            try:
                key_link = self.responseHeaders["Link"]
                if (
                    'rel="next"' not in key_link
                ):  # Breaks if there is no rel="next" text in key Link
                    break
                else:
                    bar = key_link.split(",")
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

    def get_author_name(self, x) -> str:
        """
        purpose: get the author's name 
        arg1 :  x -> a key in the of the main class attribute self.data
        return type: string 
        """
        return self.data[x]["commit"]["author"]["name"]

    def get_committer_name(self, x) -> str:
        """
        purpose: get the committer's name 
        arg1 :  x -> a key in the of the main class attribute self.data
        return type: string 
        """
        return self.data[x]["commit"]["committer"]["name"]
    
    def get_message(self, x) -> str:
        """
        purpose: get the message attached to the commit 
        arg1 :  x -> a key in the of the main class attribute self.data
        return type: string 
        """
        return self.data[x]["commit"]["message"]

    def get_comment_count(self, x) -> int:
        """
        purpose: get the number of comments  
        arg1 :  x -> a key in the of the main class attribute self.data
        return type: int 
        """
        return self.data[x]["commit"]["comment_count"]

    def get_commits_url(self, x) -> str:
        """
        purpose: get the commit's url  
        arg1 :  x -> a key in the of the main class attribute self.data
        return type: string (url) 
        """
        return self.data[x]["commit"]["url"]

    def get_comments_url(self, x) -> str:
        """
        purpose: get the comments's url 
        arg1 :  x -> a key in the of the main class attribute self.data
        return type: string (url)
        """
        return self.data[x]["comments_url"]

    def get_author_date(self, x) -> datetime:
        """
        purpose: get the author date of the commit as well as cleaning up the date format 
        arg1 :  x -> a key in the of the main class attribute self.data
        return type: datetime object 
        """
        author_date = (
            self.data[x]["commit"]["author"]["date"]
            .replace("T", " ")
            .replace("Z", " ")
        )
        author_date = datetime.strptime(author_date, "%Y-%m-%d %H:%M:%S ")
        return author_date
    
    def get_committer_date(self, x) -> datetime:
        """
        purpose: get the commiter date of the commit as well as cleaning up the date format 
        arg1 :  x -> a key in the of the main class attribute self.data
        return type: datetime object 
        """
        committer_date = (
            self.data[x]["commit"]["committer"]["date"]
            .replace("T", " ")
            .replace("Z", " ")
        )
        committer_date = datetime.strptime(
            committer_date, "%Y-%m-%d %H:%M:%S "
        )
        return committer_date


    def get_github_data(self, other_func, x):
        """
        purpose: a higher order function to try obtaining the data from the class function and return NA if not obtainable 
        arg1 :  other_func -> another function to perform 
        arg2 :  x -> a key in the of the main class attribute self.data, will act as a paramter to arg1
        return type: datetime object 
        """
        try:
            return_string = other_func(x)
        except KeyError:
            return_string = "NA"
        except AttributeError:
            return_string = "NA"
        return return_string
    
