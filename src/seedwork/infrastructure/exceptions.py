class InfrastructureException(Exception): ...


class MissingDatabaseConfiguration(InfrastructureException):
    def __init__(self, message="Missing one or more config values for db connection"):
        self.__message = message

    def __str__(self):
        return str(self.__message)


class MissingDatabaseCredentials(InfrastructureException):
    def __init__(self, message="Missing user and/or password for db connection"):
        self.__message = message

    def __str__(self):
        return str(self.__message)
