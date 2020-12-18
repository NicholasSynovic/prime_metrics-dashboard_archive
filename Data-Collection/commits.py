from libs.collector import Collector_4


class Commits(Collector_4):
    def insertData(self, dataset: dict) -> None:
        id = 0
        for dataPoint in range(len(dataset)):
            sha = dataset[dataPoint]["sha"]
            author = dataset[dataPoint]["commit"]["author"]["name"]
            date = dataset[dataPoint]["commit"]["committer"]["date"]
            treeSHA = dataset[dataPoint]["commit"]["tree"]["sha"]
            commentCount = dataset[dataPoint]["commit"]["comment_count"]

            sql = "INSERT OR IGNORE INTO Commits (ID, SHA, Author, Commit_Date, Tree_SHA, Comment_Count) VALUES (?,?,?,?,?,?);"

            self.connection.executeSQL(
                sql, (id, sha, author, date, treeSHA, commentCount), True
            )

            id += 1
