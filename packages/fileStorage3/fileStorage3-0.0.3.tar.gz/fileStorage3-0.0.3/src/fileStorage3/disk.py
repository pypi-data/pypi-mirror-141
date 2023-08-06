import abc


class DiskError(ValueError):
    def __init__(self, message: str = "", *args: object, **kwargs: object) -> None:
        ValueError.__init__(self, message, *args, **kwargs)


class DiskInterface(abc.ABC):
    @property
    @abc.abstractmethod
    def config(self) -> dict:
        pass

    @property
    @abc.abstractmethod
    def config_params(self) -> tuple:
        pass

    @abc.abstractmethod
    def setConfig(self, config: dict) -> None:
        pass

    @abc.abstractmethod
    def relativePath(self, path: str) -> str:
        pass

    @abc.abstractmethod
    def exists(self, path: str) -> bool:
        pass

    @abc.abstractmethod
    def missing(self, path: str) -> bool:
        pass

    @abc.abstractmethod
    def get(self, path: str):
        pass

    @abc.abstractmethod
    def put(self, origin: str, destination: str) -> str:
        pass

    @abc.abstractmethod
    def delete(self, path: str) -> bool:
        pass

    @abc.abstractmethod
    def move(self, path: str, target: str) -> bool:
        pass

    @abc.abstractmethod
    def copy(self, path: str, target: str) -> bool:
        pass

    @abc.abstractmethod
    def size(self, path: str) -> int:
        pass

    @abc.abstractmethod
    def lastModified(self, path: str) -> int:
        pass

    @abc.abstractmethod
    def files(self, path: str) -> list:
        pass

    @abc.abstractmethod
    def isFile(self, path: str) -> bool:
        pass

    @abc.abstractmethod
    def directories(self, directory: str) -> list:
        pass

    @abc.abstractmethod
    def makeDirectory(self, path: str, mode: int = 511, recursive: bool = False) -> bool:
        pass

    @abc.abstractmethod
    def moveDirectory(self, directory: str, destination: str) -> bool:
        pass

    @abc.abstractmethod
    def copyDirectory(self, directory: str, destination: str) -> bool:
        pass

    @abc.abstractmethod
    def deleteDirectory(self, directory: str, recursive: bool = False) -> bool:
        pass

    @abc.abstractmethod
    def cleanDirectory(self, directory: str) -> bool:
        pass

    @abc.abstractmethod
    def isDirectory(self, path: str) -> bool:
        pass


class Disk(DiskInterface):
    __config = {}

    def __init__(self, config: dict) -> None:
        self.setConfig(config)

    @property
    def config(self):
        return self.__config

    def setConfig(self, config: dict) -> None:
        """
        Parameters
        ----------
        config : dict
        """
        if not set(self.config_params).issubset(config.keys()):
            raise DiskError("The configuration is not valid")
        self.__config = config
