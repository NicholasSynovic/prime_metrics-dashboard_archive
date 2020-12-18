from libs.collector import Collector_3


class Repository(Collector_3):
    def insertData(self, dataset: dict) -> None:
        id = dataset["id"]
        name = dataset["name"]
        owner = dataset["owner"]["login"]
        private = str(dataset["private"])
        fork = str(dataset["fork"])
        createdAt = dataset["created_at"]
        updatedAt = dataset["updated_at"]
        pushedAt = dataset["pushed_at"]
        size = dataset["size"]
        forks = dataset["forks_count"]
        openIssues = dataset["open_issues_count"]

        sql = "INSERT OR IGNORE INTO Repository (ID, Name, Owner, Private, Fork, Created_At, Updated_At, Pushed_At, Size, Forks, Open_Issues) VALUES (?,?,?,?,?,?,?,?,?,?,?)"

        self.connection.executeSQL(
            sql,
            (
                id,
                name,
                owner,
                private,
                fork,
                createdAt,
                updatedAt,
                pushedAt,
                size,
                forks,
                openIssues,
            ),
            True,
        )
