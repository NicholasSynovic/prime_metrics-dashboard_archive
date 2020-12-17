from sqlite3 import Connection
from libs.cmdLineInterface import arguementHandling
from libs.databaseConnector import DatabaseConnector
from repository import Repository


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

        repositorySQL = "CREATE TABLE Repository (ID INTEGER, Name TEXT, Owner TEXT, Private TEXT, Fork TEXT, Created_At TEXT, Updated_At TEXT, Pushed_At TEXT, Size INTEGER, Forks INTEGER, Open_Issues INTEGER, PRIMARY KEY(ID))"

        self.dbConnector.executeSQL(sql=repositorySQL, commit=True)

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

        repositoryCollector = Repository(
            dbConnection=self.dbConnector,
            oauthToken=self.token,
            repository=self.repository,
            username=self.username,
            url="https://api.github.com/repos/{}/{}?per_page=100&page={}",
        )

        _collectData(repositoryCollector)


if __name__ == "__main__":
    cmdLineArgs = arguementHandling()

    dc = DataCollection(
        oauthToken=cmdLineArgs.token[0],
        outfile=cmdLineArgs.outfile[0],
        repository=cmdLineArgs.url[0].split("/")[-1],
        username=cmdLineArgs.url[0].split("/")[-2],
    )

    dc.startDataCollection()
