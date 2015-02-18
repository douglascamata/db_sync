from db_sync.cassandra import setup_cassandra
from db_sync.elastic_search import setup_elastic_search
from db_sync.models import elastic_search, cassandra


def setup_all():
    setup_elastic_search()
    setup_cassandra()
    elastic_search.Report.sync_index()
    cassandra.Report.sync_table()
