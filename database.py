class Database:
    def __init__(self):
        """
        initializer
        """
        self.dict = {}

    def set_value(self, key, val):
        """
        sets a new value in the dictionary
        :param: key the key of the dictionary
        :param: val value to put in the dictionary
        :return: True if the value added to dictionary and false if not
        """
        self.dict[key] = val
        if key in self.dict.keys():
            return True
        else:
            return False

    def get_value(self, key):
        """
        returns the value in the dictionary
        :param: key the key of the dictionary
        :return: the value of the key
        """
        if key in self.dict.keys():
            return self.dict.get(key)
        else:
            return None

    def delete_value(self, key):
        """
        deletes the value of the key
        :param key: the key of the dictionary
        :return: the value that was deleted
        """
        if key in self.dict.keys():
            value = self.get_value(key)
            del self.dict[key]
            return value
        else:
            return None

