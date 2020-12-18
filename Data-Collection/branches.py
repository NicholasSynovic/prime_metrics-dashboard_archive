from libs.collector import Collector_3


class Branches(Collector_3):
    def insertData(self, dataset: dict) -> None:
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
