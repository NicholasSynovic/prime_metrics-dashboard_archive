from sqlite3 import Connection, Cursor

from requests import Response

from libs.databaseConnector import DatabaseConnector
from libs.githubConnector import GitHubConnector


class Milestones:
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
        self.url = "https://api.github.com/repos/{}/{}".format(
            username, repository, self.currentPage
        )

    def getData(self) -> list:
        response = self.githubConnection.openConnection(url=self.url)
        return [response.json(), response]

    def insertData(self, dataset: dict) -> None:
        for dataPoint in range(len(dataset)):
            id = dataset[dataPoint]["id"]
            number = dataset[dataPoint]["number"]
            state = dataset[dataPoint]["state"]
            title = dataset[dataPoint]["title"]
            description = dataset[dataPoint]["description"]
            creator = dataset[dataPoint]["creator"]["login"]
            openIssues = dataset[dataPoint]["open_issues"]
            closedIssues = dataset[dataPoint]["closed_issues"]
            createdAt = dataset[dataPoint]["created_at"]
            updatedAt = dataset[dataPoint]["updated_at"]
            closedAt = dataset[dataPoint]["closed_at"]
            dueOn = dataset[dataPoint]["due_on"]

            sql = "INSERT OR IGNORE INTO Milestones (ID, Number, State, Title, Description , Creator, Open_Issues, Closed_Issues, Created_At, Updated_At, Closed_At, Due_On) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"

            self.connection.executeSQL(
                sql,
                (
                    id,
                    number,
                    state,
                    title,
                    description,
                    creator,
                    openIssues,
                    closedIssues,
                    createdAt,
                    updatedAt,
                    closedAt,
                    dueOn,
                ),
                True,
            )

    def iterateNext(self, responseHeaders: Response) -> bool:
        if (
            self.githubConnection.parseResponseHeaders(responseHeaders)["Last-Page"]
            == -1
        ):
            return False

        self.currentPage += 1
        self.url = "https://api.github.com/repos/{}/{}/".format(
            self.username, self.repository, self.currentPage
        )
        return True
