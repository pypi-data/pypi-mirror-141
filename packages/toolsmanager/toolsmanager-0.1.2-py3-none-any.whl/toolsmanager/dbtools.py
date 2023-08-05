import json

import attr
import coloring

from . import exceptions, utils
from .bases import pm_tasks
from .consts import IsInstalledStatus

# Import to load tasks
from .tasks import BaseTask


@attr.s
class Collection:
    name = attr.ib()
    collections = attr.ib(kw_only=True, factory=list)
    tools = attr.ib(kw_only=True, factory=list)


@attr.s
class AttrTool:
    name = attr.ib()
    deps = attr.ib(kw_only=True, factory=set)
    tasks = attr.ib(kw_only=True, factory=list)
    tags = attr.ib(kw_only=True, factory=set)

    def install(self):
        requires_root = self.requires_root()

        # debug printing
        if requires_root:
            coloring.print_info(
                f"{self.name!r} requires root privileges to be installed"
            )
        else:
            coloring.print_info(
                f"{self.name!r} does not require root privileges to be installed"
            )

        # exit if not root and need root privileges (like with sudo apt install)
        if requires_root and not utils.is_root():
            raise exceptions.RootPrivilegesRequiredException

        # check if the tool is installed
        # FIXME: check is installed before root previlges
        is_installed = self.isinstalled()
        if is_installed == IsInstalledStatus.YES:
            coloring.print_info(f"{self.name!r} is already installed")
        elif is_installed == IsInstalledStatus.NO:
            coloring.print_info(f"{self.name!r} is not installed")
        else:
            coloring.print_info(
                f"{self.name!r} is installed status {is_installed.name!r}"
            )

        # install
        # FIXME: we already checked installs, gather the i of last installed and go on
        # TODO: Install deps
        # Create metadata to give to all tasks
        meta = {}
        # Keep track of previous_tasks
        previous_tasks = []
        for task in self.tasks:
            is_installed = task.isinstalled()
            if not is_installed == IsInstalledStatus.YES:
                # prepare for installation (meta, previous_tasks)
                # keep old meta
                old_meta = task.meta
                task.meta = dict(task.meta)
                task.meta.update(meta)

                # keep old previous_tasks
                old_previous_tasks = task.previous_tasks
                task.previous_tasks = previous_tasks

                # install
                task.install()

            meta = task.get_metadata()
            previous_tasks.append(task)

            if not is_installed == IsInstalledStatus.YES:
                # restore meta/previous_tasks
                task.meta = old_meta
                task.previous_tasks = old_previous_tasks

        coloring.print_success(f"{self.name!r} installed")

    def isinstalled(self):
        # all yes => yes
        # one no => no
        # TODO: fixme with DONTKNOW
        # FIXME: if one no, maybe previous tasks are yes (example in nikto (git+bin)
        #   bin is no but git is yes => is_installed => partial
        nb_yes = 0
        for i, task in reversed(list(enumerate(self.tasks))):
            is_installed = task.isinstalled()
            # print("[DEBUG]", task.name, is_installed.name)
            if is_installed == IsInstalledStatus.NO:
                return IsInstalledStatus.NO
            elif is_installed == IsInstalledStatus.YES:
                nb_yes += 1
        if nb_yes == len(self.tasks):
            return IsInstalledStatus.YES
        return IsInstalledStatus.DONTKNOW

    def uninstall(self):
        is_installed = self.isinstalled()
        if is_installed == IsInstalledStatus.YES:
            coloring.print_info(f"{self.name!r} is already installed")
        elif is_installed == IsInstalledStatus.NO:
            coloring.print_info(f"{self.name!r} is not installed, skipping")
        else:
            coloring.print_info(
                f"{self.name!r} is installed status {is_installed.name!r}"
            )

        if is_installed in [IsInstalledStatus.YES, IsInstalledStatus.DONTKNOW]:
            for task in reversed(self.tasks):
                task.uninstall()

    def requires_root(self):
        return any(task.requires_root() for task in self.tasks)


class Tool:
    def __init__(self, name, *, raw_tasks):
        self.name = name
        self.raw_tasks = raw_tasks
        self._tasks = None

    @property
    def tasks(self):
        if self._tasks is None:
            self._tasks = []
            for raw_task in self.raw_tasks:
                raw_task = dict(raw_task)
                Task = pm_tasks[raw_task["task"]]
                kwargs = dict(raw_task)
                kwargs.pop("task")
                task = Task(**kwargs)
                self._tasks.append(task)
        return self._tasks

    def isinstalled(self):
        pass

    def install(self):
        pass

    def requires_root(self):
        return any(task.requires_root() for task in self.tasks)

    def __str__(self):
        return f"Tool({self.name!r})"

    def __repr__(self):
        return self.__str__()


class ToolsManager:
    def __init__(self):
        # Tools as class
        self._tools = {}
        # Tools in dict format
        self._raw_tools = {}

    def __getitem__(self, item) -> Tool:
        if item in self._tools:
            return self._tools[item]

        raw_tool = self._raw_tools[item]
        tool = Tool(raw_tool["name"], raw_tasks=raw_tool["tasks"])

        self._tools[item] = tool
        return tool

    def add_tool(self, name, *, tasks=None, deps=None, tags=None):
        if name in self._tools:
            raise exceptions.ToolAlreadyExistsException(
                f"Tool {name!r} already in database"
            )
        self._tools[name] = AttrTool(name, tags=tags, tasks=tasks, deps=deps)

    def get_tool(self, name: str):
        return self._tools[name]

    def install(self, *toolnames, raise_errors=False):
        # TODO: fix order with set/list
        toolnames = set(toolnames)  # remove duplicates
        # nb_success = 0
        # nb_failures = 0
        for tool_name in toolnames:

            try:
                tool = self.get_tool(tool_name)
                coloring.print_info(f"Installing {tool.name!r}")
                tool.install()
            except Exception as e:
                coloring.print_failure(
                    f'Error installing {tool_name!r} "{type(e).__name__} {e}"'
                )
                continue

    def uninstall(self, *toolnames, raise_errors=False):
        toolnames = set(toolnames)  # remove duplicates
        # nb_success = 0
        # nb_failures = 0
        for tool_name in toolnames:
            try:
                tool = self.get_tool(tool_name)
                coloring.print_info(f"Uninstalling {tool.name!r}")
                tool.uninstall()

            except Exception as e:
                coloring.print_failure(
                    f'Error uninstalling {tool_name!r} "{type(e).__name__} {e}"'
                )
                continue

    def install_collection(self,):
        pass

    def normalize_task(self, task) -> BaseTask:
        if isinstance(task, BaseTask):
            return task
        raw_task = task
        del task

        raw_task = dict(raw_task)  # make a copy
        Task = pm_tasks[raw_task["task"]]  # get the cls of the task
        kwargs = dict(raw_task)
        kwargs.pop("task")
        task = Task(**kwargs)
        return task

    def loaddb(self, dbpath: str):
        raw_json_tools = json.load(open(dbpath))

        for raw_tool in raw_json_tools:
            tasks = raw_tool.get("tasks", [])
            tasks = [self.normalize_task(task) for task in tasks]
            self.add_tool(
                raw_tool["name"],
                tasks=tasks,
                deps=raw_tool.get("deps"),
                tags=raw_tool.get("tags"),
            )

    def loaddb_old(self, dbpath):
        # old function using lazy load (maby I will use it latter if needed)
        json_tools = json.load(open(dbpath))
        tools = {}
        for json_tool in json_tools:
            name = json_tool["name"]
            tools[name] = json_tool

        self._raw_tools = tools
