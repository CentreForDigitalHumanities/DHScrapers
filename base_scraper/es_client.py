from environs import env
from elasticsearch import Elasticsearch

env.read_env("../.env")  # load environment variables from .env file

ES_HOST = env('ES_HOST') or 'localhost'
API_ID = env('API_ID')
API_KEY = env('API_KEY')
CERTS_LOCATION = env('CERTS_LOCATION')


def es_client():
    node = {
        'host': ES_HOST,
        'port': 9200,
    }
    kwargs = {'max_retries': 15, 'retry_on_timeout': True, 'request_timeout': 180}
    if API_ID and API_KEY and CERTS_LOCATION:
        node['scheme'] = 'https'
        kwargs['ca_certs'] = CERTS_LOCATION
        kwargs['api_key'] = (API_ID, API_KEY)
    else:
        node['scheme'] = 'http'
    return Elasticsearch([node], **kwargs)
