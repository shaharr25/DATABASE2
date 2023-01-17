from syncdb import Syncdb
from filedb import Filedb
from threading import Thread
import logging
import win32event
import win32process


def writer(db):
    """
    writer gets access to write to the dictionary
    :param db: dictionary
    :return:  None
    """
    logging.debug("writer joined")
    for i in range(100):
        assert db.set_value(i, i)
    for i in range(100):
        val = db.delete_value(i)
        flag = val == i or val is None
        assert flag
    logging.debug("writer left")


def reader(db):
    """
    reader gets access to read value from the dictionary
    :param db: dictionary
    :return: None
    """
    logging.debug("reader joined")
    for i in range(100):
        flag = db.get_value(i) is None or db.get_value(i) == i
        assert flag
    logging.debug("reader left")


def main():
    logging.basicConfig(filename='logthread.txt', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(threadName)s %(message)s')
    db = Syncdb(Filedb(), True)
    for i in range(200, 300):
        db.set_value(i, i)
    logging.debug("no competition")
    writer(db)
    reader(db)
    logging.debug("in competition")
    counter = 0
    for i in range(0, 10):
        thread = win32process.beginthreadex(None, 1000, reader, (db,), 0)[0]
        if win32event.WaitForSingleObject(thread, win32event.INFINITE) == 0:
            counter += 1
    for i in range(0, 50):
        thread = win32process.beginthreadex(None, 1000, writer, (db, ), 0)[0]
        if win32event.WairForSingleObject(thread, win32event.INFINITE) == 0:
            counter += 1




if __name__ == "__main__":
    main()