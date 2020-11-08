# This file creates the tables necessary for data collection as well as all of the columns needed to do so
# This file starts all of the data collection files and insertes the data into the database where it needs to go

# 3: Start collecting data

from datetime import datetime, timedelta
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
        pass


dc = DataCollection(
    oauthToken=10,
    outfile="dicks.db",
    repository="temp",
    username="temp",
)

t = dc.checkForFile()

dc.createFileTablesColumns(t)

c = Commits(
    dbConnection=t,
    oauthToken="1be86e557ba54e7f5edd6b2054ae129d8dfec09d",
    repository="Metrics-Dashboard",
    username="NicholasSynovic",
    page=1,
)

data = c.getData()
c.iteratePages(data[1])
