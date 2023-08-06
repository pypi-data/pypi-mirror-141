from aurelio.clients import RedisClient
from aurelio.exceptions import ClientError
from aurelio.settings import RedisSettings


def client_factory(settings):
    mapping = {
        'RedisSettings': RedisClient,
    }
    try:
        return mapping[settings.__class__.__name__](settings)
    except KeyError:
        raise ClientError('Client not supported!')
