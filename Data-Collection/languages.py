from requests import Response

from libs.collector import Collector_3


class Languages(Collector_3):
    def insertData(self, dataset: dict) -> None:
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
