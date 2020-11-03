import sqlite3
from sqlite3 import Connection, Cursor


class DatabaseConnector:
    def __init__(self, fileName: str = "DefectDensity.db") -> None:
        self.fileName = fileName
        self.filePath = "metrics/{}".format(fileName)

    def createDatabase(self) -> bool:
        try:
            with open(self.filePath, "r") as database:
                database.close()
            return False
        except FileNotFoundError:
            with open(self.filePath, "w") as database:
                database.close()
            return True

    def openDatabaseConnection(self) -> list:
        databaseConnection = sqlite3.connect(self.filePath)
        return [databaseConnection, self.filePath]

    def executeSQL(
        self,
        sql: str,
        databaseConnection: list,
        options: tuple = None,
        commit: bool = False,
    ) -> bool:
        connection = databaseConnection[0]

        if options is None:
            connection.execute(sql)
        else:
            connection.execute(sql, options)

        if commit:
            connection.commit()

        return commit

    def commitSQL(self, databaseConnection: list) -> bool:
        # TODO: Implement proper logging or errors
        connection = databaseConnection[0]

        try:
            connection.commit()
            return True
        except Exception as error:
            print(error)
            return False

    def closeDatabaseConnection(self, databaseConnection: list) -> bool:
        connection = databaseConnection[0]
        filePath = databaseConnection[1]

        try:
            if connection:
                connection.close()
                return True

        except Exception as error:
            # TODO: Implement proper logging or errors
            print("{} Connection still active for: ".format(filePath))
            print(error)
            return False

    def changeFile(self, fileName: str, create: bool = True) -> str:
        self.fileName = fileName
        self.filePath = "metrics/" + fileName

        if create:
            fileCreatedAlready = self.createDatabase()

            if fileCreatedAlready:
                return "{} was created at {}".format(self.fileName, self.filePath)

            else:
                return "{} has already been created at {}".format(
                    self.fileName, self.filePath
                )

        return "Changed file to {} at {}".format(self.fileName, self.filePath)
