from sqlite3 import Connection

from branches import Branches
from commits import Commits
from forks import Forks
from issues import Issues
from languages import Languages
from libs.cmdLineInterface import arguementHandling
from libs.databaseConnector import DatabaseConnector
from repository import Repository


class DataCollection:
    def __init__(
        self,
        oauthToken: str,
        outfile: str,
        repository: str,
        username: str,
    ) -> None:
        self.file = outfile
        self.repository = repository
        self.token = oauthToken
        self.username = username

        self.dbConnector = DatabaseConnector(databaseFileName=outfile)

    def checkForFile(self) -> Connection:
        self.dbConnector.createDatabase()
        self.dbConnector.openDatabaseConnection()

    def createFileTablesColumns(self, dbConnection: Connection) -> bool:

        branchesSQL = (
            "CREATE TABLE Branches (ID INTEGER, Name TEXT, SHA TEXT, PRIMARY KEY(ID))"
        )

        commitsSQL = "CREATE TABLE Commits (ID INTEGER, SHA TEXT, Branch TEXT, Author TEXT, Commit_Date TEXT, Tree_SHA TEXT, Comment_Count INTEGER, PRIMARY KEY(ID));"

        forksSQL = "CREATE TABLE Forks (ID TEXT, Name TEXT, Owner TEXT, Created_At TEXT, Updated_At TEXT, Pushed_At TEXT, Size INTEGER, Forks INTEGER, Open_Issues INTEGER, PRIMARY KEY(ID))"

        issuesSQL = "CREATE TABLE Issues (ID INTEGER, Count INTEGER, Title TEXT, Author TEXT, Assignees TEXT, Labels TEXT, Created_At TEXT, Updated_At TEXT, Closed_At TEXT, PRIMARY KEY(ID));"

        languagesSQL = "CREATE TABLE Languages (ID INTEGER, Language TEXT, Bytes_of_Code INTEGER, PRIMARY KEY(ID))"

        repositorySQL = "CREATE TABLE Repository (ID INTEGER, Name TEXT, Owner TEXT, Private TEXT, Fork TEXT, Created_At TEXT, Updated_At TEXT, Pushed_At TEXT, Size INTEGER, Forks INTEGER, Open_Issues INTEGER, PRIMARY KEY(ID))"

        self.dbConnector.executeSQL(sql=branchesSQL, commit=True)
        self.dbConnector.executeSQL(sql=commitsSQL, commit=True)
        self.dbConnector.executeSQL(sql=forksSQL, commit=True)
        self.dbConnector.executeSQL(sql=issuesSQL, commit=True)
        self.dbConnector.executeSQL(sql=languagesSQL, commit=True)
        self.dbConnector.executeSQL(sql=repositorySQL, commit=True)

    def startDataCollection(self) -> None:
        def _collectData(collector) -> None:
            while True:
                # print("...\tDownloading information")
                data = collector.getData()
                collector.insertData(dataset=data[0])
                if not collector.iterateNext(data[1]):
                    break

        databaseConnection = self.checkForFile()
        self.createFileTablesColumns(dbConnection=databaseConnection)

        branchCollector = Branches(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
            url="https://api.github.com/repos/{}/{}/branches?per_page=100&page={}",
        )

        forksCollector = Forks(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
            url="https://api.github.com/repos/{}/{}/forks?per_page=100&page={}",
        )

        issuesCollector = Issues(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
            url="https://api.github.com/repos/{}/{}/issues?state=all&per_page=100&page={}",
        )

        languageCollector = Languages(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
            url="https://api.github.com/repos/{}/{}/languages?per_page=100&page={}",
        )

        repositoryCollector = Repository(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
            url="https://api.github.com/repos/{}/{}?per_page=100&page={}",
        )

        _collectData(languageCollector)  # One request only
        _collectData(repositoryCollector)  # One request only
        _collectData(branchCollector)  # Estimated < 10 requests
        _collectData(forksCollector)  # Estimated < 10 requests
        _collectData(issuesCollector)  # Estimated < 20 requests

        branchList = self.dbConnector.selectColumn(table="Branches", column="SHA")

        for branch in branchList:
            commitsCollector = Commits(
                dbConnection=self.dbConnector,
                oauthToken=self.token,
                repository=self.repository,
                sha=branch[0],
                username=self.username,
                url="https://api.github.com/repos/{}/{}/commits?per_page=100&page={}&sha={}",
            )
            _collectData(commitsCollector)  # Estimated to have the most requests


if __name__ == "__main__":
    cmdLineArgs = arguementHandling()

    dc = DataCollection(
        oauthToken=cmdLineArgs.token[0],
        outfile=cmdLineArgs.outfile[0],
        repository=cmdLineArgs.url[0].split("/")[-1],
        username=cmdLineArgs.url[0].split("/")[-2],
    )

    dc.startDataCollection()
