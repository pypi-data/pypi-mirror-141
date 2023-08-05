import os
from enum import Enum, auto

USERHOME = os.path.expanduser("~")
TM_HOME = os.path.join(USERHOME, f".toolsmanager")
USER_BASHRC_PATH = os.path.join(USERHOME, ".bashrc")

TM_BIN = os.path.join(TM_HOME, "bin")
TM_BASHRC_PATH = os.path.join(TM_HOME, ".bashrc")
TM_GIT = os.path.join(TM_HOME, "git")
VERSION = "0.1.2"


class IsInstalledStatus(Enum):
    YES = auto()
    NO = auto()
    DONTKNOW = auto()
    PARTIAL = auto()


class InstallStatus(Enum):
    SUCCESS = auto()
    FAILURE = auto()
    PARTIAL = auto()
