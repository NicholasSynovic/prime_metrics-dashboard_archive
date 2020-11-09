from sqlite3 import Connection, Cursor

from assignees import Assignees
from comments import Comments
from commits import Commits
from issueEvents import IssueEvents
from issues import Issues
from labels import Labels
from libs.cmdLineInterface import arguementHandling
from libs.databaseConnector import DatabaseConnector
from milestones import Milestones


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
        milestonesSQL = "CREATE TABLE Milestones (ID INTEGER, Number INTEGER, State TEXT, Title TEXT, Description TEXT, Creator TEXT, Open_Issues INTEGER, Closed_Issues INTEGER, Created_At TEXT, Updated_At TEXT, Closed_At TEXT, Due_On TEXT, PRIMARY KEY(ID))"

        labelsSQL = "CREATE TABLE Labels (ID INTEGER, Name TEXT, Description TEXT, Color TEXT, Default_Label TEXT, PRIMARY KEY(ID))"

        issueEventsSQL = "CREATE TABLE Issue_Events (ID INTEGER, Actor TEXT, Type TEXT, Site_Admin TEXT, Event TEXT, Assignee TEXT, Assigner TEXT, Created_At TEXT, PRIMARY KEY(ID))"

        commitsSQL = "CREATE TABLE Commits (SHA TEXT,Commit_Date TEXT, Author TEXT, Message TEXT, Comment_Count INTEGER, PRIMARY KEY(SHA));"

        issuesSQL = "CREATE TABLE Issues (ID INTEGER, Count INTEGER, Title TEXT, Author TEXT, Assignees TEXT, Labels TEXT, Created_At TEXT, Updated_At TEXT, Closed_At TEXT, PRIMARY KEY(ID));"

        assigneesSQL = "CREATE TABLE Assigness (ID INTEGER, Login TEXT, Type TEXT, Site_Admin TEXT, PRIMARY KEY(ID))"

        commentsSQL = "CREATE TABLE Comments (ID INTEGER, Author TEXT, Author_Association TEXT, Message TEXT, Created_At TEXT, Updated_At TEXT, PRIMARY KEY(ID))"

        self.dbConnector.executeSQL(sql=milestonesSQL, commit=True)
        self.dbConnector.executeSQL(sql=labelsSQL, commit=True)
        self.dbConnector.executeSQL(sql=issueEventsSQL, commit=True)
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

        milestoneCollector = Milestones(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
        )

        labelCollector = Labels(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
        )

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

        issueEventCollector = IssueEvents(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
        )

        _collectData(milestoneCollector)
        _collectData(labelCollector)
        _collectData(issueEventCollector)
        _collectData(commentCollector)
        _collectData(assigneeCollector)
        _collectData(commitsCollector)
        _collectData(issueCollector)


if __name__ == "__main__":
    cmdLineArgs = arguementHandling()

    dc = DataCollection(
        oauthToken=cmdLineArgs.token[0],
        outfile=cmdLineArgs.outfile[0],
        repository=cmdLineArgs.url[0].split("/")[-1],
        username=cmdLineArgs.url[0].split("/")[-2],
    )

    dc.startDataCollection()
