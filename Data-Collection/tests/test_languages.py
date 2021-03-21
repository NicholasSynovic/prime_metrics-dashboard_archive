import os
import unittest

from languages import Languages
from libs.databaseConnector import DatabaseConnector


class Test_Languages(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Test database setup
        cls.dbConnector = DatabaseConnector(databaseFileName="testLanguageDB.db")
        cls.dbConnector.createDatabase()
        cls.dbConnector.openDatabaseConnection()
        cls.dbConnector.executeSQL(
            sql="CREATE TABLE Languages (ID INTEGER, Language TEXT, Bytes_of_Code INTEGER, PRIMARY KEY(ID))"
        )

        # Test data
        cls.testData = {"testLang1": 7357, "testLang2": 5}

        cls.dataComparison = [(0, "testLang1", 7357), (1, "testLang2", 5)]

        # Commit class setup
        cls.lang = Languages(
            dbConnection=cls.dbConnector,
            oauthToken="token",
            repository="repo",
            username="name",
            url="url",
        )

    @classmethod
    def tearDownClass(cls) -> None:
        # close database
        cls.dbConnector.executeSQL("DELETE FROM Languages;")
        cls.dbConnector.commitSQL(databaseConnection=cls.dbConnector.databaseConnection)
        cls.dbConnector.closeDatabaseConnection(
            databaseConnection=cls.dbConnector.databaseConnection
        )

        # delete created file
        os.remove("testLanguageDB.db")

    def test_insertData(self):
        self.lang.insertData(dataset=self.testData)
        dataActual = self.dbConnector.selectColumn(table="Languages", column="*")
        self.assertEqual(dataActual, self.dataComparison)


if __name__ == "__main__":
    unittest.main()
