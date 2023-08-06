from abc import ABC, abstractmethod


class AbstractClient(ABC):
    def __init__(self):
        self.__client = None

    @property
    def client(self):
        return self.__client

    @abstractmethod
    def __setitem__(self, key, value):
        pass

    @abstractmethod
    def __getitem__(self, key):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __delitem__(self, key):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def __contains__(self, key):
        pass

    @abstractmethod
    def keys(self):
        pass

    @abstractmethod
    def items(self):
        pass

    @abstractmethod
    def pop(self, key):
        pass
