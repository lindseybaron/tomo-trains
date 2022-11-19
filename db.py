class Database:

    def get(self, key=None):
        """Return a value given a key."""
        return getattr(self, key)

    def set(self, key, val):
        """Store a value for a key."""
        setattr(self, key, val)

    def keys(self):
        """Return all database keys."""
        return self.__dict__.keys()
