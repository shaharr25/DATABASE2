import threading
import multiprocessing
from filedb import Filedb
import logging
import win32event


class Syncdb:
    def _init_(self, database: Filedb, thread_or_process):
        """
        initializer
        :param database: dictionary
        :param thread_or_process: true if thread and false if process
        """
        if not isinstance(database, Filedb):
            raise ValueError("not filedb instance")
        self.database = database
        self.semaphore = win32event.CreateSemaphore(None, 10, 10, "semaphore")
        self.lock = win32event.CreateMutex(None, True, "lock")


    def get_value(self, key):
        """
        let only 10 readers read at the same time
        :param: key the key of the dictionary
        :return: the value of the key
        """
        win32event.WaitForSingleObject(self.semaphore, win32event.INFINITE)
        logging.debug("reader in")
        value = self.database.get_value(key)
        win32event.ReleaseSemaphore(self.semaphore, 1)
        logging.debug("reader out")
        return value

    def set_value(self, key, val):
        """
        let only one user set a new value in the dictionary with no other readers or writers at the same time
        :param: key the key of the dictionary
        :param: val value to put in the dictionary
        :return: True if the value added to dictionary and false if not
        """
        win32event.WaitForSingleObject(self.lock, win32event.INFINITE)
        for i in range(10):
            win32event.WaitForSingleObject(self.semaphore, win32event.INFINITE)
        logging.debug("writer in")
        flag = self.database.set_value(key, val)
        win32event.ReleaseSemaphore(self.semaphore, 10)
        logging.debug("writer out")
        win32event.ReleaseMutex(self.lock)
        return flag

    def delete_value(self, key):
        """
        let only one user to delete from the dictionary with no other readers or writers at the same time
        :param key: the key of the dictionary
        :return: the value that was deleted
        """
        self.lock.acquire()
        for i in range(10):
            self.semaphore.acquire()
        flag = self.database.delete_value(key)
        for i in range(10):
            self.semaphore.release()
        self.lock.release()
        return flag