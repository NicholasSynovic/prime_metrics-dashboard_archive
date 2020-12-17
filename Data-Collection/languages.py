from requests import Response

from libs.databaseConnector import DatabaseConnector
from libs.githubConnector import GitHubConnector
from libs.collector import Collector


class Languages(Collector):
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
