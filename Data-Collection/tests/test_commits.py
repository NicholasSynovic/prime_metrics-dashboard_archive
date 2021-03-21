import unittest
import os
from libs.databaseConnector import DatabaseConnector
from commits import Commits
class Test_Commits(unittest.TestCase):
    

    @classmethod
    def setUpClass(cls) -> None:
        #Test database setup
        cls.dbConnector = DatabaseConnector(databaseFileName = "testDB.db")
        cls.dbConnector.createDatabase()
        cls.dbConnector.openDatabaseConnection()
        cls.dbConnector.executeSQL(sql='CREATE TABLE Commits (ID INTEGER, SHA TEXT, Branch TEXT, Author TEXT, Commit_Date TEXT, Tree_SHA TEXT, Comment_Count INTEGER, PRIMARY KEY(ID));')
        
        #Test data
        cls.testData = {0: {'sha': 'testSHA', 'commit': {
                    'author': {'name': 'testName'}, 
                    'committer': {'date': 'testDate'}, 
                    'tree': {'sha': 'testTreeSHA'}, 
                    'comment_count': '7357'}}}
        cls.dataComparison = [(0, 'testSHA', 'sha', 'testName', 'testDate', 'testTreeSHA', 7357)]

        #Commit class setup
        cls.commit = Commits(dbConnection = cls.dbConnector,
                             oauthToken = "token",
                             repository = "repo",
                             sha = "sha",
                             username = "name",
                             url = "url")
    
    @classmethod
    def tearDownClass(cls) -> None:
        #close database
        cls.dbConnector.executeSQL('DELETE FROM Commits;')
        cls.dbConnector.commitSQL(databaseConnection = cls.dbConnector.databaseConnection)
        cls.dbConnector.closeDatabaseConnection(databaseConnection = cls.dbConnector.databaseConnection)

        #delete created file
        os.remove('testDB.db')
    
    def test_insertData(self):
        self.commit.insertData(dataset = self.testData)
        dataActual = self.dbConnector.selectColumn(table = "Commits", column = "*")

        self.assertEqual(dataActual, self.dataComparison)
            


if __name__ == '__main__':
    unittest.main()