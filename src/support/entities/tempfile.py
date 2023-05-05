import os


class TempFile:

    _path = None

    def __init__(self, path):
        self._path = path

    @property
    def path(self):
        return self._path

    def close(self):
        os.remove(self.path)
