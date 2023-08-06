import boto3
from .disk import Disk, DiskError


class S3(Disk):
    @property
    def config_params(self) -> tuple:
        return ("aws_access_key_id", "aws_secret_access_key", "region", "bucket",)

    @property
    def session(self):
        return boto3.Session(
            aws_access_key_id=self.config.get("aws_access_key_id"),
            aws_secret_access_key=self.config.get("aws_secret_access_key"),
            region_name=self.config.get("region"),
        )

    @property
    def resource(self):
        return self.session.resource('s3')

    @property
    def bucket(self):
        return self.resource.Bucket(self.config.get("bucket"))

    def relativePath(self, path: str, is_directory: bool = False) -> str:
        if path.startswith("/"):
            path = path[1:]
        if is_directory and not path.endswith("/"):
            path = f"{path}/"
        return path

    def exists(self, path: str) -> bool:
        path = self.relativePath(path)
        return len(list(self.bucket.objects.filter(Prefix=path))) > 0

    def missing(self, path: str) -> bool:
        return not self.exists(path)

    def get(self, path: str, destination: str):
        if self.missing(path):
            return False
        path = self.relativePath(path)
        with open(destination, "wb") as f:
            self.resource.meta.client.download_fileobj(
                self.config.get("bucket"), path, f
            )
        return True

    def put(self, origin: str, destination: str) -> str:
        destination = self.relativePath(destination)
        self.resource.meta.client.upload_file(
            origin, self.config.get('bucket'), destination
        )
        return f"https://{self.config.get('bucket')}.s3.amazonaws.com/{destination}"

    def delete(self, path: str) -> bool:
        if self.isFile(path):
            path = self.relativePath(path)
            self.bucket.delete_objects(Delete={ "Objects": [{ "Key": path }]})
            return True
        return False

    def move(self, path: str, target: str) -> bool:
        if self.copy(path, target):
            return self.delete(path)
        return False

    def copy(self, path: str, target: str) -> bool:
        if self.isFile(path):
            target = self.relativePath(target)
            source = {
                "Bucket": self.config.get("bucket"),
                "Key": self.relativePath(path)
            }
            self.resource.meta.client.copy(source, self.config.get('bucket'), target)
            return self.isFile(target)
        return False

    def size(self, path: str) -> int:
        if self.isFile(path):
            path = self.relativePath(path)
            file = self.resource.meta.client.get_object(
                Bucket=self.config.get("bucket"),
                Key=path
            )
            return file.get("ContentLength")
        return False

    def lastModified(self, path: str) -> int:
        if self.isFile(path):
            path = self.relativePath(path)
            file = self.resource.meta.client.get_object(
                Bucket=self.config.get("bucket"),
                Key=path
            )
            return int(file.get("LastModified").timestamp())
        return False

    def files(self, path: str) -> list:
        path = self.relativePath(path, is_directory=True)
        if not self.isDirectory(path):
            raise DiskError("The directory does not exist")
        objects = self.bucket.objects.filter(Prefix=path, Delimiter="/")
        files = []
        for _ in objects:
            if not _.key.endswith("/"):
                files.append(_.key)
        return files

    def isFile(self, path: str) -> bool:
        path = self.relativePath(path)
        return len(list(self.bucket.objects.filter(Prefix=path))) == 1

    def directories(self, directory: str) -> list:
        if not self.isDirectory(directory):
            raise DiskError("The directory does not exist")
        directory = self.relativePath(directory, is_directory=True)
        result = self.resource.meta.client.list_objects(
            Bucket=self.config.get("bucket"),
            Prefix=directory,
            Delimiter="/"
        )
        directories = []
        for _ in result.get("CommonPrefixes", []):
            if _.get("Prefix").endswith("/"):
                directories.append(_.get("Prefix"))
        return directories

    def makeDirectory(self, path: str, mode: int = 511, recursive: bool = False) -> bool:
        path = self.relativePath(path, is_directory=True)
        self.resource.meta.client.put_object(
            Bucket=self.config.get("bucket"),
            Key=path
        )
        return self.isDirectory(path)

    def moveDirectory(self, directory: str, destination: str) -> bool:
        if self.copyDirectory(directory, destination):
            return self.deleteDirectory(directory)
        return False

    def copyDirectory(self, directory: str, destination: str) -> bool:
        if self.isDirectory(directory):
            path = self.relativePath(directory)
            objects = self.bucket.objects.filter(Prefix=path)
            for _ in objects:
                directory = self.relativePath(directory, is_directory=True)
                destination = self.relativePath(destination, is_directory=True)
                self.copyObject(_.key, _.key.replace(directory, destination, 1))
            return self.isDirectory(destination)
        return False

    def deleteDirectory(self, directory: str, recursive: bool = False) -> bool:
        if self.isDirectory(directory):
            directory = self.relativePath(directory, is_directory=True)
            objects = self.resource.meta.client.list_objects(
                Bucket=self.config.get("bucket"),
                Prefix=directory
            )
            keys = [
                {"Key" : k} for k in [
                    obj["Key"] for obj in objects.get('Contents', [])
                ]
            ]
            self.resource.meta.client.delete_objects(
                Bucket=self.config.get("bucket"),
                Delete={'Objects' : keys}
            )
            return True
        return False

    def cleanDirectory(self, directory: str) -> bool:
        if self.isDirectory(directory):
            self.deleteDirectory(directory)
            self.makeDirectory(directory)
            return self.isDirectory(directory)
        return False

    def isDirectory(self, path: str) -> bool:
        path = self.relativePath(path, is_directory=True)
        return len(list(self.bucket.objects.filter(Prefix=path))) > 0

    def copyObject(self, path: str, target: str):
        target = self.relativePath(target)
        source = {
            "Bucket": self.config.get("bucket"),
            "Key": self.relativePath(path)
        }
        self.resource.meta.client.copy(source, self.config.get('bucket'), target)
