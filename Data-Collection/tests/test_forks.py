import os
import unittest

from forks import Forks
from libs.databaseConnector import DatabaseConnector


class Test_Forks(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Test database setup
        cls.dbConnector = DatabaseConnector(databaseFileName="testForksDB.db")
        cls.dbConnector.createDatabase()
        cls.dbConnector.openDatabaseConnection()
        cls.dbConnector.executeSQL(
            sql="CREATE TABLE Forks (ID TEXT, Name TEXT, Owner TEXT, Created_At TEXT, Updated_At TEXT, Pushed_At TEXT, Size INTEGER, Forks INTEGER, Open_Issues INTEGER, PRIMARY KEY(ID));"
        )

        # Test data
        cls.testData = {
            0: {
                "id": "testID",
                "name": "testName",
                "owner": {"login": "testLogin"},
                "created_at": "testCreate",
                "updated_at": "testUpdate",
                "pushed_at": "testPush",
                "size": 7357,
                "forks_count": 7357,
                "open_issues_count": 7357,
            }
        }

        cls.dataComparison = [
            (
                "testID",
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
        cls.forks = Forks(
            dbConnection=cls.dbConnector,
            oauthToken="token",
            repository="repo",
            username="name",
            url="url",
        )

    @classmethod
    def tearDownClass(cls) -> None:
        # close database
        cls.dbConnector.executeSQL("DELETE FROM Forks;")
        cls.dbConnector.commitSQL(databaseConnection=cls.dbConnector.databaseConnection)
        cls.dbConnector.closeDatabaseConnection(
            databaseConnection=cls.dbConnector.databaseConnection
        )

        # delete created file
        os.remove("testForksDB.db")

    def test_insertData(self):
        self.forks.insertData(dataset=self.testData)
        dataActual = self.dbConnector.selectColumn(table="Forks", column="*")
        self.assertEqual(
            dataActual,
            self.dataComparison,
        )


if __name__ == "__main__":
    unittest.main()
