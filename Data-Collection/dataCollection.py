from sqlite3 import Connection, Cursor

from libs import *
from commits import Commits


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
        return self.dbConnector.openDatabaseConnection()

    def createFileTablesColumns(self, dbConnection: Connection) -> bool:
        commitsSQL = "CREATE TABLE Commits (SHA TEXT,Commit_Date TEXT, Author TEXT, Message TEXT, Comment_Count INTEGER, PRIMARY KEY(SHA));"

        issuesSQL = "CREATE TABLE Issues (ID TEXT, Count TEXT, Title TEXT, Author TEXT, Assignees TEXT, Labels TEXT, Description TEXT, Created At TEXT, Updated At TEXT, Closed At TEXT, PRIMARY KEY(ID));"

        self.dbConnector.executeSQL(
            sql=commitsSQL, databaseConnection=dbConnection, commit=True
        )
        self.dbConnector.executeSQL(
            sql=issuesSQL, databaseConnection=dbConnection, commit=True
        )

    def startDataCollection(self) -> None:
        databaseConnection = self.checkForFile()
        self.createFileTablesColumns(dbConnection=databaseConnection)

        commitsCollector = Commits(
            dbConnection=databaseConnection,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
        )

        commitsData = commitsCollector.getData()
        commitsCollector.insertData(dataset=commitsData[0])
        commitsCollector.iterateNext(commitsData[1])


dc = DataCollection(
    oauthToken="54a7765ecac4f78aa9cf1edfe060b03509abe26e",
    outfile=r"test.db",
    repository="Metrics-Dashboard",
    username="NicholasSynovic",
)

dc.startDataCollection()
