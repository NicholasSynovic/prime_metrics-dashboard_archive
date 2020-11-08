from sqlite3 import Connection, Cursor

from requests import Response

from libs import *


class OpenIssues:
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
            "https://api.github.com/repos/{}/{}/issues?per_page=100&page={}".format(
                username, repository, self.currentPage
            )
        )

    def getData(self) -> list:
        response = self.githubConnection.openConnection(url=self.url)
        return [response.json(), response]

    def insertData(self, dataset: dict) -> None:
        def _labelCollection(
            index: int,
        ) -> str:
            labelNames = []
            for label in dataset[index]["labels"]:
                labelNames.append(label["name"])
            return ", ".join(labelNames)

        def _asigneeCollection(
            index: int,
        ) -> str:
            labelNames = []
            for assignee in dataset[index]["assignees"]:
                labelNames.append(assignee["login"])
            return ", ".join(labelNames)

        for dataPoint in range(len(dataset)):
            print
            id = dataset[dataPoint]["id"]
            count = dataset[dataPoint]["number"]
            title = dataset[dataPoint]["title"]
            author = dataset[dataPoint]["user"]["login"]
            assignees = _asigneeCollection(index=dataPoint)
            labels = _labelCollection(index=dataPoint)
            createdAt = dataset[dataPoint]["created_at"]
            updatedAt = dataset[dataPoint]["updated_at"]
            closedAt = dataset[dataPoint]["closed_at"]

            sql = "INSERT OR IGNORE INTO ISSUES (ID, Count, Title, Author, Assignees, Labels, Created_At, Updated_At, Closed_At) VALUES (?,?,?,?,?,?,?,?,?);"

            self.connection.executeSQL(
                sql,
                (
                    id,
                    count,
                    title,
                    author,
                    assignees,
                    labels,
                    createdAt,
                    updatedAt,
                    closedAt,
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
        self.url = (
            "https://api.github.com/repos/{}/{}/issues?per_page=100&page={}".format(
                self.username, self.repository, self.currentPage
            )
        )
        return True
