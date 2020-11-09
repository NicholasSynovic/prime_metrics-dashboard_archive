from sqlite3 import Connection, Cursor

from requests import Response

from libs.databaseConnector import DatabaseConnector
from libs.githubConnector import GitHubConnector


class IssueEvents:
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
        self.url = "https://api.github.com/repos/{}/{}/issues/events?per_page=100&page={}".format(
            username, repository, self.currentPage
        )

    def getData(self) -> list:
        response = self.githubConnection.openConnection(url=self.url)
        return [response.json(), response]

    def insertData(self, dataset: dict) -> None:
        for dataPoint in range(len(dataset)):
            id = dataset[dataPoint]["id"]
            actor = dataset[dataPoint]["actor"]["login"]
            actorType = dataset[dataPoint]["actor"]["type"]
            siteAdmin = str(dataset[dataPoint]["actor"]["site_admin"])
            event = dataset[dataPoint]["event"]
            try:
                assignee = dataset[dataPoint]["assignee"]["login"]
            except KeyError:
                assignee = "N/A"
            try:
                assigner = dataset[dataPoint]["assigner"]["login"]
            except KeyError:
                assigner = "N/A"
            createdAt = dataset[dataPoint]["created_at"]

            sql = "INSERT OR IGNORE INTO Issue_Events (ID, Actor, Type, Site_Admin, Event, Assignee, Assigner, Created_At) VALUES (?,?,?,?,?,?,?,?);"

            self.connection.executeSQL(
                sql,
                (
                    id,
                    actor,
                    actorType,
                    siteAdmin,
                    event,
                    assignee,
                    assigner,
                    createdAt,
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
        self.url = "https://api.github.com/repos/{}/{}/issues/events?per_page=100&page={}".format(
            self.username, self.repository, self.currentPage
        )
        return True
