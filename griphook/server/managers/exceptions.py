class ManagerException(Exception):
    def __init__(self, error_text):
        self.error_text = error_text


class ProjectManagerException(ManagerException):
    pass


class TeamManagerException(ManagerException):
    pass


class ServerManagerException(ManagerException):
    pass


class ClusterManagerException(ManagerException):
    pass
