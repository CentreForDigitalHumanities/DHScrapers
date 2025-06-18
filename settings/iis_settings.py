''' Django settings for I-Analyzer, to set up the IIS corpus for indexing'''

import os

from ianalyzer.common_settings import *

PEACEPORTAL_IIS_DATA = '/postprocessed'
PEACEPORTAL_IIS_ES_INDEX = 'peace-iis'

CORPORA = {
    "peaceportal-iis": "/backend/corpora/peaceportal/iis.py",
}

SERVERS = {
    # Default ElasticSearch server
    'default': {
        'host': os.environ.get('ES_HOST', 'localhost'),
        'port': os.environ.get('ES_PORT', 9200),
        'api_id': os.environ.get('ES_API_ID'),
        'api_key': os.environ.get('ES_API_KEY'),
        'certs_location': os.environ.get('CERTS_LOCATION'),
        'chunk_size': 900,  # Maximum number of documents sent during ES bulk operation
        'max_chunk_bytes': 1*1024*1024,  # Maximum size of ES chunk during bulk operation
        'bulk_timeout': '60s',  # Timeout of ES bulk operation
        'scroll_timeout': '3m',  # Time before scroll results time out
        'scroll_page_size': 5000,  # Number of results per scroll page
        'index_prefix': 'ianalyzer'  # Prefix applied to index names created on this server
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dh-scrapers',
        'USER': 'dh-scrapers',
        'PASSWORD': 'dh-scrapers',
        'HOST': 'db',
        'PORT': 5432
    }
}