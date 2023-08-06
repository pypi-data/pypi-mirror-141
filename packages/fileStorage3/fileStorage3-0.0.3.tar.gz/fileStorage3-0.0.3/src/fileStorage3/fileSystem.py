import os
import shutil
from .disk import Disk


class FileSystem(Disk):
    @property
    def config_params(self) -> tuple:
        return ("root",)

    def relativePath(self, path: str) -> str:
        """
        Parameters
        ----------
        path : str

        Returns
        -------
        str
        """
        if path.startswith("/"):
            path = path[1:]
        return os.path.join(self.config.get("root", "/"), path)

    def exists(self, path: str) -> bool:
        """ Determine if a file or directory exists.

        Parameters
        ----------
        path : str
            The file or directory path to check

        Returns
        -------
        bool
            True if file exists or False anotherwise
        """
        path = self.relativePath(path)
        return os.path.exists(path)

    def missing(self, path: str) -> bool:
        """ Determine if a file or directory is missing.

        Parameters
        ----------
        path : str
            The file or directory path to check

        Returns
        -------
        bool
        """
        return not self.exists(path)

    def get(self, path: str) -> str:
        """ Get the contents of a file

        Parameters
        ----------
        path : str

        Returns
        -------
        str

        Raises
        ------
        FileNotFoundException
        """
        pass

    def put(self, origin: str, destination: str) -> bool:
        """ Write the content of a file.

        Parameters
        ----------
        path : str
        contents : str

        Returns
        -------
        bool
        """
        pass

    def delete(self, path: str) -> bool:
        """ Delete the file at a given path.

        Parameters
        ----------
        path : str

        Returns
        -------
        bool
        """
        if self.isFile(path):
            path = self.relativePath(path)
            os.unlink(path)
            return True
        return False

    def move(self, path: str, target: str) -> bool:
        """ Move a file to a new location.

        Parameters
        ----------
        path : str
        target : str

        Returns
        -------
        bool
        """
        if self.isFile(path):
            path = self.relativePath(path)
            shutil.move(path, self.relativePath(target))
            return self.isFile(target)
        return False

    def copy(self, path: str, target: str) -> bool:
        """ Copy a file to a new location.

        Parameters
        ----------
        path : str
        target : str

        Returns
        -------
        bool
        """
        if self.isFile(path):
            path = self.relativePath(path)
            shutil.copy(path, self.relativePath(target))
            return self.isFile(target)
        return False

    def size(self, path: str) -> int:
        """ Get the file size of a given file.

        Parameters
        ----------
        path : str

        Returns
        -------
        int
        """
        path = self.relativePath(path)
        return os.stat(path).st_size

    def lastModified(self, path: str) -> int:
        """ Get the file's last modification time.

        Parameters
        ----------
        path : str

        Returns
        -------
        int
        """
        path = self.relativePath(path)
        return int(os.stat(path).st_mtime)

    def files(self, directory: str, hidden: bool = False) -> list:
        """ Get a list of all files in a directory.

        Parameters
        ----------
        directory : str
        hidden : bool

        Returns
        -------
        list
        """
        path = self.relativePath(directory)
        files = []
        for entry in os.listdir(path):
            if self.isFile(os.path.join(directory, entry)):
                if not entry.startswith(".") or hidden:
                    files.append(entry)
        return files

    def isFile(self, file: str) -> bool:
        """ Determine if the given path is a file.

        Parameters
        ----------
        file : str


        Returns
        -------
        bool
        """
        file = self.relativePath(file)
        return os.path.isfile(file)

    def directories(self, directory: str) -> list:
        """ Get all of the directories within a given directory

        Parameters
        ----------
        directory : str

        Returns
        -------
        list
        """
        path = self.relativePath(directory)
        directories = []
        for entry in os.listdir(path):
            if self.isDirectory(os.path.join(directory, entry)):
                directories.append(entry)
        return directories

    def makeDirectory(self, path: str, mode: int = 511, recursive: bool = False) -> bool:
        """ Create a directory.

        Parameters
        ----------
        path : str
        mode : int, optional
        recursive : bool, optional

        Returns
        -------
        bool
        """
        directory = self.relativePath(path)
        if recursive:
            os.makedirs(directory, mode=mode)
        else:
            os.mkdir(directory, mode=mode)
        return self.isDirectory(path)

    def moveDirectory(self, directory: str, destination: str) -> bool:
        """ Move a directory.

        Parameters
        ----------
        directory : str
        destination : str

        Returns
        -------
        bool
        """
        if self.isDirectory(directory):
            directory = self.relativePath(directory)
            shutil.move(directory, self.relativePath(destination))
            return self.isDirectory(destination)
        return False

    def copyDirectory(self, directory: str, destination: str) -> bool:
        """ Copy a directory from one location to another.

        Parameters
        ----------
        directory : str
        destination : str

        Returns
        -------
        bool
        """
        if self.isDirectory(directory):
            directory = self.relativePath(directory)
            shutil.copytree(directory, self.relativePath(destination))
            return self.isDirectory(destination)
        return False

    def deleteDirectory(self, directory: str, recursive: bool = False) -> bool:
        """ Recursively delete a directory.

        Parameters
        ----------
        directory : str
        recursive : bool, Optional

        Returns
        -------
        bool
        """
        if self.isDirectory(directory):
            directory = self.relativePath(directory)
            if recursive:
                shutil.rmtree(directory)
            else:
                print("?????", directory)
                os.rmdir(directory)
            return True
        return False

    def cleanDirectory(self, directory: str) -> bool:
        """ Empty the specified directory of all files and folders.

        Parameters
        ----------
        directory : str

        Returns
        -------
        bool
        """
        if not self.isDirectory(directory):
            return False
        for file in self.files(directory, hidden=True):
            self.delete(os.path.join(directory, file))
        for d in self.directories(directory):
            self.deleteDirectory(os.path.join(directory, d), recursive=True)
        return len(self.files(directory)) == 0 and len(self.directories(directory)) == 0

    def isDirectory(self, directory: str) -> bool:
        """ Determine if the given path is a directory.

        Parameters
        ----------
        directory : str

        Returns
        -------
        bool
        """
        directory = self.relativePath(directory)
        return os.path.isdir(directory)
