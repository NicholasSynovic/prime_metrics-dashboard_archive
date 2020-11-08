import json
import sys
import unittest
from json import load

from requests import Response

sys.path.append("../")

from commits import Commits
from libs.databaseConnector import DatabaseConnector
from libs.githubConnector import GitHubConnector


dbConnection = DatabaseConnector(databaseFileName="temp.db")
dbConnection.createDatabase()
dbConnection.openDatabaseConnection()
commitsSQL = "CREATE TABLE Commits (SHA TEXT,Commit_Date TEXT, Author TEXT, Message TEXT, Comment_Count INTEGER, PRIMARY KEY(SHA));"
dbConnection.executeSQL(sql=commitsSQL, commit=True)

with open("jsonResponses.json", "r") as file:
    commitsResponse = load(file)["commits"]
    file.close()

with open("jsonResponseHeaders.json", "r") as file:
    commitsResponseHeaders = load(file)["commits"]
    file.close()

commitsCollector = Commits(
    dbConnection=dbConnection,
    oauthToken="CHANGE ME",
    repository="Metrics-Dashboard",
    username="SoftwareSystemsLaboratory",
)


class TestCommits(unittest.TestCase):
    def test_Commits(self):
        assert commitsCollector.currentPage == 1
        assert commitsCollector.repository == "Metrics-Dashboard"
        assert commitsCollector.username == "SoftwareSystemsLaboratory"

    def test_getData(self):
        data = commitsCollector.getData()
        assert data[1].status_code == 200
        self.assertIsInstance(data[0], list)

    def test_insertData(self):
        commitsCollector.insertData(dataset=commitsResponse)

    # TODO: Create a proper test for this function
    # def test_IterateNext(self):
