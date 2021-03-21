from libs.collector import Collector_3
from requests import Response


class Languages(Collector_3):
    """Handels data referring to languages. Inherits from Collector_3 class"""

    def insertData(self, dataset: dict) -> None:
        """Takes in data identifying commits and inserts it into the database.

        Iterates through the dataset, assigns an id and executes sql to insert data into the database in a
        for loop. Will ignore the data if it is duplicated.

        Parameters:
            dataset (dict): nested dictionary containing data to be inserted into database

        Note:
            dataset should include: language and bytes of code in the language

        Returns:
            No return value
        """
        id = 0
        for key in dataset.keys():
            language = key
            bytesOfCode = dataset[key]
            sql = "INSERT OR IGNORE INTO Languages (ID, Language, Bytes_of_Code ) VALUES (?,?,?)"

            self.connection.executeSQL(
                sql,
                (id, language, bytesOfCode),
                True,
            )

            id += 1
