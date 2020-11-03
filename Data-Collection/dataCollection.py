from datetime import datetime, timedelta
from sqlite3 import Connection, Cursor

# import commits
from libs import *


class Main:
    def __init__(
        self,
        username: str = None,
        repository: str = None,
        token: str = None,
        tokenList: list = None,
        cursor: Cursor = None,
        connection: Connection = None,
    ) -> None:

        self.githubUser = username
        self.githubRepo = repository
        self.githubToken = token
        self.githubTokenList = tokenList
        self.dbCursor = cursor
        self.dbConnection = connection
        self.data = None
        self.gha = None

    def program(self) -> None:
        self.set_Data(endpoint="")  # %%

        self.set_Data(endpoint="commits")
        Commits.Logic(
            gha=self.gha,
            data=self.data[0],
            responseHeaders=self.data[1],
            cursor=self.dbCursor,
            connection=self.dbConnection,
        ).parser()

        self.dbCursor.execute("SELECT committer_date FROM COMMITS;")
        date_rows = self.dbCursor.fetchall()

        total_times = []
        total_time_differences = []
        for row in date_rows:
            date = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            total_times.append(date)

        if len(total_times) >= 2:
            for t in range(len(total_times) - 1):
                time_difference = abs(total_times[t] - total_times[t + 1])
                total_time_differences.append(time_difference.total_seconds())

            value = str(sum(total_time_differences) / len(total_time_differences))
        else:
            value = "N/A"

        calc_name = "Average Time Between Commits (secs)"

        sql = "INSERT INTO COMMITS_CALCULATIONS (calc_name, value) VALUES (?,?);"
        self.dbCursor.execute(
            sql,
            (str(calc_name), str(value)),
        )

        self.dbConnection.commit()

    def generate_DateTimeList(self, rCDT: datetime) -> list:
        dates_in_specific_format = []
        today = datetime.today()
        if rCDT.strftime("%Y-%m-%d") == today.strftime("%Y-%m-%d"):
            dates_in_specific_format.append(str(today))
        else:
            dates_in_specific_format.append(str(today))
            while today > rCDT:
                today = today - timedelta(days=1)
                dates_in_specific_format.append(str(today))
        return dates_in_specific_format

    def get_Data(self) -> dict:
        return self.data

    def get_DbConnection(self) -> Connection:
        return self.dbConnection

    def get_DbCursor(self) -> Cursor:
        return self.dbCursor

    def get_GitHubRepo(self) -> str:
        return self.githubRepo

    def get_GitHubToken(self) -> str:
        return self.githubToken

    def get_GitHubUser(self) -> str:
        """
        Returns the class variable githubUser.
        """
        return self.githubUser

    def set_Data(self, endpoint: str = "/") -> None:
        endpoint = endpoint.lower()
        self.gha = GitHubAPI(
            username=self.githubUser,
            repository=self.githubRepo,
            token=self.githubToken,
            tokenList=self.githubTokenList,
        )
        if endpoint == "commits":
            self.data = [
                self.gha.access_GitHubRepoCommits(),
                self.gha.get_ResponseHeaders(),
            ]
        elif endpoint == "issues":
            self.data = [
                self.gha.access_GitHubRepoIssues(),
                self.gha.get_ResponseHeaders(),
            ]
        elif endpoint == "pulls":
            self.data = [
                self.gha.access_GitHubRepoPulls(),
                self.gha.get_ResponseHeaders(),
            ]
        elif endpoint == "":
            self.data = [
                self.gha.access_GitHubAPISpecificEndpoint(endpoint=endpoint),
                self.gha.get_ResponseHeaders(),
            ]
        elif endpoint[0] == "/":
            self.data = [
                self.gha.access_GitHubAPISpecificEndpoint(endpoint=endpoint),
                self.gha.get_ResponseHeaders(),
            ]
        else:
            self.data = [
                self.gha.access_GitHubAPISpecificURL(url=endpoint),
                self.gha.get_ResponseHeaders(),
            ]
