from libs.collector import Collector_CommitWebScraper

from collections import defaultdict


class Files(Collector_CommitWebScraper):
    def insertData(self) -> int:

        commitSHA = set()
        loc = []
        noc = []
        sizeBytes = []
        pairs = {}

        self.getPage()

        data = self.getData()

        for info in data:

            filesSQL = "INSERT OR IGNORE INTO Files (ID, Commit_SHA, Branch, File_Tree, Status, Raw_URL, Lines_Of_Code, Number_Of_Characters, Size_In_Bytes) VALUES (?,?,?,?,?,?,?,?,?)"

            locNOC_Size = self.getLOCNOC_Size(rawURL=info[2])

            self.connection.executeSQL(
                filesSQL,
                (
                    self.id,
                    self.commitSHA,
                    self.branch,
                    info[0],
                    info[1],
                    info[2],
                    locNOC_Size[0],
                    locNOC_Size[1],
                    locNOC_Size[2],
                ),
                True,
            )
            self.id += 1

            commitSHA.add(self.commitSHA)
            loc.append((self.commitSHA, locNOC_Size[0]))
            noc.append((self.commitSHA, locNOC_Size[1]))
            sizeBytes.append((self.commitSHA, locNOC_Size[2]))

            for sha in commitSHA:
                pairs[sha] = defaultdict(lambda: 0)

            for pair in loc:
                pairs[pair[0]]["LOC"] += pair[1]

            for pair in noc:
                pairs[pair[0]]["NOC"] += pair[1]

            for pair in sizeBytes:
                pairs[pair[0]]["size"] += pair[1]

        commitsSQL = "UPDATE Commits SET Lines_Of_Code = ?, Number_Of_Characters = ?, Size_In_Bytes = ? WHERE Commit_SHA = ?"

        for key in pairs.keys():

            self.connection.executeSQL(
                commitsSQL,
                (pairs[key]["LOC"], pairs[key]["NOC"], pairs[key]["size"], key),
                True,
            )
