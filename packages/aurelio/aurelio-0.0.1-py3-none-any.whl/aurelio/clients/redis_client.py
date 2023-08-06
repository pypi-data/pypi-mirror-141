import logging

from aurelio.clients.abstract_client import AbstractClient

try:
    from redis import Redis
except ImportError:
    logging.warning('Could not import Redis client!')


class RedisClient(AbstractClient):
    def __init__(self, settings):
        super().__init__()
        self.__settings = settings
        self.__client = Redis(**settings.asdict())

    def decode(self, data):
        return data.decode(self.__settings.encoding)

    def __setitem__(self, key, value):
        self.__client.set(key, value)

    def __getitem__(self, key):
        value = self.__client.get(key)
        if value is None:
            raise KeyError(key)
        return self.decode(value)

    def __len__(self):
        return self.__client.dbsize()

    def __delitem__(self, key):
        self.pop(key)

    def clear(self):
        self.__client.flushdb()

    def __contains__(self, key):
        return self.__client.exists(key)

    def keys(self):
        for key in self.__client.keys():
            yield self.decode(key)

    def items(self):
        for key in self.__client.scan_iter():
            yield (self.decode(key), self[key])

    def pop(self, key):
        value = self[key]
        self.__client.delete(key)
        return value
