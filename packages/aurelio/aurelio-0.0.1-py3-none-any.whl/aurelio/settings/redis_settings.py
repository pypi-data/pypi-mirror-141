import dataclasses


@dataclasses.dataclass
class RedisSettings:
    host: str = 'localhost'
    port: int = 6379
    db: int = 0
    password: str = None
    socket_timeout = None
    socket_connect_timeout = None
    socket_keepalive = None
    socket_keepalive_options = None
    connection_pool = None
    unix_socket_path = None
    encoding: str = 'utf-8'
    encoding_errors: str = 'strict'
    charset = None
    errors = None
    decode_responses: bool = False
    retry_on_timeout: bool = False
    retry_on_error = []
    ssl: bool = False
    ssl_keyfile = None
    ssl_certfile = None
    ssl_cert_reqs: str = 'required'
    ssl_ca_certs = None
    ssl_ca_path = None
    ssl_check_hostname: bool = False
    ssl_password = None
    ssl_validate_ocsp: bool = False
    ssl_validate_ocsp_stapled: bool = False
    ssl_ocsp_context = None
    ssl_ocsp_expected_cert = None
    max_connections = None
    single_connection_client: bool = False
    health_check_interval: int = 0
    client_name = None
    username: str = None
    retry = None
    redis_connect_func = None

    def asdict(self):
        return dataclasses.asdict(self)
