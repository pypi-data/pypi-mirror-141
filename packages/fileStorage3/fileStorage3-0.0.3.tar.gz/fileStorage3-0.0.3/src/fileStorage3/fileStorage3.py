import abc
import boto3
from .fileSystem import FileSystem
from .s3 import S3

class FileStorage3:
    def __init__(self) -> None:
        self.disks = {}

    def disk(self, name: str):
        return self.get(name)

    def get(self, name: str):
        return self.disks[name] if name in self.disks else None

    def set(self, name: str, disk, config: dict):
        self.disks[name] = disk(config)
        return self

    def createS3Driver(self, config: dict):
        self.set('s3', S3, config)

    def createFileSystemDriver(self, config: dict):
        self.set('local', FileSystem, config)
