class ToolsManagerException(Exception):
    pass


class CmdAlreadyExistException(ToolsManagerException):
    pass


class CmdDontExistException(ToolsManagerException):
    pass


class ToolDontExistsException(ToolsManagerException):
    pass


class ToolAlreadyExistsException(ToolsManagerException):
    pass


class RootPrivilegesRequiredException(ToolsManagerException):
    pass
