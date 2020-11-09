from sqlite3 import Connection, Cursor

from assignees import Assignees
from commits import Commits
from libs.cmdLineInterface import arguementHandling
from libs.databaseConnector import DatabaseConnector
from issues import Issues
from comments import Comments


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
        commitsSQL = "CREATE TABLE Commits (SHA TEXT,Commit_Date TEXT, Author TEXT, Message TEXT, Comment_Count INTEGER, PRIMARY KEY(SHA));"

        issuesSQL = "CREATE TABLE Issues (ID INTEGER, Count INTEGER, Title TEXT, Author TEXT, Assignees TEXT, Labels TEXT, Created_At TEXT, Updated_At TEXT, Closed_At TEXT, PRIMARY KEY(ID));"

        assigneesSQL = "CREATE TABLE Assignees (ID INTEGER, Login TEXT, Type TEXT, Site_Admin TEXT, PRIMARY KEY(ID))"

        commentsSQL = "CREATE TABLE Comments (ID INTEGER, Author TEXT, Author_Association TEXT, Message TEXT, Created_At TEXT, Updated_At TEXT, PRIMARY KEY(ID))"

        self.dbConnector.executeSQL(sql=commitsSQL, commit=True)
        self.dbConnector.executeSQL(sql=issuesSQL, commit=True)
        self.dbConnector.executeSQL(sql=assigneesSQL, commit=True)
        self.dbConnector.executeSQL(sql=commentsSQL, commit=True)

    def startDataCollection(self) -> None:
        def _collectData(collector) -> None:
            while True:
                print(
                    """...\tDownloading information from:
   \t{}\n""".format(
                        collector.url
                    )
                )
                data = collector.getData()
                collector.insertData(dataset=data[0])
                if not collector.iterateNext(data[1]):
                    break

        databaseConnection = self.checkForFile()
        self.createFileTablesColumns(dbConnection=databaseConnection)

        commitsCollector = Commits(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
        )

        issueCollector = Issues(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
        )

        assigneeCollector = Assignees(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
        )

        commentCollector = Comments(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
        )

        _collectData(commentCollector)
        _collectData(assigneeCollector)
        _collectData(commitsCollector)
        _collectData(issueCollector)


if __name__ == "__main__":
    cmdLineArgs = arguementHandling()

    prepository = cmdLineArgs.url[0].split()
    print(prepository)

    dc = DataCollection(
        oauthToken=cmdLineArgs.token[0],
        outfile=cmdLineArgs.outfile[0],
        repository=cmdLineArgs.url[0].split("/")[-1],
        username=cmdLineArgs.url[0].split("/")[-2],
    )

    dc.startDataCollection()
