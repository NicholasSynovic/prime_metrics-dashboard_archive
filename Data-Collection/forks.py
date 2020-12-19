from libs.collector import Collector_3


class Forks(Collector_3):
    def insertData(self, dataset: dict) -> None:
        for fork in dataset:
            id = fork["id"]
            name = fork["name"]
            owner = fork["owner"]["login"]
            createdAt = fork["created_at"]
            updatedAt = fork["updated_at"]
            pushedAt = fork["pushed_at"]
            size = fork["size"]
            forks = fork["forks_count"]
            openIssues = fork["open_issues_count"]

            sql = "INSERT OR IGNORE INTO Forks (ID, Name, Owner, Created_At, Updated_At, Pushed_At, Size, Forks, Open_Issues) VALUES (?,?,?,?,?,?,?,?,?)"

            self.connection.executeSQL(
                sql,
                (
                    id,
                    name,
                    owner,
                    createdAt,
                    updatedAt,
                    pushedAt,
                    size,
                    forks,
                    openIssues,
                ),
                True,
            )
