import sqlite3
from os import error
from sqlite3 import Connection, OperationalError


class DatabaseConnector:
    """Class to use when accessing the database file where data is stored.

    This class can create, add data to, and return data from a database.

    Note:
        The database specification is SQLite and all database files need to be created with the filetype, ".db".
    """

    def __init__(self, databaseFileName: str) -> None:
        """Initializes the class

        Returns:
            None: The class is initalized.
        """
        self.file = databaseFileName
        self.databaseConnection = None

    def createDatabase(self) -> bool:
        """Creates the database file if it does not already exists.

        Returns:
            bool: Returns True if the database is created and False if the database already exists.
        """
        try:
            with open(self.file, "r") as database:
                database.close()
            return False
        except FileNotFoundError:
            with open(self.file, "w") as database:
                database.close()
            return True

    def openDatabaseConnection(self) -> None:
        """Opens a connection to the database."""
        self.databaseConnection = sqlite3.connect(self.file)

    def executeSQL(
        self,
        sql: str,
        options: tuple = None,
        commit: bool = False,
    ) -> bool:
        """Executes SQL code on the current working database.

        Parameters:
            sql (str): The SQL code to be executed.
            options (tuple): A list of options that can be executed alongside the SQL commands.
            commit (bool): If True, the connection to the database will commit the changes to the database.

        Returns:
            bool: Returns False if there is an error executing the SQL commands and True if it goes through with the connection.
        """
        connection = self.databaseConnection
        try:
            if options is None:
                connection.execute(sql)
            else:
                connection.execute(sql, options)
        except OperationalError as error:
            print("❗ {}".format(error))
            return False
        if commit:
            connection.commit()
            return True
        return "❗ Waiting to commit"

    def commitSQL(self, databaseConnection: Connection) -> bool:
        """Commits changes to the database.

        Parameters:
            databaseConnection (Connection): A connection object to the current working database.

        Returns:
            bool: Returns True if there are no operational errors and False if there are any errors."""
        connection = databaseConnection
        try:
            connection.commit()
            return True
        except Exception as error:
            print("❗ {}".format(error))
            return False

    def closeDatabaseConnection(self, databaseConnection: Connection) -> bool:
        """Closes the connection to the current working database.

        Parameters:
            databaseConnection (Connection): The connection object to the current working database.

        Returns:
            bool: Returns True if the connection is closed successfully and False otherwise.
        """
        try:
            if databaseConnection:
                databaseConnection.close()
                return True

        except Exception as error:
            print("❗ Database connection still active for: {}".format(self.file))
            print("❗ {}".format(error))
            return False

    def changeFile(self, databaseFileName: str, create: bool = True) -> str:
        """Changes the current working database file to something else.

        Parameters:
            databaseFileName (str): The name of the new database file to create.
            create (bool): Set to True to create the new database or set it to False to use an existing database file.

        Returns:
            str: A string that provides further information about the database in question.
        """
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

    def selectColumn(self, table: str, column: str) -> list:
        """Returns all data from a column in a table of the current working database.

        Parameters:
            table (str): The name of the table to get information from.
            column (str): The name of the column in the table to get information from.
        """
        command = self.databaseConnection.execute(
            "SELECT {} FROM {}".format(column, table)
        )
        return command.fetchall()
