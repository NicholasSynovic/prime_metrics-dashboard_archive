# This file is meant to calculate the total size of every branch in a project at a certain period of time
# This file is meant to calculate the total size of the project at a certain period of time


from libs.databaseConnector import DatabaseConnector
from sqlite3 import Connection


class ProjectSize:
    def __init__(self, database: str, time: str) -> None:
        self.dbConnector = DatabaseConnector(databaseFileName=database)
        self.time = time
        self.connection = None

    def checkForFile(self) -> Connection:
        self.dbConnector.createDatabase()
        self.dbConnector.openDatabaseConnection()
        self.connection = self.dbConnector.databaseConnection

    def calculateBranchSizes(self) -> dict:
        def _getCommits(branch: str):
            return self.connection.execute(
                "SELECT Commit_SHA FROM Commits WHERE Branch = '{}'".format(branch)
            ).fetchall()

        branches = set()
        commitsPerBranch = {}

        for branch in self.dbConnector.selectColumn("Branches", "name"):
            branches.add(branch[0])

        for branch in branches:
            _getCommits(branch)

            commitsPerBranch[branch] = None


ps = ProjectSize("ChessJS.db", "Hello World")
ps.checkForFile()
ps.calculateBranchSizes()
