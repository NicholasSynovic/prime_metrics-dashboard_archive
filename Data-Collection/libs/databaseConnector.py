from os import error
import sqlite3
from sqlite3 import Connection, Cursor, IntegrityError, OperationalError


class DatabaseConnector:
    def __init__(self, databaseFileName: str) -> None:
        self.file = databaseFileName
        self.databaseConnection = None

    def createDatabase(self) -> bool:
        try:
            with open(self.file, "r") as database:
                database.close()
            return False
        except FileNotFoundError:
            with open(self.file, "w") as database:
                database.close()
            return True

    def openDatabaseConnection(self) -> None:
        databaseConnection = sqlite3.connect(self.file)
        self.databaseConnection = databaseConnection

    def executeSQL(
        self,
        sql: str,
        options: tuple = None,
        commit: bool = False,
    ) -> bool:
        connection = self.databaseConnection
        try:
            if options is None:
                connection.execute(sql)
            else:
                connection.execute(sql, options)
        except OperationalError:
            return False
        if commit:
            connection.commit()
            return True
        return "❗ Waiting to commit"

    def commitSQL(self, databaseConnection: Connection) -> bool:
        connection = databaseConnection
        try:
            connection.commit()
            return True
        except Exception as error:
            print("❗ {}".format(error))
            return False

    def closeDatabaseConnection(self, databaseConnection: Connection) -> bool:
        try:
            if databaseConnection:
                databaseConnection.close()
                return True

        except Exception as error:
            print("❗ Database connection still active for: {}".format(self.file))
            print("❗ {}".format(error))
            return False

    def changeFile(self, databaseFileName: str, create: bool = True) -> str:
        self.file = databaseFileName
        if create:
            fileCreatedAlready = self.createDatabase()
            if fileCreatedAlready:
                return "✔️ {} was created at {}".format(self.fileName, self.file)
            else:
                return "❗ {} has already been created at {}".format(
                    self.fileName, self.file
                )
        return "✔️ Changed file to {} at {}".format(self.fileName, self.file)
