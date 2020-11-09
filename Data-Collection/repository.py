from sqlite3 import Connection, Cursor

from requests import Response

from libs.databaseConnector import DatabaseConnector
from libs.githubConnector import GitHubConnector


class Repository:
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
        id = dataset["id"]
        name = dataset["name"]
        owner = dataset["owner"]["login"]
        description = dataset["description"]
        fork = str(dataset["fork"])
        createdAt = dataset["created_at"]
        updatedAt = dataset["updated_at"]
        pushedAt = dataset["pushed_at"]
        size = dataset["size"]
        stars = dataset["stargazers_count"]
        watchers = dataset["watchers_count"]
        language = dataset["language"]
        hasIssues = str(dataset["has_issues"])
        hasProjects = str(dataset["has_projects"])
        hasDownloads = str(dataset["has_downloads"])
        hasWiki = str(dataset["has_wiki"])
        hasPages = str(dataset["has_pages"])
        forks = dataset["forks_count"]
        archived = str(dataset["archived"])
        disabled = str(dataset["disabled"])
        openIssues = dataset["open_issues_count"]
        license = dataset["license"]["name"]
        organization = dataset["organization"]["login"]
        networkCount = dataset["network_count"]
        subscribers = dataset["subscribers_count"]
        private = str(dataset["private"])

        sql = "INSERT OR IGNORE INTO Repository (ID, Name, Owner, Description, Fork, Created_At, Updated_At, Pushed_At, Size, Stars, Watchers, Language, Has_Issues, Has_Projects, Has_Downloads, Has_Wiki, Has_Pages, Forks, Archived, Disabled, Open_Issues, License, Organization, Network_Count, Subscribers, Private) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

        self.connection.executeSQL(
            sql,
            (
                id,
                name,
                owner,
                description,
                fork,
                createdAt,
                updatedAt,
                pushedAt,
                size,
                stars,
                watchers,
                language,
                hasIssues,
                hasProjects,
                hasDownloads,
                hasWiki,
                hasPages,
                forks,
                archived,
                disabled,
                openIssues,
                license,
                organization,
                networkCount,
                subscribers,
                private,
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
