import os.path

from database import Database
import pickle
import win32file


class Filedb(Database):
    def _init_(self):
        """
        initializer
        """
        super()._init_()
        file_handle = win32file.CreateFileW("dbfile.txt", win32file.GENERIC_WRITE, win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE, None, win32file.OPEN_ALWAYS, 0)
        win32file.CloseHandle(file_handle)

    def dump(self):
        """
        writes the dictionary in the file
        :return: None
        """
        file_handle = win32file.CreateFileW("dbfile.txt", win32file.GENERIC_WRITE, win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE, None, win32file.OPEN_ALWAYS, 0)
        data = pickle.dumps(self.dict)
        return_value = win32file.WriteFile(file_handle, data)
        assert return_value[0] == 0
        win32file.CloseHandle(file_handle)

    def load(self):
        """
        gets the file into the dictionary
        :return: None
        """
        file_handle = win32file.CreateFileW("dbfile.txt", win32file.GENERIC_READ, win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE , None, win32file.OPEN_ALWAYS, 0)
        error, data = win32file.ReadFile(file_handle, os.path.getsize("dbfile.txt"))
        assert error == 0
        try:
            self.dict = pickle.loads(data)
        except EOFError:
            self.dict = {}
        win32file.CloseHandle(file_handle)

    def set_value(self, key, val):
        """
        sets a new value in the dictionary file
        :param: key the key of the dictionary
        :param: val value to put in the dictionary
        :return: True if the value added to dictionary and false if not
        """
        self.load()
        flag = super().set_value(key, val)
        self.dump()
        return flag

    def get_value(self, key):
        """
        returns the value from the dictionary file
        :param: key the key of the dictionary
        :return: the value of the key
        """
        self.load()
        return super().get_value(key)

    def delete_value(self, key):
        """
        deletes the value of the key from the dictionary file
        :param key: the key of the dictionary
        :return: the value that was deleted
        """
        self.load()
        val = super().delete_value(key)
        self.dump()
        return val