from libs.collector import Collector_3


class Files(Collector_3):
    def insertData(self, dataset: dict) -> int:
        for file in range(len(dataset["tree"])):
            filename = dataset["tree"][file]["path"]
            commitSHA = self.currentPage

            sql = "INSERT OR IGNORE INTO Files (ID, Commit_SHA, Branch, Filename) VALUES (?,?,?,?)"

            self.connection.executeSQL(
                sql,
                (
                    self.id,
                    commitSHA,
                    self.branch,
                    filename,
                ),
                True,
            )
            self.id += 1
