from libs.collector import Collector_3


class Issues(Collector_3):
    def insertData(self, dataset: dict) -> None:
        def _labelCollection(
            index: int,
        ) -> str:
            labelNames = []
            for label in dataset[index]["labels"]:
                labelNames.append(label["name"])
            return ", ".join(labelNames)

        def _asigneeCollection(
            index: int,
        ) -> str:
            labelNames = []
            for assignee in dataset[index]["assignees"]:
                labelNames.append(assignee["login"])
            return ", ".join(labelNames)

        for dataPoint in range(len(dataset)):
            id = dataset[dataPoint]["id"]
            count = dataset[dataPoint]["number"]
            title = dataset[dataPoint]["title"]
            author = dataset[dataPoint]["user"]["login"]
            assignees = _asigneeCollection(index=dataPoint)
            labels = _labelCollection(index=dataPoint)
            state = dataset[dataPoint]["state"]
            createdAt = dataset[dataPoint]["created_at"]
            updatedAt = dataset[dataPoint]["updated_at"]
            closedAt = dataset[dataPoint]["closed_at"]

            sql = "INSERT OR IGNORE INTO Issues (ID, Count, Title, Author, Assignees, Labels, State, Created_At, Updated_At, Closed_At) VALUES (?,?,?,?,?,?,?,?,?,?);"

            self.connection.executeSQL(
                sql,
                (
                    id,
                    count,
                    title,
                    author,
                    assignees,
                    labels,
                    state,
                    createdAt,
                    updatedAt,
                    closedAt,
                ),
                True,
            )
