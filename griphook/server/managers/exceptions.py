class ManagerException(Exception):
    pass


class ProjectManagerException(ManagerException):
    pass


class TeamManagerException(ManagerException):
    pass


class ServerManagerException(ManagerException):
    pass


class ClusterManagerException(ManagerException):
    pass
