import os

import coloring

from . import consts
from .bases import BaseTask
from .consts import IsInstalledStatus
from .functions import addcmd, gitclone, normalize_git_repo, rmcmd, rmgit
from .utils import run


class AptTask(BaseTask):
    name = "apt"

    def __init__(self, name):
        super().__init__()
        self.name = name

    def install(self):
        results = run(["apt", "install", self.name, "-y"])
        if results.returncode == 0:
            return "OK"
        print(results)

    def isinstalled(self):
        pass

    def uninstall(self):
        run(["apt", "remove", self.name, "-y"])

    def requires_root(self):
        return True

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name})"


class GitTask(BaseTask):
    name = "git"

    def __init__(self, repo):
        super().__init__()
        self.repo = repo

    def uninstall(self):
        normalized_repo = normalize_git_repo(self.repo)
        directory = normalized_repo["directory"]
        coloring.print_info(f"Removing git directory {directory}")
        rmgit(directory)

    def install(self):
        normalized_repo = normalize_git_repo(self.repo)
        fullurl = normalized_repo["fullurl"]
        coloring.print_info(f"Cloning repository {fullurl!r}")
        x = gitclone(self.repo, verbose=False)
        return x

    def isinstalled(self):
        dir_git = self.repo.split("/")[1]
        if os.path.exists(os.path.join(consts.TM_GIT, dir_git)):
            return IsInstalledStatus.YES
        else:
            return IsInstalledStatus.NO

    def get_metadata(self):
        parsed_repo = normalize_git_repo(self.repo)
        directory = parsed_repo["directory"]
        return {"tool_directory": os.path.join(os.path.join(consts.TM_GIT, directory))}

    def __str__(self):
        return f"{self.__class__.__name__}(repo={self.repo})"


class BinTask(BaseTask):
    name = "bin"

    def __init__(self, executables, fromdir=False):
        """fromdir => must cd in directory before"""
        super().__init__()
        if isinstance(executables, str):
            executables = [executables]
        self.executables = executables

    def install(self):
        for executable in self.executables:
            if ":" in executable:
                executable, cmdname = executable.split(":")
            else:
                cmdname = None
            tool_directory = self.meta["tool_directory"]
            cmdpath = f"{tool_directory}/{executable}"
            cmdname_str = cmdname or os.path.basename(executable)
            coloring.print_info(
                f"Adding bin shortcut {executable!r} -> {cmdname_str!r}"
            )
            addcmd(cmdpath, cmdname)

    def isinstalled(self) -> consts.IsInstalledStatus:
        for executable in self.executables:
            if ":" in executable:
                executable = executable.split(":")[1]
            if not os.path.exists(os.path.join(consts.TM_BIN, executable)):
                return consts.IsInstalledStatus.NO
        return consts.IsInstalledStatus.YES

    def uninstall(self):
        for executable in self.executables:
            if ":" in executable:
                executable = executable.split(":")[1]

            coloring.print_info(f"Removing bin shortcut {executable!r}")
            rmcmd(executable)

    def __str__(self):
        return f"BinTask(executables={self.executables!r})"


class DlTask(BaseTask):
    name = "dl"

    def __init__(self):
        super().__init__()

    def uninstall(self):
        # Do nothing
        pass

    def install(self):
        url_repo = f"https://github.com/{self.repo}"
        x = gitclone(url_repo)
        return x

    def isinstalled(self):
        dir_git = self.repo.split("/")[1]
        return os.path.exists(os.path.join(consts.TM_GIT, dir_git))

    def __str__(self):
        return f"DlTask(repo={self.repo!r})"


class SnapTask(BaseTask):
    name = "snap"

    def __init__(self, name):
        super().__init__()
        self.name = name

    def requires_root(self):
        return True

    def uninstall(self):
        # Do nothing
        pass

    def install(self):
        url_repo = f"https://github.com/{self.repo}"
        x = gitclone(url_repo)
        return x

    def isinstalled(self):
        dir_git = self.repo.split("/")[1]
        return os.path.exists(os.path.join(consts.TM_GIT, dir_git))

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name})"


class BashTask(BaseTask):
    name = "bash"

    def __init__(self, path, root=False):
        super().__init__()
        self.path = path
        self.root = root

    def requires_root(self):
        return self.root

    def uninstall(self):
        # Do nothing
        pass

    def install(self):
        print("meta in bash", self.meta)
        path = os.path.join(self.meta["tool_directory"], self.path)
        run(path, None, None)

    def isinstalled(self):
        return False

    def __str__(self):
        return f"{self.__class__.__name__}(path={self.path})"


class MageTask(BaseTask):
    name = "mage"

    def install(self):
        pass

    def isinstalled(self):
        return False

    def __str__(self):
        return f"{self.__class__.__name__}()"


class WwwTask(BaseTask):
    # Copy the file to "www" to be shared after
    name = "www"

    def __init__(self, path):
        super().__init__()

    def install(self):
        pass

    def isinstalled(self):
        return False

    def __str__(self):
        return f"{self.__class__.__name__}()"
