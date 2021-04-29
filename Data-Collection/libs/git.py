from os import chdir, getcwd, popen, system
from os.path import exists

from progress.bar import Bar


class Git:
    def __init__(self) -> None:
        self.gitFolderName = ".git"
        self.gitPath = "/usr/bin/git"
        self.cwd = getcwd()

    def checkIfGitInstalled(self) -> bool:
        return exists(self.gitPath)

    def checkIfGitRepository(self, src: str) -> bool:
        chdir(src)

        val = exists(self.gitFolderName)

        chdir(self.cwd)
        return val

    def gitClone(self, repoURL: str, dst: str) -> int:
        return system(
            "git clone {} {} -q && cd {} && for remote in `git branch -r | grep -v /HEAD`; do git checkout --track $remote -f -q; done".format(
                repoURL, dst, dst
            )
        )

    def gitCommitHashCodes(self, sourceFolder: str) -> set:
        output = []

        chdir(sourceFolder)

        branches: list = (
            popen("git branch").read().replace(" ", "").replace("*", "").split("\n")
        )

        with Bar(message="Extracting commits from branches", max=len(branches)) as bar:
            branch: str
            for branch in branches:
                system("git checkout {} -q".format(branch))

                log: str = popen(cmd="git log").read()
                logList: list = log.split("\n")

                message: str
                for message in logList:
                    if message.find("commit") != -1:
                        output.append(message.split(" ")[1])
                bar.next()
        chdir(self.cwd)

        commit: str
        for commit in output:
            if commit == "":
                output.pop(output.index(commit))

        return set(output)

    def gitRepoCreate(self, src: str, dst: str, chc) -> None:
        src: str = self.cwd + "/" + src

        chdir(dst)

        print("Running command git init -q ...")
        system("git init -q")

        upstreamStr: str = "git remote add upstream {}".format(src)
        print("Running command {} ...".format(upstreamStr))
        system(upstreamStr)

        print("Running command git fetch upstream -q ...")
        system("git fetch upstream -q")

        checkoutStr: str = "git checkout {} -q".format(chc)
        print("Running command {} ...".format(checkoutStr))
        system(checkoutStr)

        chdir(self.cwd)
