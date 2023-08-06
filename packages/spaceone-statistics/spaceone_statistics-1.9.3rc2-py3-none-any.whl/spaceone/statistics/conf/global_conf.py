DATABASE_AUTO_CREATE_INDEX = True
DATABASES = {
    'default': {
        'db': 'statistics',
        'host': 'localhost',
        'port': 27017,
        'username': '',
        'password': ''
    }
}

CACHES = {
    'default': {},
    'local': {
        'backend': 'spaceone.core.cache.local_cache.LocalCache',
        'max_size': 128,
        'ttl': 300
    }
}

HANDLERS = {
}

CONNECTORS = {
    'ServiceConnector': {
    }
}

ENDPOINTS = {}
LOG = {}
QUEUES = {}
SCHEDULERS = {}
WORKERS = {}
TOKEN = ""
TOKEN_INFO = {}
CELERY = {}