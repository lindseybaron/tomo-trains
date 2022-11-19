from threading import Lock, Thread


class Database:

    def get(self, key=None):
        """ Implement a function to return a value given a key """
        return getattr(self, key)

    def set(self, key, val):
        """ Implement a function to store a value for a key """
        setattr(self, key, val)

    def keys(self):
        """ Implement a function to return database keys """
        return self.__dict__.keys()
