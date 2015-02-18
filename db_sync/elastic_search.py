from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, String, Date, Integer
from elasticsearch_dsl.connections import connections

def setup_elastic_search():
    connections.add_connection('default', Elasticsearch())

