import unittest
import os
from libs.databaseConnector import DatabaseConnector
from repository import Repository
class Test_Repository(unittest.TestCase):
    

    @classmethod
    def setUpClass(cls) -> None:
        #Test database setup
        cls.dbConnector = DatabaseConnector(databaseFileName = "testDB.db")
        cls.dbConnector.createDatabase()
        cls.dbConnector.openDatabaseConnection()
        cls.dbConnector.executeSQL(sql='CREATE TABLE Repository (ID INTEGER, Name TEXT, Owner TEXT, Private TEXT, Fork TEXT, Created_At TEXT, Updated_At TEXT, Pushed_At TEXT, Size INTEGER, Forks INTEGER, Open_Issues INTEGER, PRIMARY KEY(ID))')
        
        #Test data
        cls.testData = {'id': 0, 'name': 'testName',
                        'owner': {'login': 'testLogin'}, 'private': 'testPrivate',
                        'fork': 'testFork', 'created_at': 'testCreate',
                        'updated_at': 'testUpdate', 'pushed_at': 'testPush',
                        'size': 7357, 'forks_count': 7357,
                        'open_issues_count': 7357}
    
        cls.dataComparison = [(0, 'testName', 'testLogin', 'testPrivate', 
                               'testFork', 'testCreate', 'testUpdate', 'testPush', 
                               7357, 7357, 7357)]

        #Commit class setup
        cls.repo = Repository(dbConnection = cls.dbConnector,
                             oauthToken = "token",
                             repository = "repo",
                             username = "name",
                             url = "url")
    
    @classmethod
    def tearDownClass(cls) -> None:
        #close database
        cls.dbConnector.executeSQL('DELETE FROM Repository;')
        cls.dbConnector.commitSQL(databaseConnection = cls.dbConnector.databaseConnection)
        cls.dbConnector.closeDatabaseConnection(databaseConnection = cls.dbConnector.databaseConnection)

        #delete created file
        os.remove('testDB.db')
    
    def test_insertData(self):
        self.repo.insertData(dataset = self.testData)
        dataActual = self.dbConnector.selectColumn(table = "Repository", column = "*")
        self.assertEqual(dataActual, self.dataComparison,)
            


if __name__ == '__main__':
    unittest.main()