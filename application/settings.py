import os
import sys

SERVICE_NAME = 'python-rabbitmq-app'

SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
SERVER_PORT = int(os.getenv('SERVER_PORT', '8080'))

APP_LOGGING_LEVEL = os.getenv('APP_LOGGING_LEVEL', 'INFO')
AIOHTTP_LOGGING_LEVEL = os.getenv('AIOHTTP_LOGGING_LEVEL', 'WARNING')
AIOPIKA_LOGGING_LEVEL = os.getenv('AIOPIKA_LOGGING_LEVEL', 'WARNING')

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', '5672'))
RABBITMQ_LOGIN = os.getenv('RABBITMQ_LOGIN', 'guest')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')
RABBITMQ_PREFETCH_COUNT = int(os.getenv('RABBITMQ_PREFETCH_1', '1'))
RABBITMQ_DEFAULT_TIMEOUT = int(os.getenv('RABBITMQ_DEFAULT_TIMEOUT', '10'))  # seconds

ENVIRONMENT = os.getenv('RUN_ENV', 'LOCAL').upper()

LOGGING: dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'to_json': {
            'class': 'jsonformatter.JsonFormatter',
            'format': {
                'Name': 'name',
                'Levelname': 'levelname',
                'Pathname': 'pathname',
                'Module': 'module',
                'Lineno': 'lineno',
                'FuncName': 'funcName',
                'Time': 'asctime',
                'Message': 'message',
            },
        },
    },
    'handlers': {
        'stdout': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'to_json' if ENVIRONMENT != 'LOCAL' else None,
        },
    },
    'root': {
        'handlers': ['stdout'],
        'level': APP_LOGGING_LEVEL if ENVIRONMENT != 'LOCAL' else 'DEBUG',
    },
    'loggers': {
        'application': {
            'handlers': ['stdout'],
            'level': APP_LOGGING_LEVEL,
            'propagate': True,
        },
        'aiohttp': {
            'handlers': ['stdout'],
            'level': AIOHTTP_LOGGING_LEVEL,
            'propagate': True,
        },
        'aio_pika': {
            'handlers': ['stdout'],
            'level': AIOPIKA_LOGGING_LEVEL,
            'propagate': True,
        },
    },
}
