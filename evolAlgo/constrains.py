
import threading

from collections import OrderedDict


class EvolAlgoConstraints(object):
    def __init__(self):
        self._constraints = OrderedDict()
        self._locks = {}
        self.__initialized = True

    def update(self, other_userdata):
        """Combine this userdata struct with another.
        This overwrites duplicate keys with values from C{other_userdata}.
        """
        # Merge data
        self._constraints.update(other_userdata._constraints)

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __setitem__(self, key, item):
        self._constraints[key] = item

    def keys(self):
        return list(self._constraints.keys())

    def values(self):
        return list(self._constraints.values())

    def __contains__(self,key):
        return key in self._constraints

    def __getattr__(self, name):
        """Override getattr to be thread safe."""
        if name[0] == '_':
            return object.__getattr__(self, name)
        if name not in self._locks.keys():
            self._locks[name] = threading.Lock()

        try:
            with self._locks[name]:
                temp = self._constraints[name]
        except:
            pass

        return temp

    def __setattr__(self, name, value):
        """Override setattr to be thread safe."""
        # If we're still in __init__ don't do anything special
        if name[0] == '_' or '_UserData__initialized' not in self.__dict__:
            return object.__setattr__(self, name, value)

        if not name in self._locks.keys():
            self._locks[name] = threading.Lock()
        self._locks[name].acquire()
        self._constraints[name] = value
        self._locks[name].release()