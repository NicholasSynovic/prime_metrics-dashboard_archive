from libs.collector import Collector_3


class Branches(Collector_3):
    """Handels data referring to branches. Inherits from Collector_3 class"""

    def insertData(self, dataset: dict) -> None:
        """Takes in data identifying branches and inserts it into the database.

        Iterates through dataset, assigns an id num and executes sql to insert data into the
        database in a for loop. Will ignore the data if it is duplicated.

        Parameters:
            dataset (dict): nested dictionary containing data to be inserted into database.

        Note:
            dataset should include: the branch name and the branch hash

        Returns:
            No return value
        """
        id = 0

        for dataPoint in range(len(dataset)):
            name = dataset[dataPoint]["name"]
            sha = dataset[dataPoint]["commit"]["sha"]

            sql = "INSERT OR IGNORE INTO Branches (ID, Name, SHA) VALUES (?,?,?)"

            self.connection.executeSQL(
                sql,
                (id, name, sha),
                True,
            )

            id += 1
