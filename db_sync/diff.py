from db_sync.cassandra import setup_cassandra
from db_sync.elastic_search import setup_elastic_search
from db_sync.models import elastic_search, cassandra


class DatabaseDiff:

    def diff(self):
        cassandra_data = list(map(lambda x: x.to_dict(), cassandra.Report.objects.all()))

        elastic_search_raw = elastic_search.Report.search().execute()
        elastic_search_data = list(map(lambda x: x.to_dict(), elastic_search_raw))

        return self._find_diff(cassandra_data, elastic_search_data)

    def _find_diff(self, cassandra_data, elastic_search_data):
        return {
            'elastic_search': self._find_elastic_search_changes(cassandra_data),
            'cassandra': self._find_cassandra_changes(elastic_search_data)
        }

    def _find_elastic_search_changes(self, cassandra_data):
        elastic_search_create = []
        elastic_search_update = []

        for cassandra_row in cassandra_data:
            elastic_row = elastic_search.Report.find_by_uid(cassandra_row['uid'])
            if elastic_row:
                if cassandra_row['created_at'] > elastic_row['created_at']:
                    elastic_search_update.append(cassandra_row)
                else:
                    next
            else:
                elastic_search_create.append(cassandra_row)
        return {
            'create': elastic_search_create,
            'update': elastic_search_update
        }

    def _find_cassandra_changes(self, elastic_search_data):
        cassandra_create = []
        cassandra_update = []

        for elastic_row in elastic_search_data:
            cassandra_row = cassandra.Report.find_by_uid(elastic_row['uid'])
            if cassandra_row:
                if elastic_row['created_at'] > cassandra_row.created_at:
                    cassandra_update.append(elastic_row)
                else:
                    next
            else:
                cassandra_create.append(elastic_row)
        return {
            'create': cassandra_create,
            'update': cassandra_update
        }
