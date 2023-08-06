from aurelio import utils


class Dict:
    def __init__(self, settings):
        self.__client = utils.client_factory(settings)

    @property
    def client(self):
        return self.__client.client

    def __setitem__(self, key, value):
        self.__client[key] = value

    def __getitem__(self, key):
        return self.__client[key]

    def __len__(self):
        return len(self.__client)

    def __delitem__(self, key):
        del self.__client[key]

    def clear(self):
        self.__client.clear()

    def __contains__(self, key):
        return key in self.__client

    def has_key(self, key):
        return key in self.__client

    def keys(self):
        return self.__client.keys()

    def items(self):
        return self.__client.items()

    def values(self):
        for _, value in self.items():
            yield value

    def pop(self, key):
        return self.__client.pop(key)

    def __iter__(self):
        return iter(self.values())

    def copy(self):
        raise NotImplementedError('Copy method is not implemented!')

    def __cmp__(self, other):
        raise NotImplementedError('Compare method is not implemented!')

    def update(self, *args, **kwargs):
        raise NotImplementedError('Update method is not implemented!')
