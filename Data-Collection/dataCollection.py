from sqlite3 import Connection

from assignees import Assignees
from branches import Branches
from collaborators import Collaborators
from communityMetrics import CommunityMetrics
from issueComments import IssueComments
from commits import Commits
from contributors import Contributors
from issueEvents import IssueEvents
from issues import Issues
from labels import Labels
from languages import Languages
from libs.cmdLineInterface import arguementHandling
from libs.databaseConnector import DatabaseConnector
from milestones import Milestones
from repository import Repository
from tags import Tags
from teams import Teams


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

        assigneesSQL = "CREATE TABLE Assigness (ID INTEGER, Login TEXT, Type TEXT, Site_Admin TEXT, PRIMARY KEY(ID))"

        branchesSQL = "CREATE TABLE Branches (ID INTEGER, Name TEXT, Commit_SHA TEXT, PRIMARY KEY(ID))"

        collaboratorsSQL = "CREATE TABLE Collaborators (ID INTEGER, Login TEXT, Type TEXT, Site_Admin TEXT, Can_Pull TEXT, Can_Push TEXT, Is_Admin TEXT, PRIMARY KEY(ID))"

        commentsSQL = "CREATE TABLE Comments (ID INTEGER, Author TEXT, Author_Association TEXT, Message TEXT, Created_At TEXT, Updated_At TEXT, PRIMARY KEY(ID))"

        commitsSQL = "CREATE TABLE Commits (SHA TEXT, Commit_Date TEXT, Author TEXT, Message TEXT, Comment_Count INTEGER, PRIMARY KEY(SHA));"

        contributorsSQL = "CREATE TABLE Contributors (ID TEXT, Login TEXT, Type TEXT, Site_Admin TEXT, Contributions TEXT, PRIMARY KEY(ID))"

        issuesSQL = "CREATE TABLE Issues (ID INTEGER, Count INTEGER, Title TEXT, Author TEXT, Assignees TEXT, Labels TEXT, Created_At TEXT, Updated_At TEXT, Closed_At TEXT, PRIMARY KEY(ID));"

        issueEventsSQL = "CREATE TABLE Issue_Events (ID INTEGER, Actor TEXT, Type TEXT, Site_Admin TEXT, Event TEXT, Assignee TEXT, Assigner TEXT, Created_At TEXT, PRIMARY KEY(ID))"

        labelsSQL = "CREATE TABLE Labels (ID INTEGER, Name TEXT, Description TEXT, Color TEXT, Default_Label TEXT, PRIMARY KEY(ID))"

        languagesSQL = "CREATE TABLE Languages (ID INTEGER, Language TEXT, Bytes_of_Code INTEGER, PRIMARY KEY(ID))"

        milestonesSQL = "CREATE TABLE Milestones (ID INTEGER, Number INTEGER, State TEXT, Title TEXT, Description TEXT, Creator TEXT, Open_Issues INTEGER, Closed_Issues INTEGER, Created_At TEXT, Updated_At TEXT, Closed_At TEXT, Due_On TEXT, PRIMARY KEY(ID))"

        repositorySQL = "CREATE TABLE Repository (ID INTEGER, Name TEXT, Owner TEXT, Description TEXT, Fork TEXT, Created_At TEXT, Updated_At TEXT, Pushed_At TEXT, Size INTEGER, Stars INTEGER, Watchers INTEGER, Language TEXT, Has_Issues TEXT, Has_Projects TEXT, Has_Downloads TEXT, Has_Wiki TEXT, Has_Pages TEXT, Forks INTEGER, Archived TEXT, Disabled TEXT, Open_Issues INTEGER, License TEXT, Organization TEXT, Network_Count INTEGER, Subscribers INTEGER, Private TEXT, PRIMARY KEY(ID))"

        tagsSQL = "CREATE TABLE Tags (Node_ID TEXT, Name TEXT, PRIMARY KEY(Node_ID))"

        teamsSQL = "CREATE TABLE Teams (ID INTEGER, Name TEXT, Description TEXT, Privacy TEXT, Permission TEXT, Parent TEXT, PRIMARY KEY(ID))"

        self.dbConnector.executeSQL(sql=assigneesSQL, commit=True)
        self.dbConnector.executeSQL(sql=branchesSQL, commit=True)
        self.dbConnector.executeSQL(sql=collaboratorsSQL, commit=True)
        self.dbConnector.executeSQL(sql=commentsSQL, commit=True)
        self.dbConnector.executeSQL(sql=commitsSQL, commit=True)
        self.dbConnector.executeSQL(sql=contributorsSQL, commit=True)
        self.dbConnector.executeSQL(sql=issuesSQL, commit=True)
        self.dbConnector.executeSQL(sql=issueEventsSQL, commit=True)
        self.dbConnector.executeSQL(sql=labelsSQL, commit=True)
        self.dbConnector.executeSQL(sql=languagesSQL, commit=True)
        self.dbConnector.executeSQL(sql=milestonesSQL, commit=True)
        self.dbConnector.executeSQL(sql=repositorySQL, commit=True)
        self.dbConnector.executeSQL(sql=tagsSQL, commit=True)
        self.dbConnector.executeSQL(sql=teamsSQL, commit=True)

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

        assigneeCollector = Assignees(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
        )

        branchCollector = Branches(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
        )

        collaboratorCollector = Collaborators(
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

        commitsCollector = Commits(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
        )

        contributorCollector = Contributors(
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

        issueEventCollector = IssueEvents(
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

        languageCollector = Languages(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
        )

        milestoneCollector = Milestones(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
        )

        repositoryCollector = Repository(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
        )

        tagCollector = Tags(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
        )

        teamCollector = Teams(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
        )

        # _collectData(assigneeCollector)
        # _collectData(branchCollector)
        _collectData(collaboratorCollector)
        # _collectData(commentCollector)
        # _collectData(commitsCollector)
        # _collectData(contributorCollector)
        # _collectData(issueCollector)
        # _collectData(issueEventCollector)
        # _collectData(labelCollector)
        # _collectData(languageCollector)
        # _collectData(milestoneCollector)
        # _collectData(repositoryCollector)
        # _collectData(tagCollector)
        # _collectData(teamCollector)


if __name__ == "__main__":
    cmdLineArgs = arguementHandling()

    dc = DataCollection(
        oauthToken=cmdLineArgs.token[0],
        outfile=cmdLineArgs.outfile[0],
        repository=cmdLineArgs.url[0].split("/")[-1],
        username=cmdLineArgs.url[0].split("/")[-2],
    )

    dc.startDataCollection()
