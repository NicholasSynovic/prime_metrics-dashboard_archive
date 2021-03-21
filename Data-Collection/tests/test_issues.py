import os
import unittest

from issues import Issues
from libs.databaseConnector import DatabaseConnector


class Test_Issues(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Test database setup
        cls.dbConnector = DatabaseConnector(databaseFileName="testDB.db")
        cls.dbConnector.createDatabase()
        cls.dbConnector.openDatabaseConnection()
        cls.dbConnector.executeSQL(
            sql="CREATE TABLE Issues (ID INTEGER, Count INTEGER, Title TEXT, Author TEXT, Assignees TEXT, Labels TEXT, Created_At TEXT, Updated_At TEXT, Closed_At TEXT, PRIMARY KEY(ID));"
        )

        # Test data
        cls.testData = {
            0: {
                "id": 0,
                "number": 7357,
                "title": "testTitle",
                "user": {"login": "testAuthLogin"},
                "assignees": {"login": "A1Log", "login": "A2log"},
                "labels": {"name": "testLabel1", "name": "testLabel2"},
                "state": "testState",
                "created_at": "testCreate",
                "updated_at": "testUpdate",
                "pushed_at": "testPush",
            }
        }

        cls.dataComparison = [
            (
                0,
                "testName",
                "testLogin",
                "testPrivate",
                "testFork",
                "testCreate",
                "testUpdate",
                "testPush",
                7357,
                7357,
                7357,
            )
        ]

        # Commit class setup
        cls.issue = Issues(
            dbConnection=cls.dbConnector,
            oauthToken="token",
            repository="repo",
            username="name",
            url="url",
        )

    @classmethod
    def tearDownClass(cls) -> None:
        # close database
        cls.dbConnector.executeSQL("DELETE FROM Issues;")
        cls.dbConnector.commitSQL(databaseConnection=cls.dbConnector.databaseConnection)
        cls.dbConnector.closeDatabaseConnection(
            databaseConnection=cls.dbConnector.databaseConnection
        )

        # delete created file
        os.remove("testDB.db")

    def test_insertData(self):
        self.issue.insertData(dataset=self.testData)
        dataActual = self.dbConnector.selectColumn(table="Issues", column="*")
        print(dataActual)
        self.assertEqual(
            dataActual,
            self.dataComparison,
        )


if __name__ == "__main__":
    unittest.main()
